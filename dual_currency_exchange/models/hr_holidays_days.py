from datetime import datetime
import calendar
from odoo import models, fields, api

class HrSpecialDays(models.Model):
    _inherit = "hr.payslip"

    mondays = fields.Integer(
        "Nro lunes",
        compute="_compute_mondays",
        help="Este campo trae el número de lunes en el período",
        store=True,
        readonly=True,
    )

    @api.depends("date_from", "date_to")
    def _compute_mondays(self):
        for selff in self:
            nro_lunes = 0
            if selff.date_from and selff.date_to:
                # Convertir las fechas a objetos datetime
                fecha_inicio = fields.Date.from_string(selff.date_from)
                fecha_fin = fields.Date.from_string(selff.date_to)

                # Calcular la diferencia de días entre las fechas
                delta_dias = (fecha_fin - fecha_inicio).days + 1

                # Obtener el día de la semana de la fecha de inicio
                dia_inicio = fecha_inicio.weekday()  # 0 = lunes, 6 = domingo

                # Calcular el número de lunes en el rango de fechas
                for i in range(delta_dias):
                    if (dia_inicio + i) % 7 == 0:  # 0 representa lunes
                        nro_lunes += 1

            selff.mondays = nro_lunes