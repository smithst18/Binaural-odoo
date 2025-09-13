from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class AbsenceReason(models.Model):
  
    _name = "hr.absence.reason"
    _description = "Modelo Custom para Hr Motivo de Ausencia"
    
    active = fields.Boolean(string="Activo", default=True)
    
    name = fields.Char(
        string="Motivo de Ausencia",
        required=True,
        copy=False,
        help="Motivo de ausencia",
    )
    
    code = fields.Char(
        string="Codigo",
        required=True,
        copy=False,
        size=8, 
        index=True,
        help="Codigo de motivo de ausencia para abreviaturas",
    )
    
    description = fields.Text(
        string="Descripción del motivo de ausencia",
        required=False,
        copy=False,
        help="Descripción del motivo de ausencia",
    )
    
    _sql_constraints = [
        ("unique_code", "unique(code)", "El codigo de abreviatura debe ser unico"),
    ]
  
    @api.constrains("code")
    def _check_code_format(self):
        for rec in self:
            if rec.code and not rec.code.isupper():
                raise ValidationError("Codigo debe estar en Mayusculas.")
            if " " in rec.code:
                raise ValidationError("El codigo no debe contener espacios.")
