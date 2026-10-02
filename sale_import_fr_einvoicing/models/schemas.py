# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo.addons.sale_import_base.models.schemas import Customer, SaleOrder


class ExtendedSaleOrder(SaleOrder, extends=SaleOrder):
    directory_line_name: str | None = None


class EinvoicingCustomer(Customer, extends=Customer):
    directory_line_name: str | None = None
    siret: str | None = None
