from odoo import api, models, fields
from odoo.exceptions import ValidationError


class TaskTask(models.Model):
    _name = "task.task"
    _description = "Custom Task"

    name = fields.Char(string="Name", required=True)

    priority_id = fields.Many2one(
        comodel_name="task.priority", string="Priority", required=True
    )

    description = fields.Text(string="Description",
                              groups="taks.task_group_admin")

    is_completed = fields.Boolean(string="Completed", default=False)

    person_id = fields.Many2one(comodel_name="task.person", string="Person")

    tag_ids = fields.Many2many(
        comodel_name="task.tag",
        column1="task_id",
        column2="tag_id",
        string="Tag",
    )
