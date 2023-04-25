# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import api, fields, models, tools, SUPERUSER_ID
from odoo.tools.translate import _
import xmlrpc.client

class Lead(models.Model):
    _inherit = "crm.lead"

    def crear_oportunidad(self, url, db, username, password):
        # url = "https://avanguardiatech-contenedoresmas-pruebas-7433491.dev.odoo.com/xmlrpc"
        # db = 'avanguardiatech-contenedoresmas-pruebas-7433491'
        # username = 'leonardo@contenedoresmas.com'
        # password = 'Contenedoresmas23'
        for record in self:
            print ("URLL", url)
            common = xmlrpc.client.ServerProxy(url +'/common')
            uid = common.login(db, username, password)
            print ("UIDDD", uid)
            models = xmlrpc.client.ServerProxy(url +'/object')
            prodid = models.execute_kw(db, uid, password, 'crm.lead', 'create', [{
                'contact_name': record.contact_name,
                'name': record.name,
                'type': record.type,
                'email_from': record.email_from,
                'mobile': record.mobile,
                'city': record.city,
                'description': record.description.replace('\n', '<br>') if record.description else "",

              }])
            print ("prodid",prodid)
        return True
