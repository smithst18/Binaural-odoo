from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CustomResConfigSettings(models.TransientModel):
  
    _inherit = 'res.config.settings'
    
    double_validation = fields.Boolean(
        string='Activar Doble Validación de Pagos',
        default=False,
        help='Determina si se implementará la validación de pagos',
        config_parameter='custom_contability.double_validation'
    )
    
    double_validation_limit = fields.Float(
        string='Límite para Doble Validación de Pagos',
        default=50000.0,
        help='Determina el límite para la validación de pagos',
        config_parameter='custom_contability.double_validation_limit'
    )
    #constrains
    #validate double validation >  0 (ostive number)
    @api.constrains('double_validation', 'double_validation_limit')
    def _check_double_validation_limit(self):
        for record in self:
            if record.double_validation and record.double_validation_limit <= 0:
                raise ValidationError(
                    _('El límite para la doble validación de pagos debe ser mayor a 0 cuando la opción está activada.')
                )
