from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import date

class CustomInheritProductTemplate(models.Model):
  
    _inherit = "product.template"
    _description = "Heredado para Producto Modelo product.template"
    
    active = fields.Boolean(string="Activo", default=True)
    
    available_for_campaign = fields.Boolean(
        string="Disponible para Campaña",
        default=False,
        help="Determina si el producto está disponible para campaña y recibir descuento",
    )
    #this field is used to save the original price of the product
    original_price = fields.Float(
        string="Precio Original",
        readonly=True,
        help="Precio original del producto",
    )
    
    #this field is used to show the original price of the product when a campaign is active
    show_original_price = fields.Boolean(
        string="Mostrar Precio Original",
        compute="_compute_show_original_price",
        help="Determina si el producto está disponible para campaña y recibir descuento y mostrar el precio original",
    )
    
    @api.depends("available_for_campaign")
    def _compute_show_original_price (self):
        today = date.today()
        
        active_campaign = self.env['promotion.campaign'].search([
            ('status', '=', 'active'),
            ('end_date', '>', today)
        ], limit=1)
        
        for record in self:
            if record.available_for_campaign and active_campaign:
                record.show_original_price = True
            else:
                record.show_original_price = False
    
    @api.constrains('available_for_campaign')
    def _check_add_products_only_if_no_active_campaign(self):
        active_campaign = self.env['promotion.campaign'].search([
            ('status', '=', 'active'),
        ], limit=1)
        for record in self:
            if active_campaign and record.available_for_campaign:
                raise ValidationError(
                    _("No se pueden agregar productos mientras haya una campaña de promoción en curso.")
                )