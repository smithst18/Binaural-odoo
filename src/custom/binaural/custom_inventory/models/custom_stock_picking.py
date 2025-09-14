from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import date

class CustomInheritStockPicking(models.Model):
  
    _inherit = "stock.picking"
    _description = "Modelo Heredado para stock.picking"
    
    package_consolidation = fields.Boolean(
        string="Consolidacion de Paquetes",
        default=False,
        help="Determina si se realizara la consolidacion de paquetes",
    )
    
    def get_package_types(self):
        grupos = {}
        for move in self.move_ids_without_package:
            tipo_paquete = move.product_id.package_type_id
            if tipo_paquete:
                grupos.setdefault(tipo_paquete, []).append(move)
        return grupos
      
    def action_consolidate_packages(self):
        self.ensure_one()
        moves_by_type = self.get_package_types()

        for package_type, moves in moves_by_type.items():
            # Obtener move lines; si no existen, crearlas
            move_lines = self.move_line_ids.filtered(lambda ml: ml.move_id in moves)
            if not move_lines:
                move_lines = self.env['stock.move.line'].create([
                    {
                        'move_id': move.id,
                        'product_id': move.product_id.id,
                        'product_uom_id': move.product_uom.id,
                        'qty_done': move.product_uom_qty,
                        'location_id': move.location_id.id,
                        'picking_id': self.id,
                    }
                    for move in moves
                ])

            # Construir nombre del paquete
            package_name = f"{package_type.name} - {self.name}"

            # Buscar paquete existente
            package = self.env['stock.quant.package'].search([
                ('package_type_id', '=', package_type.id),
                ('name', '=', package_name)
            ], limit=1)

            if not package:
                # Crear paquete si no existe
                package = self.env['stock.quant.package'].create({
                    'package_type_id': package_type.id,
                    'name': package_name,
                    'location_id': move_lines[0].location_id.id,
                    'company_id': self.company_id.id,
                })

            # Asignar move lines al paquete
            move_lines.write({'result_package_id': package.id})

        # Marcar consolidación realizada
        self.package_consolidation = True
