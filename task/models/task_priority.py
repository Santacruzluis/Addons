from odoo import api, models, fields
from odoo.exceptions import UserError


class TaskPriority(models.Model):
    _name = "task.priority"

    _description = "Prioridad de tarea"

    name = fields.Char(string="Priority")

    @api.ondelete(at_uninstall=False)
    def _unlink_except_high_priority(self):
        master_xmlids = [
            "priority_high",
            "priority_medium",
            "priority_low",
        ]
        for master_xmlid in master_xmlids:
            master_tag = self.env.ref(
                f"task.{master_xmlid}", raise_if_not_found=False
            )
            if master_tag and master_tag in self:
                raise UserError(
                    "No puedes eliminar esta caterogria de prioridad"
                )
