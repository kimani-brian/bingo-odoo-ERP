
from odoo import _, fields, models, api
from odoo.exceptions import UserError

class ElectronicsInstallment(models.Model):
    _name = "electronics.installment"
    _description = "Electronics Store Installment"
    _order = "sequence"

    name = fields.Char(
        string="Reference",
        required=True,
    )

    sequence = fields.Integer(
        string="Sequence",
        default=1,
    )

    installment_type = fields.Selection(
        [
            ("deposit", "Deposit"),
            ("regular", "Regular Installment"),
        ],
        string="Installment Type",
        required=True,
        default="regular",
    )

    sale_order_id = fields.Many2one(
        "sale.order",
        string="Sales Order",
        required=True,
        ondelete="cascade",
    )

    customer_id = fields.Many2one(
        "res.partner",
        string="Customer",
        related="sale_order_id.partner_id",
        store=True,
        readonly=True,
    )

    invoice_id = fields.Many2one(
        "account.move",
        string="Invoice",
        readonly=True,
    )

    payment_id = fields.Many2one(
        "account.payment",
        string="Payment",
        readonly=True,
    )

    original_balance = fields.Float(
        string="Original Balance",
        readonly=True,
    )

    amount = fields.Float(
        string="Installment Amount",
        required=True,
    )

    remaining_balance = fields.Float(
        string="Remaining Balance",
        readonly=True,
    )

    due_date = fields.Date(
        string="Due Date",
        required=True,
    )

    payment_date = fields.Date(
        string="Payment Date",
        readonly=True,
    )

    state = fields.Selection(
        [
            ("pending", "Pending"),
            ("invoiced", "Invoiced"),
            ("paid", "Paid"),
            ("overdue", "Overdue"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="pending",
        required=True,
    )

    notes = fields.Text(
        string="Notes",
    )

    def _generate_invoice(self):
        self.ensure_one()

        if self.invoice_id:
            return self.invoice_id

        invoice = self.env["account.move"].create({
            "move_type": "out_invoice",
            "partner_id": self.customer_id.id,
            "invoice_origin": self.sale_order_id.name,
            "invoice_line_ids": [
                (0, 0, {
                    "name": self.name,
                    "quantity": 1,
                    "price_unit": self.amount,
                })
            ],
        })

        self.write({
            "invoice_id": invoice.id,
            "state": "invoiced",
        })

        return invoice


    def action_generate_invoice(self):
        self.ensure_one()

        invoice = self._generate_invoice()

        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "res_id": invoice.id,
            "view_mode": "form",
            "target": "current",
        }
    
    @api.model
    def cron_generate_due_invoices(self):
        today = fields.Date.today()
        installments = self.search([
            ("due_date", "=", today),
            ("invoice_id", "=", False),
            ("state", "=", "pending"),
        ])
        for installment in installments:
            installment._generate_invoice()

    @api.model
    def cron_sync_paid_installments(self):

        installments = self.search([
            ("invoice_id", "!=", False),
            ("state", "=", "invoiced"),
        ])

        for installment in installments:

            if installment.invoice_id.payment_state == "paid":

                installment.write({

                    "state": "paid",

                    "payment_date": fields.Date.today(),

                    "remaining_balance": 0,

                })