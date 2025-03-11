from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    custom_invoice_check = fields.Boolean(
        string="Activar formato de factura",
        help="Habilita esta opción para usar un formato de factura personalizado.",
        config_parameter='custom_invoice.custom_invoice_check'  # Opcional: Guardar el valor como parámetro de configuración global
    )