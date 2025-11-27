#  License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

import base64
import csv
import json
from io import StringIO
from tempfile import NamedTemporaryFile

from odoo import exceptions, fields, models


class SaleChannel(models.Model):
    _inherit = "sale.channel"

    sale_import_file_format = fields.Selection(
        selection_add=[("mirakl_csv", "Mirakl (CSV)")]
    )

    def _get_sale_payload_vals_list(self, base64file, file_format):
        if file_format == "mirakl_csv":
            if not self:
                raise exceptions.UserError(
                    self.env._(
                        "Mirakl import should be done from a dedicated sale channel"
                    )
                )
            return self._get_mirakl_payload_vals_list(base64file)
        return super()._get_sale_payload_vals_list(base64file, file_format)

    def _get_mirakl_line_vals(self, row):
        return {
            "product_code": row["SKU boutique"],
            "qty": row["Quantité"],
            "description": row["Titre du produit"],
            "price_unit": row["Prix unitaire"],
        }

    def _get_mirakl_shipping_vals(self, row):
        return {
            "name": f"{row['Adresse de livraison : Prénom']} {row['Adresse de livraison : Nom']}",  # noqa
            "street": row["Adresse de livraison : Rue 1"],
            "street2": row["Adresse de livraison : Rue 2"],
            "zip": row["Adresse de livraison : Code postal"],
            "city": row["Adresse de livraison : Ville"],
            "country_code": row["Adresse de livraison : Pays"],
            "email": row["Adresse de livraison : E-mail"],
            "mobile": row["Adresse de livraison : Téléphone"],
            "phone": row["Adresse de livraison : Téléphone 2"],
        }

    def _get_mirakl_invoicing_vals(self, row):
        return {
            "name": f"{row['Adresse de facturation : Prénom']} {row['Adresse de facturation : Nom']}",  # noqa
            "street": row["Adresse de facturation : Rue 1"],
            "street2": row["Adresse de facturation : Rue 2"],
            "zip": row["Adresse de facturation : Code postal"],
            "city": row["Adresse de facturation : Ville"],
            "country_code": row["Adresse de facturation : Pays"],
            "mobile": row["Adresse de facturation : Téléphone"],
            "phone": row["Adresse de facturation : Téléphone 2"],
        }

    def _get_mirakl_amount_vals(self, row):
        return {
            "amount_tax": float(row["Total taxes sur produits"])
            + float(row["Total taxes sur frais de port"]),
            "amount_untaxed": float(
                row["Montant total de la commande hors taxes (frais de port inclus)"]
            ),
            "amount_total": float(
                row["Montant total de commande TTC (frais de port inclus)"]
            ),
        }

    def _add_extra_info_mirakl(self, vals, row):
        return vals

    def _get_mirakl_payload_vals_list(self, base64file):
        #        fileobj = NamedTemporaryFile("wb+", prefix="odoo-import-mirakl", suffix=".csv")
        file_bytes = base64.b64decode(base64file)
        vals_list = []
        with NamedTemporaryFile("wb+", prefix="odoo-import-mirakl", suffix=".csv") as f:
            f.write(file_bytes)
            f.seek(0)
            content = f.read().decode("utf-8")
            NBSP_HEX = "\xa0"
            NBSP_UNICODE = "\u00a0"
            content_cleaned = content.replace(NBSP_HEX, " ").replace(NBSP_UNICODE, " ")
            f_cleaned = StringIO(content_cleaned)
            spamreader = csv.DictReader(f_cleaned, delimiter=";")
            orders_data = {}
            for row in spamreader:
                shipping_vals = self._get_mirakl_shipping_vals(row)
                invoice_vals = self._get_mirakl_invoicing_vals(row)
                customer_vals = invoice_vals.copy()
                customer_vals[
                    "external_id"
                ] = f"{row['Adresse de facturation : Prénom']}-{row['Adresse de facturation : Nom']}-{row['Adresse de facturation : Rue 1']}"  # noqa
                line_vals = self._get_mirakl_line_vals(row)
                # TODO delivery line
                amounts = self._get_mirakl_amount_vals(row)

                order_name = row["N° de commande"]
                if order_name not in orders_data:
                    orders_data[order_name] = {
                        "name": order_name,
                        "address_customer": customer_vals,
                        "address_shipping": shipping_vals,
                        "address_invoicing": invoice_vals,
                        "amount": amounts,
                        "lines": [],
                    }
                orders_data[order_name]["lines"].append(line_vals)
                # Hook to override if necessary
                self._add_extra_info_mirakl(orders_data[order_name], row)
        vals_list = [
            {
                "data_str": json.dumps(sale_info, indent=4),
                "sale_channel_id": self.id,
            }
            for sale_info in orders_data.values()
        ]
        return vals_list
