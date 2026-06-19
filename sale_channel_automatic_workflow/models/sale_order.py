#  Copyright (c) Akretion 2020
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    workflow_process_id = fields.Many2one(
        compute="_compute_workflow_process_id",
        store=True,
        readonly=False,
        precompute=True,
    )

    @api.depends("sale_channel_id")
    def _compute_workflow_process_id(self):
        for sale in self:
            if sale.sale_channel_id.workflow_process_id:
                sale.workflow_process_id = sale.sale_channel_id.workflow_process_id
