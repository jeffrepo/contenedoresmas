
# -*- coding: utf-8 -*-

{
    'name': 'Contenedores mas',
    'version': '1.0',
    'category': 'CRM',
    'sequence': 6,
    'summary': 'Contenedores mas',
    'description': """ Contenedores mas """,
    'author': 'JS',
    'depends': ['base','base_automation','crm','account'],
    'data': [
        # 'data/base_automation_data.xml',
        'views/crm_lead_views.xml',
        'views/reporte_invoice.xml',
        'views/account_move_views.xml',
    ],

    'installable': True,
    'website': 'http://silvatechnologies.odoo.com',
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
