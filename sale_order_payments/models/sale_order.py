# -*- coding: utf-8 -*-

import logging
from odoo import _, api, models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    transactions_count = fields.Integer(
        string="Total Done", copy=False, compute="_compute_transactions_count"
    )
    transaction_done_ids = fields.Many2many(
        comodel_name="payment.transaction",
        string="Done Transactions",
        help="Show Done Transactions",
        compute="_compute_done_transaction_ids",
        copy=False,
        compute_sudo=True,
    )

    payments_total = fields.Float(
        string="Total Payments",
        # readonly=True,
        store=True,
        precompute=True,
        compute="_compute_payments_total",
    )

    @api.depends("transaction_ids.state")
    def _compute_payments_total(self):
        for order in self:
            order.payments_total = sum(
                x.amount
                for x in order.transaction_ids
                if x.state in ("authorized", "done")
            )

    @api.depends("transaction_ids")
    def _compute_transactions_count(self):
        for sale in self:
            sale.transactions_count = len(sale.transaction_ids)

    @api.depends("transaction_ids")
    def _compute_done_transaction_ids(self):
        for sale in self:
            sale.transaction_done_ids = sale.transaction_ids.filtered(
                lambda t: t.state == "done"
            )

    def action_view_transactions(self):
        res_action = {
            "name": _("Payments"),
            "type": "ir.actions.act_window",
            "res_model": "payment.transaction",
            "target": "current",
        }
        payments = self.transaction_ids.ids
        if len(payments) == 1:
            res_action["res_id"] = payments[0]
            res_action["view_mode"] = "form"
        else:
            res_action["view_mode"] = "tree,form"
            res_action["domain"] = [("id", "in", payments)]
        return res_action
