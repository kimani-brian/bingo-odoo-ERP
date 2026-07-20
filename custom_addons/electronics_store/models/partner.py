from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    customer_since = fields.Date(
        string="Customer Since",
        default=fields.Date.today,
    )

    national_id = fields.Char(
        string="National ID",
    )

    preferred_payment_method = fields.Selection(
        [
            ("cash", "Cash"),
            ("mpesa", "M-Pesa"),
            ("card", "Card"),
            ("bank", "Bank Transfer"),
        ],
        string="Preferred Payment Method",
        default="mpesa",
    )

    vip_customer = fields.Boolean(
        string="VIP Customer",
        default=False,
    )

    loyalty_points = fields.Integer(
        string="Loyalty Points",
        default=0,
        readonly=True,
    )