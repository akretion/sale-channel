#  License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import fields, models


class SaleChannel(models.Model):
    _inherit = "sale.channel"

    workflow_process_id = fields.Many2one(
        "sale.workflow.process",
        string="Automatic Workflow",
        help="If set, the automatic workflow will be set on sale order belonging to "
        "this channel",
    )
