from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    enable_custom_print = fields.Boolean(
        string="Activar Formato Personalizado",
        config_parameter="custom_print.enable_custom_print",
    )

    paper_size = fields.Selection(
        [("letter", "Tamaño Carta"), ("half_letter", "Media Carta")],
        string="Tamaño de Papel",
        config_parameter="custom_print.paper_size",
        default="letter",
    )