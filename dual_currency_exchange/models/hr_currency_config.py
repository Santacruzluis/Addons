from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    currency_conversion_id = fields.Many2one(
        "res.currency",
        string="Moneda de Conversión",
        help="Seleccione la moneda a la que se convertirá el salario en las nóminas.",
    )

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        # Guardar en ir.config_parameter
        self.env["ir.config_parameter"].set_param(
            "hr_payroll.currency_conversion_id", self.currency_conversion_id.id
        )
        # Guardar en res.company
        self.env.company.write({
            'currency_conversion_id': self.currency_conversion_id.id
        })

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        # Obtener el valor de res.company
        company_currency_conversion_id = self.env.company.currency_conversion_id.id
        # Si no hay valor en res.company, obtener el valor de ir.config_parameter
        if not company_currency_conversion_id:
            currency_conversion_id = self.env["ir.config_parameter"].get_param(
                "hr_payroll.currency_conversion_id"
            )
            company_currency_conversion_id = int(currency_conversion_id) if currency_conversion_id else False
        # Actualizar el resultado
        res.update(
            currency_conversion_id=company_currency_conversion_id
        )
        return res

class ResCompany(models.Model):
    _inherit = "res.company"

    currency_conversion_id = fields.Many2one(
        "res.currency",
        string="Moneda de Conversión",
        help="Seleccione la moneda a la que se convertirá el salario en las nóminas.",
    )