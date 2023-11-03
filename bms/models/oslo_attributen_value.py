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
    value_enumeration  = fields.Char("choice", default=None)
    
    # related fields
    attr_def_value_type = fields.Char(related="attr_def_id.uri")

    # computed
    value_type = fields.Char(compute="_compute_value_type", string="value type")

    # relational fields
    otl_type_internal_id = fields.Char(related="object_type_id.otl_type_internal_id", string="otl_type_internal_id")
    object_id = fields.Many2one(comodel_name="bms.maintainance_object", string="Maintainance Object", required=True, ondelete="cascade")
    object_type_id = fields.Many2one(comodel_name="bms.object_type", required=True, ondelete="cascade")
    attr_def_id = fields.Many2one(comodel_name="bms.attribute_definition_")

    @api.depends("attr_def_value_type")
    def _compute_value_type(self):
        # domain = [('uri','=', self.oslo_datatype_xxx_attributen_uri)]
        # rec = self.env["bms.oslo_datatype_primitive_attributen"].search(domain)
        for rec in self: 
            match rec.attr_def_value_type:
                case "http://www.w3.org/2001/XMLSchema#anyURI":
                    rec.value_type = "char"
                case "http://www.w3.org/2001/XMLSchema#boolean":
                    rec.value_type = "boolean"
                case "http://www.w3.org/2001/XMLSchema#date":
                    rec.value_type = "date"
                case "http://www.w3.org/2001/XMLSchema#dateTime":
                    rec.value_type = "datetime"
                case "http://www.w3.org/2001/XMLSchema#decimal":
                    rec.value_type = "float"
                case "http://www.w3.org/2001/XMLSchema#nonNegativeInteger":
                    rec.value_type = "integer"
                case "http://www.w3.org/2001/XMLSchema#string":
                    rec.value_type = "char"
                case default:
                    # msg ="""Type {0} is unknown.""".format(rec.attr_def_value_type)
                    # raise Exception(msg) 
                    rec.value_type = ""

    @api.model
    def test_awv_attributen(self, vals):
        domain = [("osloclass_uri", "=", "https://wegenenverkeer.data.vlaanderen.be/ns/installatie#Aardingsinstallatie")]
        records = self.env["bms.test_awv_attributen"].search(domain)
        for record in records:
            print(record.osloclass_name, record.osloattributen_name, record.osloclass_uri)
