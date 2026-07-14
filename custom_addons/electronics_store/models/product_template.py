from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    brand_id = fields.Many2one(
        "electronics.product.brand",
        string="Brand",
    )

    warranty_plan_id = fields.Many2one(
        "electronics.warranty.plan",
        string="Warranty Plan",
    )

    model_number = fields.Char(
        string="Model Number",
    )

    serial_required = fields.Boolean(
        string="Serial Number Required",
        default=True,
    )