from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import UserError

@tagged('consolidate_packages')
class TestConsolidatePackages(TransactionCase):

    def setUp(self):
        super().setUp()

        # Crear tipos de paquete
        self.package_type_1 = self.env['stock.package.type'].create({'name': 'Caja'})
        self.package_type_2 = self.env['stock.package.type'].create({'name': 'Bolsa'})

        # Crear productos
        self.product_1 = self.env['product.product'].create({
            'name': 'Producto A',
            'type': 'product',
            'uom_id': self.env.ref('uom.product_uom_unit').id,
            'package_type_id': self.package_type_1.id,
        })
        self.product_2 = self.env['product.product'].create({
            'name': 'Producto B',
            'type': 'product',
            'uom_id': self.env.ref('uom.product_uom_unit').id,
            'package_type_id': self.package_type_2.id,
        })

        # Crear picking
        self.picking = self.env['stock.picking'].create({
            'picking_type_id': self.env.ref('stock.picking_type_out').id,
            'location_id': self.env.ref('stock.stock_location_stock').id,
            'location_dest_id': self.env.ref('stock.stock_location_customers').id,
        })

        # Crear movimientos
        self.move_1 = self.env['stock.move'].create({
            'name': 'Move 1',
            'product_id': self.product_1.id,
            'product_uom_qty': 5,
            'product_uom': self.product_1.uom_id.id,
            'picking_id': self.picking.id,
            'location_id': self.picking.location_id.id,
            'location_dest_id': self.picking.location_dest_id.id,
        })
        self.move_2 = self.env['stock.move'].create({
            'name': 'Move 2',
            'product_id': self.product_2.id,
            'product_uom_qty': 3,
            'product_uom': self.product_2.uom_id.id,
            'picking_id': self.picking.id,
            'location_id': self.picking.location_id.id,
            'location_dest_id': self.picking.location_dest_id.id,
        })

        # Confirmar y asignar picking (Odoo 16)
        self.picking.action_confirm()
        self.picking.action_assign()

    def test_grouping_by_package_type(self):
        """Verifica que los movimientos se asignan correctamente a los paquetes por tipo."""

        # Ejecutar consolidación
        self.picking.action_consolidate_packages()

        # Recuperar paquetes generados
        packages = self.env['stock.quant.package'].search([('name', 'ilike', self.picking.name)])
        self.assertEqual(len(packages), 2, "Deben crearse dos paquetes, uno por tipo de paquete")

        # Verificar asignación de move lines
        for package in packages:
            move_lines = self.env['stock.move.line'].search([('result_package_id', '=', package.id)])
            package_type_name = package.package_type_id.name
            if package_type_name == 'Caja':
                self.assertTrue(all(ml.product_id.package_type_id == self.package_type_1 for ml in move_lines),
                                "Todos los move lines deben tener tipo de paquete 'Caja'")
            elif package_type_name == 'Bolsa':
                self.assertTrue(all(ml.product_id.package_type_id == self.package_type_2 for ml in move_lines),
                                "Todos los move lines deben tener tipo de paquete 'Bolsa'")
            else:
                self.fail(f"Paquete inesperado creado: {package.name}")
