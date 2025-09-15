from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import date

class CustomInheritPossSession(models.Model):
  
    _inherit = "pos.session"
    _description = "Modelo Heredado para POS SESSION"
    
    resume_id = fields.Many2one(
        'pos.session_resume',
        string='Resumen de Sesión',
        help='Resumen automático generado para esta sesión'
    )
    
    
    def action_view_resume(self):
        self.ensure_one()
          
        return {
            'name': _("Resumen de Turno POS"),
            'type': 'ir.actions.act_window',
            'res_model': 'pos.session_resume',
            'view_mode': 'form',
            'views': [
                (self.env.ref('point_of_sales.poss_session_resume_form_view').id, 'form'),
            ],
            'res_id': self.resume_id.id,
            'target': 'current',
        }
        
    def action_pos_session_close(self, balancing_account=False, amount_to_balance=0, bank_payment_method_diffs=None):
        self.ensure_one()

        # Ejecutar cierre normal
        res = super(CustomInheritPossSession, self).action_pos_session_close(
            balancing_account, amount_to_balance, bank_payment_method_diffs
        )

        # Evitar crear duplicados
        if self.env['pos.session_resume'].search_count([('pos_session_id', '=', self.id)]) > 0:
            return res

        # Duración de la sesión en horas
        session_duration_hours = (self.stop_at - self.start_at).total_seconds() / 3600.0

        # Total ventas
        orders = self.order_ids
        total_sales = sum(orders.mapped('amount_total'))

        # Total de transacciones
        transactions_count = len(self.order_ids)

        # Total de productos vendidos
        total_products_amount = sum(line.qty for line in self.order_ids.mapped('lines'))

        # Top 3 productos por nombre
        product_counts = {}
        for line in self.order_ids.mapped('lines'):
            template = line.product_id.product_tmpl_id
            if template in product_counts:
                product_counts[template] += line.qty
            else:
                product_counts[template] = line.qty

        # Top 3 productos
        top_3_products = sorted(product_counts.items(), key=lambda x: x[1], reverse=True)[:3]

        # Crear resumen
        session_resume = self.env['pos.session_resume'].create({
            'pos_session_id': self.id,
            'sesion_duration': session_duration_hours,
            'total_sales': total_sales,
            'transactions_count': transactions_count,
            'total_products_amount': total_products_amount,
        })

        top_product_obj = self.env['pos.top_product']
        
        top_product_ids = []
        
        for template, qty in top_3_products:
            top_product = top_product_obj.create({
                'pos_session_resume_id': session_resume.id,
                'product_id': template.id, 
                'quantity': qty,
            })
            top_product_ids.append(top_product.id)

        # Asignar top_product_ids al resumen
        session_resume.top_product_ids = [(6, 0, top_product_ids)]

        # Guardar referencia en la sesión
        self.resume_id = session_resume

        return res