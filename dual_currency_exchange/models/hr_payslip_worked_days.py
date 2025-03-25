from odoo import models, fields, api

class HrPayslipWorkedDays(models.Model):
    _inherit = "hr.payslip.worked_days"

    amount_in_ves = fields.Monetary(
        string="Monto en VES",
        compute="_compute_amount_in_ves",
        currency_field="conversion_currency_id",
        help="Monto convertido a la moneda de conversión configurada."
    )

    conversion_currency_id = fields.Many2one(
        "res.currency",
        related="payslip_id.conversion_currency_id",
        string="Moneda de Conversión",
        store=True
    )

    @api.depends('amount', 'payslip_id.date_from', 'conversion_currency_id')
    def _compute_amount_in_ves(self):
        for line in self:
            if not line.conversion_currency_id:
                line.amount_in_ves = 0.0
                continue

            line.amount_in_ves = line.payslip_id.currency_id._convert(
                line.amount,
                line.conversion_currency_id,
                line.payslip_id.company_id,
                line.payslip_id.date_from or fields.Date.today()
            )