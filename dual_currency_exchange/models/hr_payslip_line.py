from odoo import models, fields, api

class HrPayslipLine(models.Model):
    _inherit = "hr.payslip.line"
    
    # Campo existente para amount
    wage_in_ves = fields.Monetary(
        string="Monto en VES (Amount)",
        compute="_compute_wage_in_ves",
        store=True,
        currency_field="conversion_currency_id"
    )
    
    # Nuevo campo para total
    total_in_ves = fields.Monetary(
        string="Total en VES (Total)",
        compute="_compute_total_in_ves",
        store=True,
        currency_field="conversion_currency_id"
    )

    conversion_currency_id = fields.Many2one(
        "res.currency",
        string="Moneda de Conversión",
        compute="_compute_conversion_currency",
        store=True
    )

    @api.depends('slip_id.company_id.currency_conversion_id')
    def _compute_conversion_currency(self):
        for line in self:
            line.conversion_currency_id = line.slip_id.company_id.currency_conversion_id

    @api.depends('amount', 'slip_id.date_from', 'conversion_currency_id')
    def _compute_wage_in_ves(self):
        for line in self:
            if not line.conversion_currency_id:
                line.wage_in_ves = 0.0
                continue
            
            line.wage_in_ves = line.currency_id._convert(
                line.amount,
                line.conversion_currency_id,
                line.slip_id.company_id,
                line.slip_id.date_from or fields.Date.today()
            )

    @api.depends('total', 'slip_id.date_from', 'conversion_currency_id')
    def _compute_total_in_ves(self):
        for line in self:
            if not line.conversion_currency_id:
                line.total_in_ves = 0.0
                continue
            
            line.total_in_ves = line.currency_id._convert(
                line.total,
                line.conversion_currency_id,
                line.slip_id.company_id,
                line.slip_id.date_from or fields.Date.today()
            )