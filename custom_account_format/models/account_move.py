from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    fiscal_check = fields.Boolean(string="Fiscal Format", default=False)
    fiscal_print_date = fields.Date(string="Fiscal Print Date")
    fiscal_payment_condition = fields.Char(string="Payment Condition")
    fiscal_comment = fields.Text(string="Fiscal Comment")
    fiscal_currency_id = fields.Many2one(
        "res.currency", string="Fiscal Currency"
    )
    fiscal_correlative = fields.Char(
        string="Fiscal Correlative",
        compute="_compute_fiscal_correlative",
        store=True,
    )
    fiscal_tax_totals = fields.Json(
        string="Fiscal Tax Totals", compute="_compute_fiscal_tax_totals"
    )

    @api.depends("name", "state")
    def _compute_fiscal_correlative(self):
        for record in self:
            if record.name and record.state == "posted":
                record.fiscal_correlative = record.name
            else:
                record.fiscal_correlative = False

    @api.depends(
        "fiscal_currency_id", "amount_total", "amount_untaxed", "amount_tax"
    )
    def _compute_fiscal_tax_totals(self):
        for record in self:
            if (
                record.fiscal_currency_id
                and record.fiscal_currency_id != record.currency_id
            ):
                # Here you would implement the logic to calculate tax totals in the fiscal currency
                # This is a simplified example
                record.fiscal_tax_totals = record.tax_totals
            else:
                record.fiscal_tax_totals = record.tax_totals

    def print_freeform(self):
        self.ensure_one()
        if not self.fiscal_check:
            raise UserError(
                _("This invoice is not marked for fiscal printing.")
            )

        # Check if we should use half letter or letter format
        report_name = "custom_account_format.action_freeform_letter_report"
        if self.env.company.use_half_letter:
            report_name = (
                "custom_account_format.action_freeform_half_letter_report"
            )

        return self.env.ref(report_name).report_action(self)

    def _get_rate(self):
        """Get the exchange rate between invoice currency and fiscal currency"""
        self.ensure_one()
        if (
            not self.fiscal_currency_id
            or self.fiscal_currency_id == self.currency_id
        ):
            return 1.0

        # Get the rate from the date of the invoice
        rate = self.env["res.currency.rate"].search(
            [
                ("currency_id", "=", self.fiscal_currency_id.id),
                ("name", "<=", self.invoice_date or fields.Date.today()),
            ],
            limit=1,
            order="name desc",
        )

        if rate:
            return rate.rate
        return 1.0

    def _validate_na(self, value):
        """Validate if a value is not empty or 'N/A'"""
        return value and value.upper() != "N/A"
