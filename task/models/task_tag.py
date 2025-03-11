from odoo import fields, models


class TaskTag(models.Model):
    _name = "task.tag"

    _description = "Etiqueta de una tarea"

    name = fields.Char(string="Tag")
