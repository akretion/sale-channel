#  License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import api, fields, models


class SaleChannelImportFile(models.TransientModel):
    _inherit = "sale.channel.import.file"

    @api.model
    def _get_selection_import_file_format(self):
        return self.env["sale.channel"].fields_get(
            allfields=["sale_import_file_format"]
        )["sale_import_file_format"]["selection"]

    import_file_format = fields.Selection(
        selection="_get_selection_import_file_format",
        compute="_compute_import_file_format",
        store=True,
        readonly=False,
    )
    sale_channel_id = fields.Many2one("sale.channel", required=True)
    file_content = fields.Binary(string="File")

    @api.depends("sale_channel_id")
    def _compute_import_file_format(self):
        for rec in self:
            if rec.sale_channel_id.import_file_format:
                rec.import_file_format = rec.sale_channel_id.import_file_format

    def run(self):
        self.sale_channel_id.import_sale_order_file(
            self.file_content, file_format=self.import_file_format
        )
