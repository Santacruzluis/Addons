# -*- coding: utf-8 -*-

from odoo import api, models, fields
from odoo.exceptions import ValidationError


class LibraryBook(models.Model):
    _name = "library.book"

    _description = "Library Book Model"

    name = fields.Char(
        string="Name",
    )
    active = fields.Boolean(string="Active", default=True)
    isbn = fields.Char(string="ISBN", size=9, required=True)
    date = fields.Date(string="Publication Date")
    image = fields.Image()
    stage_id = fields.Many2one("library.book.stage", string="Stage")
    author_id = fields.Many2one("library.author", string="Author")

    author_dni = fields.Char(string="Author's DNI", related="author_id.dni")
    pages = fields.Integer(string="Pages")
    description = fields.Html(string="Description")
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.company.currency_id,
        store=True,
    )
    price = fields.Monetary(
        string="Price", groups="library.library_group_admin"
    )
    comments = fields.Text(string="Comments")

    categ_ids = fields.Many2many(
        comodel_name="library.book.category",
        column1="book_id",
        column2="category_id",
        string="Categories",
    )

    @api.constrains("isbn")
    def _check_unique_isbn(self):
        domain = [("id", "!=", self.id), ("isbn", "in", self.mapped("isbn"))]
        books = self.env["library.book"].search(domain)
        if books:
            raise ValidationError("ISBN must be unique")

    @api.onchange("author_id")
    def _onchnage_author(self):
        return {
            "warning": {
                "title": "Warning",
                "message": "Author changed: {}".format(self.author_id.name),
                "type": "notification",
            },
        }

    @api.model
    def default_get(self, fields_list):
        res = super(LibraryBook, self).default_get(fields_list)
        stage_id = self.env.ref("library.library_book_stage_new")
        if stage_id:
            res["stage_id"] = stage_id.id
        domain = [("name", "in", ["Frontend", "Backend"])]
        def_tag_ids = self.env["library.book.category"].search(domain)
        if def_tag_ids:
            res["categ_ids"] = [(6, 0, def_tag_ids.ids)]
        return res
