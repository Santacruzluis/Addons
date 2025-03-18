from odoo import models, fields, api

class HrContract(models.Model):
    _inherit = 'hr.contract'

    wage_in_ves = fields.Monetary(
        string="Salario en VEF",
        compute="_compute_wage_in_ves",
        store=False,  # No se almacena en la base de datos
        help="Salario convertido a VEF"
    )

    @api.depends('wage', 'currency_id')
    def _compute_wage_in_ves(self):
        for contract in self:
            # Obtener la tasa de cambio actual para VES
            ves_currency = self.env['res.currency'].search([('name', '=', 'VEF')], limit=1)
            if ves_currency and contract.currency_id:
                # Convertir el salario a VES
                contract.wage_in_ves = contract.currency_id._convert(
                    contract.wage,  # Monto a convertir
                    ves_currency,   # Moneda de destino (VES)
                    contract.company_id or self.env.company,  # Compañía
                    fields.Date.today()  # Fecha de conversión
                )
            else:
                contract.wage_in_ves = 0.0