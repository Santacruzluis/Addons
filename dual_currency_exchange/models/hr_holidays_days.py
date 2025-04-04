# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    # Campos existentes (según tu código previo)
    wage_in_ves = fields.Monetary(
        string="Salario en moneda secundaria",
        compute="_compute_wage_in_ves",
        store=True,
        currency_field="conversion_currency_id",
    )
    conversion_currency_id = fields.Many2one(
        "res.currency",
        string="Moneda de conversión",
        related="company_id.currency_conversion_id",
        readonly=True,
    )
    mondays = fields.Integer(
        string="Número de Lunes (Período)",
        compute="_compute_mondays",
        store=True,
    )

    # Nuevo campo
    mondays_month = fields.Integer(
        string="Lunes del Mes",
        compute="_compute_mondays_month",
        store=True,
        help="Número de lunes en el mes completo de la fecha 'date_to'",
    )

    # Métodos computados
    @api.depends("date_from", "date_to")
    def _compute_mondays(self):
        for payslip in self:
            if not payslip.date_from or not payslip.date_to:
                payslip.mondays = 0
                continue

            date_from = datetime.combine(
                payslip.date_from, datetime.min.time()
            )
            date_to = datetime.combine(payslip.date_to, datetime.min.time())

            mondays_count = 0
            current_date = date_from

            while current_date <= date_to:
                if current_date.weekday() == 0:  # 0 = Lunes
                    mondays_count += 1
                current_date += relativedelta(days=1)

            payslip.mondays = mondays_count

    @api.depends("date_to")
    def _compute_mondays_month(self):
        for payslip in self:
            if not payslip.date_to:
                payslip.mondays_month = 0
                continue

            month_start = payslip.date_to.replace(day=1)
            next_month = month_start + relativedelta(months=1)
            month_end = next_month - relativedelta(days=1)

            mondays = 0
            current_date = month_start
            while current_date <= month_end:
                if current_date.weekday() == 0:
                    mondays += 1
                current_date += relativedelta(days=1)

            payslip.mondays_month = mondays

    @api.depends(
        "net_wage",
        "company_id.currency_id",
        "company_id.currency_conversion_id",
    )
    def _compute_wage_in_ves(self):
        for payslip in self:
            if not payslip.company_id.currency_conversion_id:
                payslip.wage_in_ves = 0.0
                continue

            company_currency = payslip.company_id.currency_id
            conversion_currency = payslip.company_id.currency_conversion_id

            if company_currency and conversion_currency:
                payslip.wage_in_ves = company_currency._convert(
                    payslip.net_wage,
                    conversion_currency,
                    payslip.company_id,
                    fields.Date.today(),
                )
            else:
                payslip.wage_in_ves = 0.0
