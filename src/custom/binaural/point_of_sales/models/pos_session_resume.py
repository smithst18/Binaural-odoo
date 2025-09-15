from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import date

class PossSessionResume(models.Model):
  
    _name = "pos.session_resume"
    _description = "Modelo Custom para Pos Session Resume"
    
    #sesion resume 
    pos_session_id = fields.Many2one(
        "pos.session",
        string="Sesión",
        help="Pos Session",
        readonly=True,
    )
    
    user_id = fields.Many2one(
        related="pos_session_id.user_id", 
        string="Usuario",
        help="Usuario",
    )
    
    sesion_duration = fields.Float(
        string="Duración de la sesión (h)",
        readonly=True,
        help="Duración (h)",
    )
    #sales resume
    
    total_sales = fields.Float(
        string="Total de ventas",
        readonly=True,
        help="Total de ventas",
    )
    transactions_count = fields.Integer(
        string="Transacciones totales",
        readonly=True,
        help="Transacciones",
    )
    
    #products resume 
    total_products_amount = fields.Float(
        string="Productos vendidos",
        readonly=True,
        help="Total de Productos vendidos",
    )
    #top saled products at least 3 products
    top_product_ids = fields.One2many(
        "pos.top_product",
        "pos_session_resume_id",
        string="Top Productos",
        help="Los productos más vendidos de la sesión"
    )
    
    
class PosSessionResumeTopProduct(models.Model):
  
    _name = "pos.top_product"
    _description = "Modelo Custom para Pos Top Products"
    
    pos_session_resume_id = fields.Many2one(
        "pos.session_resume",
        string="Resumen de la sesión",
        help="Resumen de la sesión",
        readonly=True,
    )
    
    product_id = fields.Many2one(
        "product.template",
        string="Producto",
        help="Producto",
        readonly=True,
    )
    
    quantity = fields.Integer(
        string="Cantidad",
        readonly=True,
        help="Cantidad",
    )