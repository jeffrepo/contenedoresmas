from odoo import models, fields, api
import xlsxwriter
import base64
import io
import logging

class LibroVentasWizard(models.TransientModel):
    _name = 'contenedoresmas.nombre.wizard'
    _description = "Wizard para reporte de ventas"

    fecha_inicio = fields.Date('Fecha inicio')
    fecha_fin = fields.Date('Fecha fin')
    diarios_ids = fields.Many2many('account.journal', string='Diarios')
    name = fields.Char('Nombre archivo', size=32)
    archivo = fields.Binary('Archivo', filters='.xls')

    def print_report(self):
        data = {
            'ids': [],
            'model': 'contenedoresmas.nombre.wizard',
            'form': self.read()[0]
        }
        return self.env.ref('contenedoresmas.nombre.wizard').report_action([], data=data)

    def print_report_excel(self):
        facturas_dict = {}

        for w in self:
            dict = {
                'fecha_inicio': w.fecha_inicio,
                'fecha_fin': w.fecha_fin,
                'diarios_ids': w.diarios_ids.ids
            }

            res = self.env['report.contenedoresmas.reporte.nombre']._get_ventas(dict)

            domain = [
                ('date', '>=', w.fecha_inicio),
                ('date', '<=', w.fecha_fin),
                ('factura_proveedor_id', '!=', False),
                ('journal_id', 'in', w.diarios_ids.ids),
                ('state', '=', 'posted'),
            ]
            facturas = self.env['account.move'].search(domain, order='date asc')
            logging.warning(facturas)

            for factura in facturas:
                fecha_venta = factura.invoice_date
                facturaNo = factura.payment_reference
                tc_venta = factura.tipo_cambio
                factura_dict = {}

                for line in factura.invoice_line_ids:
                    importe_venta = line.price_subtotal
                    flete_venta = 1
                    iva_venta = (importe_venta + flete_venta) * 0.16
                    total_venta = importe_venta + flete_venta + iva_venta
                    importe_venta_tc = tc_venta * importe_venta
                    flete_venta_tc = tc_venta * flete_venta
                    iva_venta_tc = (importe_venta_tc + flete_venta_tc) * 0.16
                    total_venta_tc = importe_venta_tc + flete_venta_tc + iva_venta_tc

                    # Formatear la fecha en el formato deseado
                    fecha_venta_formatted = fecha_venta.strftime('%d/%m/%Y')

                    factura_proveedor = factura.factura_proveedor_id
                    if factura_proveedor:
                        factura_pedimento = str(factura_proveedor.payment_reference) if factura_proveedor.payment_reference else ''
                        fecha_compra = factura_proveedor.invoice_date
                        tc = factura_proveedor.tipo_cambio
                        factura_id = factura_proveedor.fel_serie

                        for line in factura_proveedor.invoice_line_ids:
                            medida = line.product_id.name
                            importe_compra = line.price_subtotal
                            flete = 1
                            iva_compra = (importe_compra + flete) * 0.16
                            total_compra = importe_compra + flete + iva_compra
                            importeC_tc = tc * importe_compra
                            flete_tc = tc * flete
                            iva_tc = (importeC_tc + flete_tc) * 0.16
                            total_compra_tc = importeC_tc + flete_tc + iva_tc
                            utilidad = (importe_venta_tc + flete_venta_tc) - importeC_tc - flete_tc

                            # Formatear la fecha en el formato deseado
                            fecha_compra_formatted = fecha_compra.strftime('%d/%m/%Y')

                            # Agregar los datos al diccionario de la factura
                            factura_dict = {
                                'fecha_compra': fecha_compra_formatted,
                                'factura_pedimento': factura_pedimento,
                                'factura_id': factura_id,
                                'medida': medida,
                                'importe_compra': importe_compra,
                                'flete': flete,
                                'iva_compra': iva_compra,
                                'total_compra': total_compra,
                                'tc': tc,
                                'importeC_tc': importeC_tc,
                                'flete_tc': flete_tc,
                                'iva_tc': iva_tc,
                                'total_compra_tc': total_compra_tc,
                                'fecha_venta': fecha_venta_formatted,
                                'facturaNo': facturaNo,
                                'importe_venta': importe_venta,
                                'flete_venta': flete_venta,
                                'iva_venta': iva_venta,
                                'total_venta': total_venta,
                                'tc_venta': tc_venta,
                                'importe_venta_tc': importe_venta_tc,
                                'flete_venta_tc': flete_venta_tc,
                                'iva_venta_tc': iva_venta_tc,
                                'total_venta_tc': total_venta_tc,
                                'utilidad': utilidad,
                            }

                            # Agregar el diccionario de la factura al diccionario principal
                            facturas_dict[factura.id] = factura_dict
                            factura_dict = {}  # Limpiar el diccionario para la próxima iteración del bucle

                    else:
                        # Agregar los datos al diccionario de la factura
                        factura_dict = {
                            'fecha_venta': fecha_venta_formatted,
                            'facturaNo': facturaNo,
                            'importe_venta': importe_venta,
                            'flete_venta': flete_venta,
                            'iva_venta': iva_venta,
                            'total_venta': total_venta,
                            'tc_venta': tc_venta,
                            'importe_venta_tc': importe_venta_tc,
                            'flete_venta_tc': flete_venta_tc,
                            'iva_venta_tc': iva_venta_tc,
                            'total_venta_tc': total_venta_tc,
                        }

                        # Agregar el diccionario de la factura al diccionario principal
                        facturas_dict[factura.id] = factura_dict


            f = io.BytesIO()
            workbook = xlsxwriter.Workbook(f)
            sheet = workbook.add_worksheet('Reporte ventas')

            # Establecer formato para los títulos de las columnas
            title_format = workbook.add_format({'bold': True, 'font_size': 12})

            # Escribir los títulos de las columnas
            sheet.write(0, 0, 'INVENTARIO DE VENTAS', title_format)
            sheet.write(2, 0, 'Rango de fechas', title_format)
            sheet.write(3, 0, f"{w.fecha_inicio.strftime('%Y-%m-%d')} al {w.fecha_fin.strftime('%Y-%m-%d')}", title_format)

            # Escribir los encabezados de columna
            headers = ['Fecha', 'Factura / Pedimento', 'ID', 'Medida', 'Importe', 'Flete', 'IVA', 'Total', 'TC',
                       'Importe', 'Flete', 'IVA', 'Total', 'Fecha', 'Factura', 'Importe', 'Flete', 'IVA', 'Total', 'TC',
                       'Importe', 'Flete', 'IVA', 'Total', 'Utilidad']
            for i, header in enumerate(headers):
                sheet.write(5, i, header, title_format)

            row = 6  # Fila de inicio de los datos

            for factura_id, factura_data in facturas_dict.items():
                # Escribir los datos de la factura en cada columna correspondiente
                sheet.write(row, 0, factura_data.get('fecha_compra', ''))
                sheet.write(row, 1, factura_data.get('factura_pedimento', ''))
                sheet.write(row, 2, factura_data.get('factura_id', ''))
                sheet.write(row, 3, factura_data.get('medida', ''))
                sheet.write(row, 4, factura_data.get('importe_compra', 0))
                sheet.write(row, 5, factura_data.get('flete', 0))
                sheet.write(row, 6, factura_data.get('iva_compra', 0))
                sheet.write(row, 7, factura_data.get('total_compra', 0))
                sheet.write(row, 8, factura_data.get('tc', 0))
                sheet.write(row, 9, factura_data.get('importeC_tc', 0))
                sheet.write(row, 10, factura_data.get('flete_tc', 0))
                sheet.write(row, 11, factura_data.get('iva_tc', 0))
                sheet.write(row, 12, factura_data.get('total_compra_tc', 0))
                sheet.write(row, 13, factura_data.get('fecha_venta', 0))
                sheet.write(row, 14, factura_data.get('facturaNo', 0))
                sheet.write(row, 15, factura_data.get('importe_venta', 0))
                sheet.write(row, 16, factura_data.get('flete_venta', 0))
                sheet.write(row, 17, factura_data.get('iva_venta', 0))
                sheet.write(row, 18, factura_data.get('total_venta', 0))
                sheet.write(row, 19, factura_data.get('tc_venta', 0))
                sheet.write(row, 20, factura_data.get('importe_venta_tc', 0))
                sheet.write(row, 21, factura_data.get('flete_venta_tc', 0))
                sheet.write(row, 22, factura_data.get('iva_venta_tc', 0))
                sheet.write(row, 23, factura_data.get('total_venta_tc', 0))
                sheet.write(row, 24, factura_data.get('utilidad', 0))

                row += 1

            workbook.close()
            data = base64.b64encode(f.getvalue())
            self.write({'archivo': data, 'name': 'inventario_ventas.xlsx'})

        return {
            'view_mode': 'form',
            'res_model': 'contenedoresmas.nombre.wizard',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
