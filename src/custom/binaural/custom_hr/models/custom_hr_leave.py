from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class CustomInheritHrLeave(models.Model):
  
    _inherit = "hr.leave"
    _description = "Campo Heredado para Hr modelo hr.leave"
    
    
    absence_reason_id = fields.Many2one(
        "hr.absence.reason",
        string="Motivo de Ausencia",
        required=True,
        domain="[('active', '=', True)]",
        help="Campo relacional para motivo de ausencia",
    )

