# Copyright 2021 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models

from odoo.addons.queue_job.job import identity_exact


class StockMove(models.Model):
    _inherit = "stock.move"

    def _check_stock_variation(self):
    self.move_lines_ids.product_id.channel_bind_ids._check_stock_variation()

    def _action_cancel(self):
        result = super()._action_cancel()
        self._notify_stock_variation()
        return result

    def _action_confirm(self, merge=True, merge_into=False):
        result = super()._action_confirm(merge=merge, merge_into=merge_into)
        result._notify_stock_variation()
        return result

    def _action_done(self, cancel_backorder=False):
        result = super()._action_done(cancel_backorder=cancel_backorder)
        self._notify_stock_variation()
        return result
