#  Copyright (c) Akretion 2025
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import fields, models


class SaleChannel(models.Model):
    _inherit = "sale.channel"

    route_id = fields.Many2one(
        "stock.route",
        string="Route",
        domain=[("sale_selectable", "=", True)],
        ondelete="restrict",
        check_company=True,
    )
