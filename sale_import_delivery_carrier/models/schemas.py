# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from pydantic import BaseModel
from extendable_pydantic import ExtendableModelMeta
from odoo.addons.sale_import_base.models.schemas import SaleOrder


class Carrier(BaseModel, metaclass=ExtendableModelMeta):
    code: str
    price_unit: float

class ExtendedSaleOrder(SaleOrder, extends=SaleOrder):
    delivery_carrier: Carrier | None = None


