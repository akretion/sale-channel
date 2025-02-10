# Copyright 2022 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


import json
import traceback

from psycopg2 import OperationalError

import odoo
from odoo import api, fields, models
from odoo.service.model import PG_CONCURRENCY_ERRORS_TO_RETRY

from odoo.addons.queue_job.exception import RetryableJobError


class SaleImportPayload(models.Model):
    _name = "sale.import.payload"
    _description = "Receive and Store payload to create sale orders"
    _order = "id desc"

    data_str = fields.Text(string="Editable data")
    state = fields.Selection(
        [("pending", "Pending"), ("done", "Done"), ("fail", "Failed")],
        default="pending",
        readonly=True,
    )
    state_info = fields.Text("Additional state information", readonly=True)
    sale_channel_id = fields.Many2one(
        "sale.channel",
        readonly=True,
    )
    company_id = fields.Many2one(
        "res.company",
        related="sale_channel_id.company_id",
        store=True,
    )
    stack_trace = fields.Text(readonly=True)

    @api.model_create_multi
    def create(self, vals):
        result = super().create(vals)
        for rec in result:
            rec.enqueue_job()
        return result

    def button_retry(self):
        self.enqueue_job()

    def enqueue_job(self):
        # by pass job for easier debugging
        # will be True if odoo is started with option --dev=pdb
        if "pdb" in odoo.tools.config.get("dev_mode"):
            return self.process()
        else:
            return self.with_delay().process()

    def _get_data(self):
        return json.loads(self.data_str)

    def _get_importer(self):
        self.ensure_one()
        return self.env["sale.channel.importer"].new({"payload_id": self.id})

    def process(self):
        self.ensure_one()
        try:
            with self.env.cr.savepoint():
                importer = self._get_importer()
                result = importer.run()
        except RetryableJobError:
            raise
        except Exception as e:
            # will be True if odoo is started with option --dev=pdb
            if "pdb" in odoo.tools.config.get("dev_mode"):
                raise
            # TODO maybe it will be simplier to have a kind of inherits
            #  on queue.job to avoid a double error management
            # so a failling chunk will have a failling job
            if (
                isinstance(e, OperationalError)
                and e.pgcode in PG_CONCURRENCY_ERRORS_TO_RETRY
            ):
                # In that case we raise an error so queue_job
                # will do a RetryableJobError
                raise
            self.state = "fail"
            self.state_info = type(e).__name__ + str(e.args)
            self.stack_trace = traceback.format_exc()
            return False
        self.state_info = ""
        self.state = "done"
        return result
