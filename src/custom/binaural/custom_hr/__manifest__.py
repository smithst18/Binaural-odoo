# -*- coding: utf-8 -*-
{
    "name": "custom_hr",
    "version": "16.0.1.0.0",
    "summary": "Módulo que incluye funcionalidades para Hr",
    "description": "Prueba Técnica - Módulo Custom Hr",
    "author": "E.A.A",
    "website": "https://www.odoo.com",
    "category": "Hr",
    "depends": [
        "base",
        "hr",
        "hr_holidays"
    ],
    "data": [
        # security
        # "security/security.xml",
        "security/admin/ir.model.access.csv",
        "security/ir.model.access.csv",
        # data
        "data/hr_absence_reason.xml",
        # views
        "views/custom_hr_leave.xml",
        "views/hr_absence_reason.xml",
        "views/menu.xml",
    ],  
    "demo": [
    ],
    'tests': [
        "tests/test_absense_reason.py",
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