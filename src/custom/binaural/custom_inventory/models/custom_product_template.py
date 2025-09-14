from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import date

class CustomInheritProductTemplate(models.Model):
  
    _inherit = "product.template"
    _description = "Modelo Heredado para Producto product.template"
    
    package_type_id = fields.Many2one(
        "stock.package.type",
        string="Tipo de Paqueteria",
        help="Tipo de paqueteria para la consolidacion",
    )