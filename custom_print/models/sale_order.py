from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    custom_print_enabled = fields.Boolean(
        compute='_compute_custom_print_enabled',
        store=False,
        string='Formato Personalizado Activado'
    )
    
    amount_by_group = fields.Binary(
        string="Impuestos por Grupo",
        compute='_compute_amount_by_group',
        help='Monto agrupado por impuestos para mostrar en reportes'
    )
    
    is_compact_mode = fields.Boolean(
        string="Modo Compacto",
        compute='_compute_compact_mode',
        help='Habilita el formato ultra compacto para más líneas por página'
    )
    
    @api.depends_context('uid')
    def _compute_custom_print_enabled(self):
        """Determina si el formato de impresión personalizado está habilitado"""
        enabled = self.env['ir.config_parameter'].sudo().get_param(
            'custom_print.enable_custom_print', 'False').lower() == 'true'
        for record in self:
            record.custom_print_enabled = enabled
    
    @api.depends('tax_totals')
    def _compute_amount_by_group(self):
        """Calcula montos por grupo de impuestos"""
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
    
    def _compute_compact_mode(self):
        """Determina si usar el modo compacto basado en parámetros"""
        compact = self.env['ir.config_parameter'].sudo().get_param(
            'custom_print.compact_mode', 'False').lower() == 'true'
        for record in self:
            record.is_compact_mode = compact
    
    def action_print_custom_quotation(self):
        """Acción para imprimir la cotización con formato personalizado"""
        self.ensure_one()
        
        # Obtener el reporte con manejo robusto de errores
        report = self._get_custom_report()
        
        # Configurar el contexto basado en parámetros
        context = {
            'paperformat': 'custom_print.paperformat_half_letter' if 
                self.env['ir.config_parameter'].sudo().get_param(
                    'custom_print.paper_size', 'letter') == 'half_letter' 
                else None,
            'report_mode': 'compact' if self.is_compact_mode else 'normal'
        }
        
        return report.with_context(**context).report_action(self)
    
    def _get_custom_report(self):
        """Obtiene el reporte personalizado con múltiples intentos"""
        try:
            return self.env.ref('custom_print.report_custom_quotation')
        except ValueError:
            try:
                return self.env.ref('custom_print.action_report_custom_quotation')
            except ValueError:
                # Fallback al reporte estándar si los personalizados no existen
                return self.env.ref('sale.action_report_saleorder')