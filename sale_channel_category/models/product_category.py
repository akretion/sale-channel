# Copyright 2021 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductCategory(models.Model):
    _inherit = ["product.category", "sale.channel.owner"]
    _name = "product.category"

    channel_ids = fields.Many2many(
        "sale.channel",
        string="Sale Channel",
        store=True,
        compute="_compute_channel_ids",
        readonly=False,
    )

    @api.depends("channel_ids", "parent_id")
    def _compute_channel_ids(self):
        for record in self:
            if not record.parent_id:
                record._propagate_channel_ids()

    def _propagate_channel_ids(self):
        for record in self:
            children = record.child_id
            if children:
                children.write({"channel_ids": record.channel_ids})
                children._propagate_channel_ids()
