from odoo import models, fields, api

class HrContract(models.Model):
    _inherit = 'hr.contract'

    wage_in_ves = fields.Monetary(
        string='Salario en moneda secundaria',
        compute='_compute_wage_in_ves',
        inverse='_inverse_wage_in_ves',
        store=True,
        currency_field='conversion_currency_id'
    )
    
    conversion_currency_id = fields.Many2one(
        'res.currency', 
        related='company_id.currency_conversion_id',
        readonly=True
    )
    
    enable_secondary_currency = fields.Boolean(
        string='Editar salario en moneda secundaria',
        default=False
    )

    @api.depends('wage', 'company_id.currency_id', 'company_id.currency_conversion_id')
    def _compute_wage_in_ves(self):
        for contract in self:
            if not contract.company_id.currency_conversion_id or not contract.wage:
                contract.wage_in_ves = 0.0
                continue
                
            if not contract.enable_secondary_currency:
                contract.wage_in_ves = contract.company_id.currency_id._convert(
                    contract.wage,
                    contract.company_id.currency_conversion_id,
                    contract.company_id,
                    fields.Date.today()
                )

    def _inverse_wage_in_ves(self):
        for contract in self:
            if not contract.company_id.currency_conversion_id or not contract.wage_in_ves:
                continue
                
            if contract.enable_secondary_currency:
                contract.wage = contract.company_id.currency_conversion_id._convert(
                    contract.wage_in_ves,
                    contract.company_id.currency_id,
                    contract.company_id,
                    fields.Date.today()
                )