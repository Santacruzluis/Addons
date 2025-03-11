from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    def _get_invoice_format(self):
        # Obtener el valor de custom_invoice_check desde la configuración
        custom_format = self.env['res.config.settings'].sudo().get_values().get('custom_invoice_check', False)
        
        if custom_format:
            return "Formato personalizado"
        else:
            return "Formato estándar"