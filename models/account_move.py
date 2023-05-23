# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import api, fields, models, tools, SUPERUSER_ID
from odoo.tools.translate import _
import xmlrpc.client

class AccountMove(models.Model):
    _inherit = "account.move"

    tipo_cambio = fields.Float(
        compute='_compute_currency_rate_contenedores',
        help="Currency rate from company currency to document currency.",
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
                
    # def crear_oportunidad(self, url, db, username, password):
    #
    #     for record in self:
    #         if record.type == "lead":
    #             print ("URLL", url)
    #             common = xmlrpc.client.ServerProxy(url +'/common')
    #             uid = common.login(db, username, password)
    #             print ("UIDDD", uid)
    #             models = xmlrpc.client.ServerProxy(url +'/object')
    #             prodid = models.execute_kw(db, uid, password, 'crm.lead', 'create', [{
    #                 'contact_name': record.contact_name,
    #                 'name': record.name,
    #                 'type': record.type,
    #                 'email_from': record.email_from,
    #                 'mobile': record.mobile,
    #                 'city': record.city,
    #                 'description': record.description.replace('\n', '<br>') if record.description else "",
    #
    #               }])
    #             print ("prodid",prodid)
    #     return True
