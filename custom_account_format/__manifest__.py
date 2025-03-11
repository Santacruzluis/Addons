{
    'name': 'Custom Invoice',
    'version': '1.0',
    'summary': 'Módulo personalizado para facturación',
    'description': 'Este módulo añade un check en la configuración para personalizar el formato de factura.',
    'author': 'Manolo',
    'depends': ['base', 'account',"web"],
    'data': [
        'data/data_currency.xml',
        'reports/free_form_template.xml',
        'reports/free_form_report.xml',
        'views/account_invoice_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': True,
}