#  License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)
from odoo import models
from odoo.exceptions import ValidationError


class SaleChannelImporter(models.TransientModel):
    _inherit = "sale.channel.importer"

    def _prepare_sale_vals(self, data):
        vals = super()._prepare_sale_vals(data)
        if data.get("warehouse"):
            wh = self.env["stock.warehouse"].search([("code", "=", data["warehouse"])])
            if not wh:
                raise ValidationError(
                    self.env._("Couldn't find a warehouse with given code")
                )
            vals["warehouse_id"] = wh.id
        return vals
