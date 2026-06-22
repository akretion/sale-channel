#  Copyright (c) Akretion 2020
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, fields, models

SELECTION_INTERNAL_NAMING_METHOD = [
    ("name", "Native"),
    ("client_order_ref", "External identifier"),
]


class SaleChannel(models.Model):
    _inherit = "sale.channel"

    allow_match_on_email = fields.Boolean("Allow customer match on email")
    archive_addresses = fields.Boolean(
        "Automatically archive partner's addresses",
        default=True,
        # default = True to be backward compatible as much as possible
    )
    sale_orders_check_amounts_untaxed = fields.Boolean(
        "(technical) Check untaxed amounts against imported values"
    )
    sale_orders_check_amounts_total = fields.Boolean(
        "(technical) Check total amounts against imported values"
    )
    pricelist_id = fields.Many2one("product.pricelist", string="Pricelist")
    crm_team_id = fields.Many2one("crm.team")
    confirm_order = fields.Boolean(help="Confirm order after import")
    invoice_order = fields.Boolean(help="Generate invoice after import")
    internal_naming_method = fields.Selection(
        SELECTION_INTERNAL_NAMING_METHOD,
        default="client_order_ref",
        help="Sale Orders can use either Odoo native sequenced numbering, "
        "or the external identifier",
    )
    sale_import_payload_ids = fields.One2many(
        "sale.import.payload", "sale_channel_id", string="Sale Imports"
    )
    count_sale_import_payloads = fields.Integer(
        string="Queue Chunks", compute="_compute_count_sale_import_payloads"
    )

    @api.depends("sale_import_payload_ids")
    def _compute_count_sale_import_payloads(self):
        for rec in self:
            rec.count_sale_import_payloads = len(rec.sale_import_payload_ids)

    def button_open_sale_import_payloads(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "sale_import_base.action_sale_import_payload"
        )
        action["domain"] = [("sale_channel_id", "=", self.id)]
        return action
