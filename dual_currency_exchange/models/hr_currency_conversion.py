from odoo import models, fields, api

class HrContract(models.Model):
    _inherit = 'hr.contract'

    wage_in_ves = fields.Monetary(
        string="Salario en Conversión",
        compute="_compute_wage_in_ves",
        store=False,
        help="Salario convertido a la moneda de conversión configurada (opcional).",
        currency_field="conversion_currency_id"  # Asociar el campo con la moneda de conversión
    )
    
    conversion_currency_id = fields.Many2one(
        "res.currency",
        string="Moneda de Conversión",
        compute="_compute_conversion_currency",
        help="Moneda de conversión configurada en la compañía."
    )

    @api.depends('company_id.currency_conversion_id')
    def _compute_conversion_currency(self):
        for contract in self:
            contract.conversion_currency_id = contract.company_id.currency_conversion_id

    @api.depends('wage', 'currency_id', 'conversion_currency_id')
    def _compute_wage_in_ves(self):
        for contract in self:
            # Obtener la moneda de conversión configurada en la compañía
            conversion_currency = contract.company_id.currency_conversion_id

            # Si no hay moneda de conversión configurada, establecer el valor en 0.0
            if not conversion_currency:
                contract.wage_in_ves = 0.0
                continue  # Salir del bucle para este contrato

            # Convertir el salario a la moneda de conversión
            if contract.currency_id and conversion_currency:
                contract.wage_in_ves = contract.currency_id._convert(
                    contract.wage,  # Monto a convertir
                    conversion_currency,  # Moneda de destino (configurada en la compañía)
                    contract.company_id or self.env.company,  # Compañía
                    fields.Date.today()  # Fecha de conversión
                )
            else:
                contract.wage_in_ves = 0.0