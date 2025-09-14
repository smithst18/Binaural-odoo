from odoo import models, fields, api

class ConsolidacionPaqueteWizard(models.TransientModel):
  
    _name = "consolidate.package.wizard"
    _description = "Wizard para Consolidacion de Paquetes"
    
    picking_id = fields.Many2one("stock.picking", string="Picking")

    package_types = fields.Many2many(
        "stock.package.type", string="Tipos de Paquete a utilizar"
    )
    
    consolidation_line_ids = fields.One2many(
        "consolidate.package.line.wizard",
        "wizard_id",
        string="Vista previa de consolidación",
    )
    
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list) or {}
        
        picking = self.env['stock.picking'].browse(self._context.get('active_id'))
        
        if picking:
            res["picking_id"] = picking.id

            groups = picking.get_package_types() or {}
            res['package_types'] = [(6, 0, [g.id for g in groups.keys()])]

            lines = []
            for package_type, moves in groups.items():
                for move in moves:
                    product = move.product_id
                    total_qty = move.product_uom_qty
                    # Calculamos peso y volumen total
                    total_weight = product.weight * total_qty
                    total_volume = product.volume * total_qty

                    lines.append((0, 0, {
                        'product_id': product.id,
                        'package_type_id': package_type.id,
                        'weight': total_weight,
                        'volume': total_volume,
                        'quantity': total_qty,
                    }))

            res['consolidation_line_ids'] = lines

        return res

    def action_consolidate(self):
      self.ensure_one()
      if not self.picking_id:
          raise UserError("No se ha seleccionado un picking.")


      self.picking_id.action_consolidate_packages()


      self.picking_id.package_consolidation = True

      
class ConsolidacionPaqueteLineWizard(models.TransientModel):
    _name = "consolidate.package.line.wizard"
    _description = "Líneas de vista previa para consolidación"

    wizard_id = fields.Many2one("consolidate.package.wizard", required=True, ondelete="cascade")
    product_id = fields.Many2one("product.product", string="Producto")
    package_type_id = fields.Many2one("stock.package.type", string="Tipo de Paquete")
    weight = fields.Float("Peso Total")
    volume = fields.Float("Volumen Total")
    quantity = fields.Float("Cantidad")