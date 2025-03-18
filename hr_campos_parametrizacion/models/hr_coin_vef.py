from odoo import models, fields, api


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    wage_in_ves = fields.Monetary(
        string="Salario en VEF", compute="_compute_wage_in_ves", store=False
    )

    @api.depends("contract_id")
    def _compute_wage_in_ves(self):
        for slip in self:
            slip.wage_in_ves = (
                slip.contract_id.wage_in_ves if slip.contract_id else 0.0
            )
