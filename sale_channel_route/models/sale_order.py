#  Copyright (c) Akretion 2020
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange("sale_channel_id")
    def onchange_sale_channel_route(self):
        default_route = self.sale_channel_id.route_id
        self.order_line.route_id = default_route

    def action_confirm(self):
        for rec in self:
            default_channel_route = rec.sale_channel_id.route_id
            if default_channel_route:
                rec.order_line.filtered(
                    lambda sol: not sol.route_id
                    and sol.qty_delivered_method == "stock_move"
                ).write({"route_id": default_channel_route.id})
        return super().action_confirm()
