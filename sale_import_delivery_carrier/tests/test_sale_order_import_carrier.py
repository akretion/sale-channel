# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo.tests import tagged

from odoo.addons.extendable_fastapi.tests.common import FastAPITransactionCase
from odoo.addons.sale_import_base.tests.common_sale_order_import import SaleImportCase


@tagged("-at_install", "post_install")
class TestSaleOrderImportDelivery(SaleImportCase, FastAPITransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.carrier = cls.env["delivery.carrier"].create(
            {
                "name": "Chronopost 13",
                "code": "CHRONO_13",
                "product_id": cls.product_b.id,
            }
        )
        cls.sale_order_example_vals_all["delivery_order"] = {
            "code": "CHRONO_13",
            "price_unit": 15.0,
        }

    def setUp(self):
        super().setUp()
        self.env = self.env(
            context=dict(self.env.context, test_queue_job_no_delay=True)
        )

    def test_import_with_delivery_carrier(self):
        payload = self._helper_create_payload(self.get_payload_vals("all"))
        self.assertEqual(payload.state, "done")
        sale = self.get_created_sales()
        self.assertTrue(sale.ids)
        self.assertEqual(sale.carrier_id, self.carrier)
        delivery_line = sale.order_line.filtered(lambda line: line.is_delivery)
        self.assertEqual(delivery_line.price_unit, 15.0)
