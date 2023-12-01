from odoo import models, fields


class DecompositionType(models.Model):
    _name = "bms.decomposition_type"
    _description = "Store the different types of decomposition"
    _order = "name asc"

    name = fields.Char("name", required=True)
    description = fields.Char("description")

    decompostion_relationship = fields.One2many(
        comodel_name="bms.decomposition_relationship", inverse_name="decomposition_type_id")
