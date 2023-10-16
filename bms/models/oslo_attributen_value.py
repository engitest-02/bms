from odoo import models, fields, api


class OsloAttributenValue(models.Model):
    """
    As the attributes are function of the object type, creatie of mechanism of
    attribute definition <-> attibute value to store in the database with the
    right native primary field type (string, float, date, ....)
    Cardinality chain
    object 1 <-> * type 1 <-> * attributes_def 1 <-> * attributes values 1 <-> 1 object

    Only to use with OTL AWV 
    """

    _name = "bms.oslo_attributen_value"
    _description = "bms.oslo_attributen_value: store values of attribute of an object type for the AWV OTL"
   
    
    value_char = fields.Char("value", default=None)
    value_boolean = fields.Boolean("value", default=False)
    value_date = fields.Date("value", default=None)
    value_datetime = fields.Datetime("value", default=None)
    value_float = fields.Float("value", default=None)
    value_integer = fields.Integer("value", default=None)
    oslo_attributen_uri = fields.Char("oslo_attributen_uri", default=None)
    object_id= fields.Integer("object_id")
    object_type_id = fields.Integer("object_type_id")

    # compute fields
    # attr_def = fields.Char(compute="_get_attribute_def")
    # attr_def_value_type = fields.Char(compute="_get_value_type")
    
    # related fields
    # object_name = fields.Char(related="object_id.name", string="object name")
    # object_type_name = fields.Char(related="object_type_id.name", string="object type")

    #relational fields

    # object_id = fields.Many2one(comodel_name="bms.maintainance_object", string="Maintainance Object", required=True, ondelete="cascade")
    # object_type_id = fields.Many2one(comodel_name="bms.object_type", required=True, ondelete="cascade")
    

    # @api.depends("oslo_attributen_uri")
    # def _get_attribute_def(self):
    #     domain = [('uri','=', self.oslo_attributen_uri)]
    #     rec = self.env["bms.oslo_datatype_primitive"].search(domain)
    #     return rec.definition_nl

    @api.depends("oslo_attributen_uri")
    def _compute_value_type(self):
        domain = [('uri','=', self.oslo_datatype_xxx_attributen_uri)]
        rec = self.env["bms.oslo_datatype_primitive_attributen"].search(domain)
        match rec.type:
            case "http://www.w3.org/2001/XMLSchema#anyURI":
                return "char"
            case "http://www.w3.org/2001/XMLSchema#boolean":
                return "boolean"
            case "http://www.w3.org/2001/XMLSchema#date":
                return "date"
            case "http://www.w3.org/2001/XMLSchema#dateTime":
                return "datetime"
            case "http://www.w3.org/2001/XMLSchema#decimal":
                return "float"
            case "http://www.w3.org/2001/XMLSchema#nonNegativeInteger":
                return "integer"
            case "http://www.w3.org/2001/XMLSchema#string":
                return "char"
            case _:
                return ""   # TODO raise error
        

    @api.model
    def test_awv_attributen(self, vals):
        domain = [("osloclass_uri", "=", "https://wegenenverkeer.data.vlaanderen.be/ns/installatie#Aardingsinstallatie")]
        records = self.env["bms.test_awv_attributen"].search(domain)
        for record in records:
            print(record.osloclass_name, record.osloattributen_name, record.osloclass_uri)
