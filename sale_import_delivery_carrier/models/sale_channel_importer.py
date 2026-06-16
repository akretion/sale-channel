#  License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)
from odoo import models
from odoo.exceptions import ValidationError


class SaleChannelImporter(models.TransientModel):
    _inherit = "sale.channel.importer"

    def _finalize(self, new_sale_order, raw_import_data):
        if raw_import_data.get("delivery_carrier"):
            carrier = self.env["delivery.carrier"].search(
                [("code", "=", raw_import_data["delivery_carrier"]["code"])]
            )
            if not carrier:
                raise ValidationError(
                    self.env._("Couldn't find a carrier with given code")
                )
            new_sale_order.set_delivery_line(
                carrier, raw_import_data["delivery_carrier"]["price_unit"]
            )
        return super()._finalize(new_sale_order, raw_import_data)
