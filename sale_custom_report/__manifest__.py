# -*- coding: utf-8 -*-
{
    "name": "Sale Order Custom Report",
    "summary": "Custom report for sales",
    "description": """
    Practice Custom Report for Sales
    """,
    "author": "Praxya Soluciones.",
    "website": "https://www.praxya.com",
    "category": "Sales",
    "version": "0.2",
    "license": "AGPL-3",
    "depends": ["sale", "web"],
    # always loaded
    "data": [
        "reports/sale_report_templates.xml",
        "reports/paperformat.xml",
        "reports/sale_report.xml",
    ],
    "assets": {
        # Lo usamos para cargar estilos propios al informe
        "web.report_assets_common": [
            "sale_custom_report/static/src/scss/style.scss"
        ],
    }
}
