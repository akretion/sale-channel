# Copyright 2021 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Sale Channel Product",
    "summary": "Link Product with sale channel",
    "version": "14.0.1.0.0",
    "category": "Sale Channel",
    "website": "https://github.com/OCA/sale-channel",
    "author": "Akretion,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": False,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "sale_channel",
    ],
    "data": [
        "views/channel_product_template_view.xml",
        "views/product_template_view.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [],
}
