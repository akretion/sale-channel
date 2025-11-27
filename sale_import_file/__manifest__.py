#  Copyright (c) Akretion 2020
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)
{
    "name": "Sale Import File",
    "summary": "Base module to import sale orders from a file",
    "version": "16.0.1.0.0",
    "category": "Generic Modules/Sale",
    "author": "Akretion, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/sale-channel",
    "depends": ["sale_import_base"],
    "license": "AGPL-3",
    "data": [
        "views/sale_channel_view.xml",
        "wizards/sale_channel_import_file.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [],
    "installable": True,
}
