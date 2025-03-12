from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    municipality = fields.Char(string='Municipio')
    ruc = fields.Char(string='RUC')
    taxpayer_license = fields.Char(string='Licencia de Contribuyente (LAE)')
    use_half_letter = fields.Boolean(string='Usar Formato Media Carta', default=False)

