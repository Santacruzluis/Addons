from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    custom_print_enabled = fields.Boolean(
        compute='_compute_custom_print_enabled',
        store=False
    )
    
    amount_by_group = fields.Binary(
        string="Tax amount by group",
        compute='_compute_amount_by_group',
        help='Amount by tax group for printing in reports'
    )
    
    @api.depends_context('uid')
    def _compute_custom_print_enabled(self):
        """Determina si el formato de impresión personalizado está habilitado"""
        enabled = self.env['ir.config_parameter'].sudo().get_param('custom_print.enable_custom_print', 'False').lower() == 'true'
        for record in self:
            record.custom_print_enabled = enabled
    
    @api.depends('tax_totals')
    def _compute_amount_by_group(self):
        """Compute amount by group for tax totals (adaptado para cotizaciones)"""
        for order in self:
            if order.tax_totals and 'groups_by_subtotal' in order.tax_totals:
                amount_by_group = []
                for subtotal in order.tax_totals['groups_by_subtotal'].values():
                    for group in subtotal:
                        amount_by_group.append((
                            group['tax_group_name'],
                            group['tax_group_amount'],
                            group['tax_group_base_amount']
                        ))
                order.amount_by_group = amount_by_group
            else:
                order.amount_by_group = []
    
    def action_print_custom_quotation(self):
        """Acción para imprimir la cotización con formato personalizado"""
        self.ensure_one()
        report = self.env.ref('custom_print.action_report_custom_quotation')
        paper_size = self.env['ir.config_parameter'].sudo().get_param(
            'custom_print.paper_size', 'letter')
        
        if paper_size == 'half_letter':
            return report.with_context(
                paperformat='custom_print.paperformat_half_letter'
            ).report_action(self)
        return report.report_action(self)