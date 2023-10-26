from odoo import models, fields, api


class AttributeDefinition(models.Model):
    _name="bms.attribute_definition_"
    _description =""" Centralize all the attributes types with a child-parent patter
         """
    
    uri = fields.Char("uri")
    name = fields.Char("name")
    label_nl = fields.Char("label_nl")
    definition_nl = fields.Char("definition_nl")
    type = fields.Char("type")
    parent_id = fields.Many2one(comodel_name="bms.attribute_definition_", string="parent_id")
    parent_uri = fields.Char("parent_uri")
    

    @api.model
    def populate_table_with_awv_otl(self, oslo_class_id):
        awv_attributen = AWVAttributen(self, oslo_class_id)
        awv_attributen.populate()



# utility classes

import logging
logger = logging.getLogger(__name__)

def get_datatype(model, attribute_uri):
    """ note: model is the self of self.env[my_table] """
    domain=[("item_uri", "=", attribute_uri)]
    attribute_datatype = model.env["bms.oslo_type_link_tabel"].search(domain).item_tabel
    return attribute_datatype

class AttributeDefinitionRecord():
    def __init__(self, model, record, parent_id=None, parent_uri=None):
        """kwargs is an odoo record"""
        self.model = model
        self.attr_def = {
            'uri': record.uri,
            'name': record.name,
            'label_nl': record.label_nl,
            'definition_nl': record.definition_nl,
            'type': record.type if hasattr(record, "type") else None,
            'constraints': record.constraints if hasattr(record, "constraints") else None,
            'parent_id': parent_id,
            'parent_uri': parent_uri
        }

    def create(self):
        created_rec = self.model.env["bms.attribute_definition_"].create([self.attr_def])
        return (created_rec.id, created_rec.uri)
    
class AwvDatatypePrimitive(AttributeDefinitionRecord):
    def __init__(self, model, datatype_primitive_rec, parent_id, parent_uri):
        super().__init__(model, datatype_primitive_rec, parent_id, parent_uri)

    def populate(self):
        # create datatype_primitive record in attribute defintion table
        parent_id, parent_uri = self.create()
        
        # create datatype_primitive_attributen records in attribute definiton table
        domain = [("class_uri", "=", self.attr_def['uri'])]
        datatype_primitive_attr_recs = self.model.env["bms.oslo_datatype_primitive_attributen"].search(domain)
        for datatype_primitive_attr_rec in datatype_primitive_attr_recs:
            AttributeDefinitionRecord(self.model, datatype_primitive_attr_rec, parent_id, parent_uri).create()

class AwvEnumeration(AttributeDefinitionRecord):
    def __init__(self, model, enumeration_record, parent_id, parent_uri):
        super().__init__(model, enumeration_record, parent_id=parent_id, parent_uri=parent_uri)

    def populate(self):
        #create enumeration record in attribute definition table
        parent_id, parent_uri = self.create()
        # the choices of the choise lists (keuzelijst) are not added to the attribute definition table
        pass

class AwvDatatypeComplex(AttributeDefinitionRecord):
    def __init__(self, model, enumeration_record, parent_id, parent_uri):
        super().__init__(model, enumeration_record, parent_id=parent_id, parent_uri=parent_uri)

    def populate(self):
        #create datatypecomplex record in attribute definition table
        parent_id, parent_uri = self.create()
        #datatypecomplex attributen
        domain = [("class_uri", "=", self.attr_def['uri'])]
        oslo_datatype_complex_attributen_recs = self.model.env["bms.oslo_datatype_complex_attributen"].search(domain,[])
        for oslo_datatype_complex_attributen_rec in oslo_datatype_complex_attributen_recs:
            attr_id, attr_uri = AttributeDefinitionRecord(self.model, oslo_datatype_complex_attributen_rec, parent_id, parent_uri).create()
            
            # if datatypecomplex attributen is a dataypecomplex iterate otherwise do nothing
            attribute_data_type = get_datatype(self.model, oslo_datatype_complex_attributen_rec.uri)
            if attribute_data_type == 'OSLODatatypeComplex':
                AwvDatatypeComplex(attribute_data_type, attribute_data_type, attr_id, attr_uri).populate()

class AWVAttributen():
    
    def __init__(self, model, oslo_class_id):
        self.model = model #odoo model self of self.env["my_model"]
        self.oslo_class_id = oslo_class_id # item of table bms.oslo_class            

    def populate(self):
        """
            Take all the attributes link to a class id, and populate with a factory of populators based on the type of each attribute
        """
        oslo_class_rec = self.model.env["bms.oslo_class"].browse(self.oslo_class_id)
        parent_id, parent_uri = AttributeDefinitionRecord(self.model, oslo_class_rec).create()

        domain = [("class_uri", "=", oslo_class_rec.uri)]
        oslo_attributen_recs = self.model.env["bms.oslo_attributen"].search(domain,[])

        for oslo_attributen_rec in oslo_attributen_recs:
            attr_id, attr_uri = AttributeDefinitionRecord(self.model, oslo_attributen_rec, parent_id, parent_uri).create()
            attribute_data_type = get_datatype(self.model, oslo_attributen_rec.type)
            self.getDataTypePopulator(attribute_data_type, oslo_attributen_rec, attr_id, attr_uri).populate()
            

    def getDataTypePopulator(self, attribute_datatype, attributen_record, parent_id, parent_uri):
        """Factory based on attribute_datatype"""
        match attribute_datatype:
            case "OSLODatatypePrimitive":
                domain = [("uri", "=", attributen_record.type)]
                datatype_primitive_rec = self.model.env["bms.oslo_datatype_primitive"].search(domain)
                return AwvDatatypePrimitive(self.model, datatype_primitive_rec, parent_id, parent_uri)
            
            case "OSLOEnumeration":
                domain = [("uri", "=", attributen_record.type)]
                datatype_enumeration_rec = self.model.env["bms.oslo_enumeration"].search(domain)
                return AwvEnumeration(self.model, datatype_enumeration_rec, parent_id, parent_uri)

            case "OSLODatatypeComplex":
                domain = [("uri", "=", attributen_record.type)]
                datatype_complex_rec = self.model.env["bms.oslo_datatype_complex"].search(domain)
                return AwvDatatypeComplex(self.model, datatype_complex_rec, parent_id, parent_uri)
            
            case "OSLODatatypeUnion":
                pass
            case default:
                msg = """Oslo attribute_type '{0}' unknown. Check TypeLinkTabel in OSLO sqlite database. Tip: 'select distinct item_tabel
                         from TypeLinkTabel' """.format(str(attribute_datatype))
                raise Exception(msg)