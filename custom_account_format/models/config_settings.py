from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    custom_invoice_check = fields.Boolean(
        string='Usar Formato de Factura Libre', 
        config_parameter='custom_account_format.custom_invoice_check'
    )
    
    use_half_letter = fields.Boolean(
        string='Usar Formato Media Carta',
        related='company_id.use_half_letter',
        readonly=False
    )

