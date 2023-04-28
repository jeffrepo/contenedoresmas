# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import api, fields, models, tools, SUPERUSER_ID
from odoo.tools.translate import _
import xmlrpc.client

class Lead(models.Model):
    _inherit = "crm.lead"

    medida_contenedor = fields.Char('Medidas de contenedor')

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
