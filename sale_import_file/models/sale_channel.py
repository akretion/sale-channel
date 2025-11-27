#  Copyright (c) Akretion 2020
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import exceptions, fields, models


class SaleChannel(models.Model):
    _inherit = "sale.channel"

    sale_import_file_format = fields.Selection([], string="File Import Format")

    def _get_payload_action(self, sale_payloads):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "sale_import_base.action_sale_import_payload"
        )
        if len(sale_payloads) > 1:
            action["domain"] = [("id", "in", sale_payloads.ids)]
        elif sale_payloads:
            form_view = [
                (
                    self.env.ref("sale_import_base.view_sale_import_payload_form").id,
                    "form",
                )
            ]
            if "views" in action:
                action["views"] = form_view + [
                    (state, view) for state, view in action["views"] if view != "form"
                ]
            else:
                action["views"] = form_view
            action["res_id"] = sale_payloads.id
        return action

    def _get_sale_action(self, sale_payloads):
        action = self.env["ir.actions.actions"]._for_xml_id("sale.action_quotations")
        sale_orders = sale_payloads.sale_order_id
        if len(sale_orders) > 1:
            action["domain"] = [("id", "in", sale_orders.ids)]
        elif sale_orders:
            form_view = [
                (
                    self.env.ref("sale.view_order_form").id,
                    "form",
                )
            ]
            if "views" in action:
                action["views"] = form_view + [
                    (state, view) for state, view in action["views"] if view != "form"
                ]
            else:
                action["views"] = form_view
            action["res_id"] = sale_orders.id
        return action

    def import_sale_order_file(self, base64file, file_format=None):
        """
        self can be empty or an singlton. If not set, channel should be deduced
        from the file and the file format is mandatory
        """
        if not file_format:
            file_format = self.sale_import_file_format
        if not file_format:
            raise exceptions.UserError(
                self.env._("No file format specified, impossible to run the import")
            )
        sale_payload_vals_list = self._get_sale_payload_vals_list(
            base64file, file_format
        )
        sale_payloads = self.env["sale.import.payload"].create(sale_payload_vals_list)
        if self.env.context.get("sale_import_no_delay"):
            return self._get_sale_action(sale_payloads)
        else:
            return self._get_payload_action(sale_payloads)

    def _get_sale_payload_vals_list(self, base64file, fileformat):
        "Override this method to implement the parsing of the file"
        return NotImplementedError
