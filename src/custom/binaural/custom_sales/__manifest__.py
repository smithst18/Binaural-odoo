{
    "name": "custom_sales",
    "version": "16.0.1.0.0",
    "summary": "Módulo que incluye funcionalidades para Sales",
    "description": "Prueba Técnica - Módulo Custom Sales",
    "author": "E.A.A",
    "website": "https://www.odoo.com",
    "category": "sales",
    "depends": [
        "base",
        "sale_management",
    ],
    "data": [
        # security
        # "security/security.xml",
        "security/admin/ir.model.access.csv",
        "security/ir.model.access.csv",
        # data
        #cron
        "data/cron_end_campaign.xml",
        # views
        "views/custom_product_template.xml",
        "views/sales_campaign.xml",
        "views/menu.xml",
    ],  
    "demo": [
    ],
    'tests': [
        "tests/test_sales_campaign.py",
    ],  
    "assets": {
    },
    "installable": True,
    "application": False,
    "auto_install": False,
    "license": "AGPL-3",
    "external_dependencies": {
        "python": [],
    },
}