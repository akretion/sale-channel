# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from stdnum.fr.siret import is_valid as siret_is_valid

from odoo import fields, models


class SaleChannelImporter(models.TransientModel):
    _inherit = "sale.channel.importer"

    def _manage_siret(self, vals, data):
        if data.get("siret"):
            siret = data["siret"].replace(" ", "")
            if siret_is_valid(siret):
                vals["siret"] = siret
            else:
                vals["invalid_siret"] = siret
        return vals

    def _prepare_partner(self, data, parent_id=None, archive_addresses=None):
        vals = super()._prepare_partner(
            data, parent_id=parent_id, archive_addresses=archive_addresses
        )
        vals = self._manage_siret(vals, data)
        return vals

    def _get_directory_line(self, partner, identifier):
        directory_line = partner.fr_directory_line_ids.filtered(
            lambda d: d.identifier == identifier
        )
        if not directory_line:
            if partner._fr_directory_should_sync_upon_confirmation() or (
                partner.fr_directory_entity_type in ("public", "private")
                and (
                    not partner.fr_directory_last_sync_date
                    or partner.fr_directory_last_sync_date
                    < fields.Date.context_today(self)
                )
            ):
                company = partner.company_id or self.env.company
                partner._fr_directory_sync_logs(company, partner.name)
                directory_line = partner.fr_directory_line_ids.filtered(
                    lambda d: d.identifier == identifier
                )
        return directory_line

    def _process_partner(self, customer_data):
        partner = super()._process_partner(customer_data)
        if dir_line_id := customer_data.get("directory_line_name"):
            dir_line = self._get_directory_line(partner, dir_line_id)
            if dir_line:
                partner.write({"default_fr_directory_line_id": dir_line.id})
        return partner

    def _finalize(self, new_sale_order, raw_import_data):
        res = super()._finalize(new_sale_order, raw_import_data)
        if dir_line_id := raw_import_data.get("directory_line_name"):
            dir_line = self._get_directory_line(new_sale_order.partner_id, dir_line_id)
            if dir_line:
                new_sale_order.write({"fr_directory_line_id": dir_line.id})
            # Should we raise if not found or something ? Confirmation will block
            # anyway, unless it is considered as private partner...
        return res
