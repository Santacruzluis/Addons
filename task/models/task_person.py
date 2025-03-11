from odoo import fields, models


class TaskPerson(models.Model):
    _name = "task.person"

    _description = "custom tasks for one person"

    name = fields.Char(string="person", size=20)

    task_ids = fields.One2many(
        comodel_name="task.task",
        inverse_name="person_id",
        string="Tasks"
    )
