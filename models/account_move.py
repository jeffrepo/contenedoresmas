# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import api, fields, models, tools, SUPERUSER_ID
from odoo.tools.translate import _
import xmlrpc.client

class AccountMove(models.Model):
    _inherit = "account.move"

    tipo_cambio = fields.Float(
        compute='_compute_currency_rate_contenedores',string="Tipo de cambio",
        help="Currency rate from company currency to document currency.",
    )

    tipo_factura = fields.Char(string="Tipo de Factura")


    factura_proveedor_id = fields.Many2one(
        comodel_name='account.move',  # Nombre del modelo relacionado
        string='Factura Proveedor'
    )

    @api.depends('currency_id', 'company_id', 'invoice_date')
    def _compute_currency_rate_contenedores(self):
        for factura in self:
            if factura.invoice_date and factura.company_id.currency_id != factura.currency_id:
                tipo_cambio = self.env['res.currency']._get_conversion_rate(
                    from_currency= factura.currency_id,
                    to_currency=factura.company_id.currency_id,
                    company=factura.company_id,
                    date=factura.invoice_date,
                )
                factura.tipo_cambio = tipo_cambio
            else:
                factura.tipo_cambio = 1.0
