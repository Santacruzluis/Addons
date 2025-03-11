# -*- coding: utf-8 -*-

from odoo import models, fields


class BookStage(models.Model):
    _name = 'library.book.stage'

    _description = "Library Book stage Model"

    name = fields.Char(
        string="Stage",
        size=20,
    )
