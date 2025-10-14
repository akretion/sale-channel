#  Copyright (c) Akretion 2020
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo.tests.common import Form, SavepointCase


class TestSaleChannel(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.sale_channel = cls.env.ref("sale_channel.sale_channel_amazon")
        cls.sale_order = cls.env.ref("sale.sale_order_3")
        cls.product_sol = cls.env.ref("sale.sale_order_line_7")
        # badly recompute because of demo data and not recomputed when sale_stock
        # is installed
        cls.product_sol._compute_qty_delivered_method()
        cls.route = cls.env["stock.route"].create(
            {
                "name": "dummy route",
                "sale_selectable": True,
            }
        )
        cls.sale_channel.write({"route_id": cls.route.id})

    def test_sale_channel_onchange_route(self):
        with Form(self.sale_order) as sale_form:
            sale_form.sale_channel_id = self.sale_channel
            sale_form.save()
        self.assertEqual(self.product_sol.route_id, self.route)
        with Form(self.sale_order) as sale_form:
            sale_form.sale_channel_id = self.env["sale.channel"]
            sale_form.save()
        self.assertFalse(self.product_sol.route_id)

    def test_sale_channel_route_confirm(self):
        self.sale_order.write({"sale_channel_id": self.sale_channel.id})
        self.assertFalse(self.product_sol.route_id)
        self.sale_order.action_confirm()
        self.assertEqual(self.product_sol.route_id, self.route)
