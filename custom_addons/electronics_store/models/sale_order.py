from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    payment_type = fields.Selection(
        [
            ("full", "Full Payment"),
            ("installment", "Installment"),
        ],
        string="Payment Type",
        default="full",
        required=True,
    )

    deposit_amount = fields.Float(
        string="Deposit Amount",
        default=0.0,
    )

    warranty_generated = fields.Boolean(
        string="Warranty Generated",
        default=False,
        readonly=True,
    )

    sales_notes = fields.Text(
        string="Sales Notes",
    )