# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    invalid_siret = fields.Char(help="Store the siret from website if it is invalid")
