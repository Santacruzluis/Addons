{
    'name': 'Res Partner Custom',
    'version': '1.0',
    'summary': 'ResPartner Custom',
    'description': """
    Este modulo permite agregar varias customizaciones
    ejercicios del curso Backend que estamos realizando 
    al modulo base por ejemplo al modelo res.partner
    """,
    'category': 'Hidden',
    'author': 'odooexperto',
    'license': 'AGPL-3',
    'depends': ['base'],
    'data': [
        'views/res_partner_filter.xml'
    ],
    'installable': True,
    'auto_install': False,
}
