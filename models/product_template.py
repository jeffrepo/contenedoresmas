from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    contenedor = fields.Boolean(string='Contenedor')
    flete = fields.Boolean(string='Flete')
