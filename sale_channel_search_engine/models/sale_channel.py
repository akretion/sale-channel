# Copyright 2022 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleChannel(models.Model):
    _inherit = "sale.channel"

    _sql_constraints = [
        ("se_uniq", "unique (search_engine_id)", "Only one backend per search engine")
    ]

    search_engine_id = fields.Many2one("se.backend", "Search Engine")
