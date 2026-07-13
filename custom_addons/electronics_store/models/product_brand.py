from odoo import models, fields


class ProductBrand(models.Model):
    _name = "electronics.product.brand"
    _description = "Product Brand"
    _order = "name"

    name = fields.Char(
        string="Brand Name",
        required=True,
    )

    logo = fields.Binary(
        string="Logo",
        attachment=True,
    )

    website = fields.Char(
        string="Website",
    )

    active = fields.Boolean(
        string="Active",
        default=True,
    )

    description = fields.Text(
        string="Description",
    )