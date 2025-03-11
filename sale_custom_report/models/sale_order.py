# -*- coding: utf-8 -*-

import logging
from odoo import _, api, models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    tot_articulos = fields.Float(compute="_compute_tot_products")

    @api.depends("order_line")
    def _compute_tot_products(self):
        so_line = "SALE_ORDER_LINE"
        query = f"""
        SELECT
        SALE_ORDER.ID,
        SUM({so_line}.PRODUCT_UOM_QTY) AS CANTIDAD
        FROM
            SALE_ORDER
            INNER JOIN  {so_line} ON SALE_ORDER.ID = {so_line}.ORDER_ID
        WHERE
            SALE_ORDER.ID = %s
        GROUP BY
            SALE_ORDER.ID
        ORDER BY
            SALE_ORDER.ID
        """
        for sale in self:
            self._cr.execute(query, [tuple(sale.ids)])
            query_res = self._cr.dictfetchall()
            sale.tot_articulos = 0
            if query_res:
                sale.tot_articulos = query_res[0].get("cantidad")
