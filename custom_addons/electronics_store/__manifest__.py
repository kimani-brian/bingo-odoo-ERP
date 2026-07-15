{
    "name": "Electronics Store",
    "version": "19.0.1.0.0",
    "summary": "Electronics Store Management",
    "description": """
Electronics Store ERP

This module extends Odoo to manage
electronics products, brands,
warranty plans and future sales features.
""",
    "author": "Brian Kimani",
    "website": "https://github.com/kimani-brian",
    "category": "Sales",
    "license": "LGPL-3",
    "depends": [
        "base",
        "product",
        "stock",
        "sale",
        
    ],
    "data": [

        "security/security.xml",
        "security/ir.model.access.csv",

        "views/product_brand_views.xml",
        "views/product_brand_actions.xml",

        "views/warranty_plan_views.xml",
        "views/warranty_plan_actions.xml",

        "views/product_template_views.xml",

        "views/partner_views.xml",
        "views/sale_order_views.xml",

        "views/menus.xml",

    ],
    "demo": [],
    "installable": True,
    "application": True,
}