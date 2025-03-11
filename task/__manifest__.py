# -*- coding: utf-8 -*-
{
    'name': "Task",

    'summary': "Task custom",

    'description': """
    task custom
    """,

    'author': "Manolo",
    'website': "https://www.yourcompany.com",

    'category': 'Project',
    'version': '0.1',
    'license': 'AGPL-3',

    'depends': ['base',],

    'data': [
        "security/groups.xml",
        'security/ir.model.access.csv',
        'views/task_custom.xml',
        'views/task_person_views.xml',
        'views/menu_task.xml',
        'views/task_filter.xml',
        'data/priority.xml',
    ],
    'installable': True,
    'application': True,
}
