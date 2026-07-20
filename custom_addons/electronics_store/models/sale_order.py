from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    payment_type = fields.Selection(
        [
            ("full", "Full Payment"),
            ("installment", "Installment"),
        ],
        default="full",
        required=True,
    )

    deposit_amount = fields.Float(
        default=0.0,
    )

    installment_count = fields.Integer(
        default=3,
    )

    warranty_generated = fields.Boolean(
        readonly=True,
        default=False,
    )

    sales_notes = fields.Text()
    
    installment_ids = fields.One2many(
        "electronics.installment",
        "sale_order_id",
        string="Installments",
    )

    installment_total = fields.Integer(
        string="Installments",
        compute="_compute_installment_total",
    )

    def action_view_installments(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "Installments",
            "res_model": "electronics.installment",
            "view_mode": "list,form",
            "domain": [("sale_order_id", "=", self.id)],
            "context": {
                "default_sale_order_id": self.id,
            },
        }
    @api.depends("installment_ids")
    def _compute_installment_total(self):

        for order in self:
            order.installment_total = len(order.installment_ids)

    @api.constrains("payment_type", "deposit_amount")
    def _check_installment_deposit(self):

        for order in self:

            if (
                order.payment_type == "installment"
                and order.deposit_amount <= 0
            ):
                raise ValidationError(
                    "Deposit must be greater than zero."
                )

    def action_confirm(self):

        result = super().action_confirm()

        Installment = self.env["electronics.installment"]

        for order in self:

            if order.payment_type != "installment":
                continue

            remaining = (
                order.amount_total
                - order.deposit_amount
            )

            installment_amount = (
                remaining
                / order.installment_count
            )

            Installment.create({

                "name": "Deposit",

                "sale_order_id": order.id,

                "due_date": fields.Date.today(),

                "amount": order.deposit_amount,

                "state": "paid",

            })

            for i in range(order.installment_count):

                Installment.create({

                    "name": f"Installment {i + 1}",

                    "sale_order_id": order.id,

                    "due_date": fields.Date.today()
                    + timedelta(days=(i + 1) * 30),

                    "amount": installment_amount,

                    "state": "pending",

                })

        return result