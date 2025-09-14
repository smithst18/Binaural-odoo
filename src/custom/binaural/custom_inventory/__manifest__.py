# -*- coding: utf-8 -*-
{
    "name": "custom_inventory",
    "version": "16.0.1.0.0",
    "summary": "Módulo que incluye funcionalidades para inventario",
    "description": "Prueba Técnica - Módulo Custom inventario",
    "author": "E.A.A",
    "website": "https://www.odoo.com",
    "category": "inventory",
    "depends": [
        "base",
        "stock",
    ],
    "data": [
        # security
        # "security/security.xml",
        "security/admin/ir.model.access.csv",
        "security/ir.model.access.csv",
        # data
        #wizards
        "wizards/consolidate_wizard.xml",
        # views
        "views/custom_product_template.xml",
        "views/custom_stock_picking.xml",
    ],  
    "tests": [
        "tests/test_custom_inventory.py",
    ],
    "demo": [
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