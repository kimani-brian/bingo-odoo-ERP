from odoo import models, fields


class WarrantyPlan(models.Model):
    _name = "electronics.warranty.plan"
    _description = "Warranty Plan"
    _order = "duration"

    name = fields.Char(
        string="Warranty Name",
        required=True,
    )

    duration = fields.Integer(
        string="Duration",
        required=True,
        default=12,
    )

    unit = fields.Selection(
        [
            ("month", "Months"),
            ("year", "Years"),
        ],
        string="Unit",
        default="month",
        required=True,
    )

    description = fields.Text(
        string="Description",
    )

    active = fields.Boolean(
        default=True,
    )