{
    "name": "custom_point_of_sale",
    "version": "16.0.1.0.0",
    "summary": "Módulo que incluye funcionalidades para Point of Sales",
    "description": "Prueba Técnica - Módulo Custom Point of Sales",
    "author": "E.A.A",
    "website": "https://www.odoo.com",
    "category": "point of sale",
    "depends": [
        "base",
        "point_of_sale",
    ],
    "data": [
        # security
        # "security/security.xml",
        "security/admin/ir.model.access.csv",
        "security/ir.model.access.csv",
        # data
        #cron
        # views
        "views/custom_pos_session.xml",
        "views/pos_session_resume.xml",
    ],  
    "tests": [
        "tests/test_pos_resume.py",
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