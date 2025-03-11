# -*- coding: utf-8 -*-

from odoo import api, models, fields


class LibraryAuthor(models.Model):
    _name = "library.author"

    _description = "Library author Model"

    name = fields.Char(
        string="Author",
        size=20,
    )
    image = fields.Image()
    book_ids = fields.One2many(
        comodel_name="library.book", inverse_name="author_id", string="Books"
    )
    book_ids_count = fields.Integer(compute="_compute_book_count")
    dni = fields.Char(string="DNI")
    passport = fields.Char(string="Passport")

    can_edit = fields.Boolean(compute="_can_edit")

    @api.depends_context("uid")
    def _can_edit(self):
        for rec in self:
            rec.can_edit = self.env.user.has_group(
                "library.library_group_admin"
            )

    def _compute_book_count(self):
        for rec in self:
            rec.book_ids_count = len(rec.book_ids)

    def view_action_books(self):
        action = {
            "name": "Books",
            "type": "ir.actions.act_window",
            "target": "current",
            "res_model": "library.book",
            "view_mode": "tree,form",
            "domain": [("id", "in", self.book_ids.ids)],
        }
        return action
