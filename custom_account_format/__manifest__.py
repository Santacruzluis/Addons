{
    'name': 'Custom Invoice',
    'version': '1.0',
    'summary': 'Módulo personalizado para facturación',
    'description': 'Este módulo añade un check en la configuración para personalizar el formato de factura.',
    'author': 'Tu Nombre',
    'depends': ['base', 'account',"web"],
    'data': [
        'views/res_config_settings_views.xml',
        'views/account_invoice_views.xml',
    ],
    'installable': True,
    'application': True,
}