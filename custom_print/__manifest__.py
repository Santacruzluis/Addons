{
    "name": "Custom Print",
    "version": "1.0",
    "summary": "Personalized printing management",
    "description": "Module to customize invoice printing formats",
    "category": "Tools",
    "author": "Manolo",
    "depends": ["base", "web", "sale"],
    "data": [
        #'security/ir.model.access.csv',
        "views/res_config_settings.xml",
        "views/sale_order.xml",
        "reports/paperformat_data.xml",
        "reports/custom_quotation_report.xml",
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
