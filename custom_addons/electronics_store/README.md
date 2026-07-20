# Electronics Store

Odoo 19 module for managing an electronics store — brands, warranty plans, and sales features.

## Author

Brian Kimani

## Dependencies

- base
- product
- stock
- sale
- account

## Custom Models

| Model | Description |
|---|---|
| `electronics.product.brand` | Product brands (name, logo, website, description) |
| `electronics.warranty.plan` | Warranty plans (duration, unit, description) |
| `electronics.installment` | Sales installments with auto invoice generation |

## Extended Models

| Model | Added Fields |
|---|---|
| `product.template` | brand_id, warranty_plan_id, model_number, serial_required |
| `res.partner` | customer_since, national_id, preferred_payment_method, vip_customer, loyalty_points |
| `sale.order` | payment_type, deposit_amount, installment_count, warranty_generated, sales_notes, installment_ids |

## Installments

When a sale order with payment type "Installment" is confirmed, the system automatically creates:
- A deposit installment (immediately marked as paid if deposit > 0)
- Regular installment records spread 30 days apart

Installments can be invoiced individually via the "Generate Invoice" button on the installment form.

### Cron Job

| Name | Interval | Description |
|---|---|---|
| Generate Invoices for Due Installments | Daily | Automatically creates invoices for pending installments whose due date is today |

## Security Groups

| Group | Implied Groups | Access Level |
|---|---|---|
| Administrator | Sales / User, Inventory / User | Full CRUD on all models |
| Sales Officer | Sales / User, Inventory / User | Full CRUD on installments, read-only on brands/warranty |
| Inventory Officer | Sales / User, Inventory / User | Read-only on installments, full CRUD on brands/warranty |

Implied groups mean users assigned to any of these groups automatically inherit the standard Sales and Inventory access, so they see both the Electronics Store app and the standard Sales/Inventory apps.

## Menu Structure

```
Electronics Store
├── Configuration  (Admin, Inventory)
│   ├── Brands
│   └── Warranty Plans
├── Sales  (Sales Officer)
│   ├── Brands
│   └── Warranty Plans
└── Installments  (Admin, Sales Officer)
```

## Access Rights

| Model | Admin | Sales Officer | Inventory Officer |
|---|---|---|---|
| `electronics.product.brand` | Full CRUD | Read-only | Full CRUD |
| `electronics.warranty.plan` | Full CRUD | Read-only | Full CRUD |
| `electronics.installment` | Full CRUD | Full CRUD (no unlink) | Read-only |
