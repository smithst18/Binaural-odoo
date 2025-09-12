# -*- coding: utf-8 -*-
{
    "name": "custom_contability",
    "version": "16.0.1.0.0",
    "summary": "Módulo que incluye funcionalidades para Contabilidad",
    "description": "Prueba Técnica - Módulo Custom Contabilidad",
    "author": "E.A.A",
    "website": "https://www.odoo.com",
    "category": "Accounting",
    "depends": [
        "base",
        "account",
    ],
    "data": [
        # security
        # "security/security.xml",
        "security/admin/ir.model.access.csv",
        "security/ir.model.access.csv",
        # data
        # views
        "views/custom_account.xml",
        "views/res_config_setting.xml",
    ],
    "demo": [
    ],
    # 'tests': [
    #     'tests/test_account_payment.py',
    # ],
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