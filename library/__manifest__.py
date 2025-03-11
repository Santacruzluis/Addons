# -*- coding: utf-8 -*-
{
    "name": "Library",
    "summary": "Library Management",
    "description": """
    Library Management
    """,
    "author": "Praxya Soluciones",
    "website": "https://www.praxya.com",
    "category": "Services",
    "version": "1.5",
    "license": "AGPL-3",
    "application": True,
    # any module necessary for this one to work correctly
    "depends": [
        "base",
    ],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "security/groups.xml",
        "views/library_book_views.xml",
        "views/library_author_views.xml",
        "views/library_book_category_views.xml",
        "views/library_book_order_views.xml",
        "views/menus.xml",
        "data/library_book_stages.xml",
        "data/library_book_categories.xml",
    ],
}
