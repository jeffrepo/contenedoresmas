# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import api, fields, models, tools, SUPERUSER_ID
from odoo.tools.translate import _
import xmlrpc.client

class Lead(models.Model):
    _inherit = "crm.lead"

    medida_contenedor = fields.Char('Medidas de contenedor')
    notas_extras = fields.Text('Notas extras')
