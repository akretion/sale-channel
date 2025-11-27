#  Copyright (c) Akretion 2020
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import exceptions, fields, models


class SaleChannel(models.Model):
    _inherit = "sale.channel"

    sale_import_file_format = fields.Selection([], string="File Import Format")

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
        # sale import payload creation does create a job that will process it and
        # create the sale order. Error management is on sale import payload side now
        # TODO we should allow a mode to do everything synchronously, in case of
        # manual update...
        self.env["sale.import.payload"].create(sale_payload_vals_list)

    def _get_sale_payload_vals_list(self, base64file, fileformat):
        "Override this method to implement the parsing of the file"
        return NotImplementedError
