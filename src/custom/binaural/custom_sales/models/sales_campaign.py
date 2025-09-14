from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import date
import logging

_logger = logging.getLogger(__name__)

class PromotionCampaign(models.Model):
  
    _name = "promotion.campaign"
    _description = "Modelo Custom para Campaña de Promoción"
    _order = "start_date desc"
    
        
    def action_start_campaign (self):
        self.ensure_one()
        self.status = "active"
        
        products = self.env["product.template"].search([
            ("available_for_campaign", "=", True),
            ("sale_ok", "=", True)
        ])
        
        for product in products:
            if product.list_price > 0:
                product.write({
                  "original_price": product.list_price,
                  "list_price": product.list_price * (1 - self.discount)
                })
            else: 
                continue

    def action_end_campaign (self):
        self.ensure_one()
        self.status = "end"
        
        products = self.env["product.template"].search([
            ("available_for_campaign", "=", True),
            ("sale_ok", "=", True)
        ])
        
        for product in products:
            product.list_price = product.original_price
        
    status = fields.Selection(
        selection=[
            ('draft', 'Borrador'),
            ('active', 'Activa'),
            ('end', 'Finalizada'),
        ],
        index=True,
        string="Estado",
        default="draft",
        help="Estado de la campaña",
    )   
    
    name = fields.Char(
        string="Nombre",
        required=True,
        help="Nombre de la campaña de promoción",
    )
    
    start_date = fields.Date(
        string="Fecha de Inicio",
        required=True,
        help="Fecha de inicio",
    )
    
    end_date = fields.Date(
        string="Fecha de Fin",
        required=True,
        help="Fecha de fin",
        
    )    
    
    days = fields.Integer(
        string="Duracion (dias)",
        readonly=True,
        compute="_compute_days",
        help="Dias de duracion de la campaña",
    )
    
    @api.depends("start_date","end_date")
    def _compute_days(self):
        for record in self:
            if record.start_date and record.end_date:
                delta = record.end_date - record.start_date
                record.days = delta.days
            else:
                record.days = 0
    
    discount = fields.Float(
        string="Descuento",
        required=True,
        help="Descuento",
    )

    description = fields.Text(
        string="Descripción",
        required=False,
        help="Descripción de la campaña como texto libre",
    )
    
    company_id = fields.Many2one(
        string="Empresa",
        comodel_name="res.company",
        required=True,
        readonly=True,
        help="Empresa",
        default=lambda self: self.env.company
    )
    

    # just one campaign active at a time
    
    @api.constrains("status")
    def _check_unique_active_campaign(self):
        for record in self:
            if record.status:
                active_campaign = self.search(
                    [("status", "=", 'active'), ("id", "!=", record.id)], limit=1
                )
                if active_campaign:
                    raise ValidationError(
                        _("Ya existe una campaña activa. Debes finalizarla antes de crear una nueva.")
                    )
                    
    @api.constrains("discount","status")
    def _check_discount_is_positive(self):
        for record in self:
            if record.discount < 0.01 or record.discount > 0.9:
                raise ValidationError(
                    _("El descuento debe estar entre 1 % y 90 %.")
                )
                
    def _cron_close_expired_campaigns(self):
        today = date.today()
        campaign = self.search([
            ("status", "=", "active"),
            ("end_date", "<", today)
        ],limit=1)
        
        if campaign:
            campaign.action_end_campaign()