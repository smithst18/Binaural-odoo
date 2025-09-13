from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import UserError, ValidationError


class TestAbsenseReason(TransactionCase):

    def setUp(self):
        super().setUp()

        