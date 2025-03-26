from odoo import models, fields, api
from datetime import date

class HrContract(models.Model):
    _inherit = 'hr.contract'

    wage_in_ves = fields.Monetary(
        string='Salario en moneda secundaria',
        compute='_compute_wage_in_ves',
        inverse='_inverse_wage_in_ves',
        store=True,
        help='Salario en la moneda secundaria configurada',
        currency_field='conversion_currency_id'
    )
    conversion_currency_id = fields.Many2one(
        'res.currency', 
        string='Moneda de conversión',
        related='company_id.currency_conversion_id',
        readonly=True
    )

    @api.depends('wage', 'company_id.currency_id', 'company_id.currency_conversion_id', 'company_id.currency_conversion_id.rate_ids.rate')
    def _compute_wage_in_ves(self):
        for contract in self:
            if not contract.company_id.currency_conversion_id or not contract.wage:
                contract.wage_in_ves = 0.0
                continue
                
            company_currency = contract.company_id.currency_id
            conversion_currency = contract.company_id.currency_conversion_id
            
            contract.wage_in_ves = company_currency._convert(
                contract.wage,
                conversion_currency,
                contract.company_id,
                fields.Date.today()
            )

    def _inverse_wage_in_ves(self):
        for contract in self:
            if not contract.company_id.currency_conversion_id or not contract.wage_in_ves:
                continue
                
            company_currency = contract.company_id.currency_id
            conversion_currency = contract.company_id.currency_conversion_id
            
            contract.wage = conversion_currency._convert(
                contract.wage_in_ves,
                company_currency,
                contract.company_id,
                fields.Date.today()
            )