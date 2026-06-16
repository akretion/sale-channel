# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo.addons.sale_import_base.models.schemas import SaleOrder


class ExtendedSaleOrder(SaleOrder, extends=SaleOrder):
    warehouse: str | None = None
