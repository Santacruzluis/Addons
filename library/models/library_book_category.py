# -*- coding: utf-8 -*-

from odoo import api, models, fields
from odoo.exceptions import UserError


class BookCategory(models.Model):
    _name = "library.book.category"

    _description = "Library Book category Model"

    name = fields.Char(
        string="Category Name",
        size=20,
    )

    color = fields.Integer(string="Color")

    @api.ondelete(at_uninstall=False)
    def _unlink_except_master_category(self):
        master_xmlids = [
            "library.library_book_category_1",
        ]
        # check if category un master data, root data
        for master_xmlid in master_xmlids:
            if master_xmlid in self.get_external_id().values():
                raise UserError("No puedes eliminar esta Categoria!")
        # check if category in books
        book_categ_ids = (
            self.env["library.book"].search([]).mapped("categ_ids").ids
        )
        if any(self.ids) in book_categ_ids:
            raise UserError(
                "Esta categoria esta usada en uno o varios Libros"
            )
