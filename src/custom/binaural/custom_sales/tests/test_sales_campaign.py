from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import date, timedelta


class TestPromotionCampaign(TransactionCase):

    def setUp(self):
        super().setUp()
        # Crear productos de prueba
        self.product_1 = self.env["product.template"].create({
            "name": "Producto Campaña 1",
            "list_price": 100.0,
            "available_for_campaign": True,
            "sale_ok": True,
        })

        self.product_2 = self.env["product.template"].create({
            "name": "Producto Campaña 2",
            "list_price": 200.0,
            "available_for_campaign": True,
            "sale_ok": True,
        })

        self.product_no_campaign = self.env["product.template"].create({
            "name": "Producto fuera campaña",
            "list_price": 300.0,
            "available_for_campaign": False,
            "sale_ok": True,
        })

        today = date.today()
        self.campaign = self.env["promotion.campaign"].create({
            "name": "Campaña Test",
            "start_date": today,
            "end_date": today + timedelta(days=7),
            "discount": 0.2,  # 20% de descuento
            "status": "draft",
            "company_id": self.env.company.id,
        })

    def test_start_campaign_updates_prices(self):
        """Al iniciar la campaña, los productos marcados deben ajustar sus precios"""
        self.campaign.action_start_campaign()
        self.assertEqual(self.campaign.status, "active")

        # Producto en campaña con descuento aplicado
        self.assertEqual(self.product_1.original_price, 100.0)
        self.assertEqual(self.product_1.list_price, 80.0)  # 100 - 20%

        # Otro producto en campaña
        self.assertEqual(self.product_2.original_price, 200.0)
        self.assertEqual(self.product_2.list_price, 160.0)  # 200 - 20%

        # Producto fuera de campaña no cambia
        self.assertEqual(self.product_no_campaign.list_price, 300.0)
        self.assertEqual(self.product_no_campaign.original_price, 0.0)

    def test_end_campaign_restores_prices(self):
        """Al finalizar la campaña, los precios deben volver al original"""
        self.campaign.action_start_campaign()
        self.campaign.action_end_campaign()

        self.assertEqual(self.campaign.status, "end")

        self.assertEqual(self.product_1.list_price, 100.0)

        self.assertEqual(self.product_2.list_price, 200.0)

    def test_unique_active_campaign(self):
        """No debe permitir más de una campaña activa"""
        self.campaign.action_start_campaign()

        # Intentar crear una segunda campaña activa debería fallar
        with self.assertRaises(ValidationError):
            self.env["promotion.campaign"].create({
                "name": "Segunda Campaña",
                "start_date": date.today(),
                "end_date": date.today() + timedelta(days=5),
                "discount": 0.1,
                "status": "active",  # Aquí forzamos el error de constraint
                "company_id": self.env.company.id,
            })

    def test_discount_constraints(self):
        """El descuento debe estar entre 1% y 90%"""
        with self.assertRaises(ValidationError):
            self.campaign.write({"discount": 0})

        with self.assertRaises(ValidationError):
            self.campaign.write({"discount": 1.0})
