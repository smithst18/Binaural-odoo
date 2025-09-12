import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class CustomInheritAccountPayment(models.Model):
  
    _inherit = "account.payment"
    _description = "Campo Heredado para Contabilidad modelo account.payment"
    
    
    double_validation_approved = fields.Boolean(
        string="Aprobado por Finanzas ?",
        default=False,  
        help="Campo Booleano utilizado para validad que el payment esta Aprobado por Finanzas",
        readonly=True
    )
    
    show_double_validation = fields.Boolean(
        string="Mostrar doble validación",
        compute="_compute_show_double_validation"
    )
    
    approved_by = fields.Many2one(
        string="Aprobado por",
        comodel_name="res.users",
        readonly=True
    )
    
    """Get Configuration"""
    @api.model
    def _get_double_validation_config(self):
        double_validation = self.env['ir.config_parameter'].sudo().get_param(
            'custom_contability.double_validation', default=False)
        double_validation_limit = self.env['ir.config_parameter'].sudo().get_param(
            'custom_contability.double_validation_limit', default=50000.0)
        return bool(double_validation), float(double_validation_limit)


    @api.depends('amount')
    def _compute_show_double_validation(self):
        double_validation, limit = self._get_double_validation_config()
        for record in self:
            record.show_double_validation = double_validation and record.amount > limit
            
      
    # Override post method to check if the payment is approved by Finanzas if double validation is enabled
    def action_post(self):
        self.ensure_one()
        double_validation, limit = self._get_double_validation_config()
        if not self.double_validation_approved and double_validation:
            raise UserError(_(f'Límite de pago excedido: {limit}. Es necesaria la validación por Finanzas.'))
            
        return super(CustomInheritAccountPayment, self).action_post()
    
    
    """ This method allows to approve a payment by Finanzas """
    def action_approve_payment(self):
        self.ensure_one()
        if not self.env.user.has_group('account.group_account_manager'):
            raise UserError(_('No tienes permisos para aprobar este pago.'))
          
        self.double_validation_approved = True
        self.approved_by = self.env.user
            

