from odoo import api, models, fields


class ObjectType(models.Model):
    """
    Type of an object
    """

    _name = "bms.object_type"
    _description = "maintenance object type"

    name = fields.Char("type name")
    description = fields.Char("description")

    otl_name = fields.Char(related="otl_id.name")

    otl_id = fields.Many2one(comodel_name="bms.object_type_library")

    attribute_ids = fields.Many2many(
        comodel_name="bms.attribute_definition",
        relation="bms_attributes_to_types",
        column1="type_id",
        column2="attribute_id",
    )

    @api.model
    def get_object_type(self, ids):
        print('ids...', ids)
        result = self.browse(ids)
        print(type(result))
        return result
        # return json.dump(self.search([["object_ids", "in", [1]]]))
