from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import UserError, ValidationError


class TestAccountPaymentDoubleValidation(TransactionCase):

    def setUp(self):
        super().setUp()

        # Partner de prueba
        self.partner = self.env['res.partner'].create({
            'name': 'Partner de prueba',
        })

        # Crear usuarios específicos para los tests
        group_account_manager = self.env.ref("account.group_account_manager")
        group_user = self.env.ref("base.group_user")

        self.user_account_manager = self.env['res.users'].create({
            'name': 'Account Manager User',
            'login': 'manager_user',
            'groups_id': [(6, 0, [group_account_manager.id, group_user.id])]
        })

        self.user_regular = self.env['res.users'].create({
            'name': 'Regular User',
            'login': 'regular_user',
            'groups_id': [(6, 0, [group_user.id])]
        })

        # Configuración inicial
        self.env['ir.config_parameter'].sudo().set_param('custom_contability.double_validation', True)
        self.env['ir.config_parameter'].sudo().set_param('custom_contability.double_validation_limit', 50000.0)

        # Crear pagos
        self.payment_under_limit = self.env['account.payment'].create({
            'amount': 1000.0,
            'payment_type': 'outbound',
            'partner_type': 'supplier',
            'partner_id': self.partner.id,
        })

        self.payment_over_limit = self.env['account.payment'].create({
            'amount': 60000.0,
            'payment_type': 'outbound',
            'partner_type': 'supplier',
            'partner_id': self.partner.id,
        })

    def test_payment_without_double_validation_under_limit(self):
        # Prueba pago sin doble validación, monto menor al límite
        # Desactivar doble validación para esta prueba
        self.env['ir.config_parameter'].sudo().set_param('custom_contability.double_validation', False)

        self.payment_under_limit.action_post()  # No debería fallar
        self.assertEqual(self.payment_under_limit.state, 'posted')

    def test_payment_with_double_validation_over_limit_error(self):
        # Prueba que se levante error al intentar postear un pago sobre el límite sin aprobación
        with self.assertRaises(UserError) as e:
            self.payment_over_limit.action_post()
        self.assertIn('Límite de pago excedido', str(e.exception))

    def test_approve_payment_by_account_manager(self):
        # Prueba aprobar pago por un usuario con permisos y luego postear
        self.payment_over_limit.with_user(self.user_account_manager).action_approve_payment()
        self.assertTrue(self.payment_over_limit.double_validation_approved)
        self.assertEqual(self.payment_over_limit.approved_by, self.user_account_manager)

        # Ahora debería permitir postear
        self.payment_over_limit.action_post()
        self.assertEqual(self.payment_over_limit.state, 'posted')

    def test_regular_user_cannot_approve_payment(self):
        # Un usuario sin permisos no puede aprobar el pago
        with self.assertRaises(UserError) as e:
            self.payment_over_limit.with_user(self.user_regular).action_approve_payment()
        self.assertIn('No tienes permisos para aprobar este pago', str(e.exception))

    def test_config_limit_validation(self):
        # Prueba que lanzar error si doble validación está activa y límite <= 0
        self.env['ir.config_parameter'].sudo().set_param('custom_contability.double_validation', True)
        self.env['ir.config_parameter'].sudo().set_param('custom_contability.double_validation_limit', 0)

        with self.assertRaises(ValidationError) as e:
            self.env['res.config.settings'].create({})
        self.assertIn(
            'El límite para la doble validación de pagos debe ser mayor a 0',
            str(e.exception)
        )
