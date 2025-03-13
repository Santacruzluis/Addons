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

        # Verificar si el formato libre está activado en la configuración global
        custom_invoice_check = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("custom_account_format.custom_invoice_check")
        )
        if custom_invoice_check not in ("True", "true", "1"):
            raise UserError(
                _("Freeform format is not enabled in the settings.")
            )

        # Determinar el formato del informe basado en la compañía
        report_name = (
            "custom_account_format.action_free_form_half_letter_report"
            if self.env.company.use_half_letter
            else "custom_account_format.action_free_form_letter_report"
        )

        return self.env.ref(report_name).report_action(self)

    def _get_rate(self):
        get_rate = self.env["res.currency"]._get_conversion_rate
        max_rate = max(
            get_rate(
                self.currency_id,
                self.fiscal_currency_id,
                self.company_id,
                self.date or fields.date.today()
            ),
            get_rate(
                self.fiscal_currency_id,
                self.currency_id,
                self.company_id,
                self.date or fields.date.today()
            ))
        return self.currency_id.format(max_rate)

    def _validate_na(self, value):
        """Validate if a value is not empty or 'N/A'"""
        return value and value.upper() != "N/A"
