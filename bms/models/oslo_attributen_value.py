from odoo import models, fields, api
from odoo.exceptions import ValidationError


class OsloAttributenValue(models.Model):
    """
    As the attributes are function of the object type, use the mechanism of
    attribute definition <-> attibute value to store in the database with the
    right native primary field type (string, float, date, ....)
    Cardinality chain
    object 1 <-> * type 1 <-> * attributes_def 1 <-> * attributes values 1 <-> 1 object

    Only to use with OTL AWV!
    """

    _name = "bms.oslo_attributen_value"
    _description = "bms.oslo_attributen_value: store values of attribute of an object type for the AWV OTL"
   
    value_type = fields.Char(string="value type")
    value_char = fields.Char("value", default=None)
    value_boolean = fields.Boolean("value", default=False)
    value_date = fields.Date("value", default=None)
    value_datetime = fields.Datetime("value", default=None)
    value_float = fields.Float("value", default=None)
    value_non_negative_integer = fields.Integer("value", default=None)
    value_enumeration  = fields.Char(related="enumeration_value_id.selection_id", string="choice", default=None, store=True)

    #related field
    otl_type_internal_id = fields.Char(related="object_type_id.otl_type_internal_id", string="otl_type_internal_id")    
    otl_name = fields.Char(related="object_type_id.otl_name", string="OTL name" )
    attr_def_id_id = fields.Integer(related='attr_def_id.id', string="attr def Id")
    object_type_id_id = fields.Integer(related='object_type_id.id', string="obj type id")

    # relational fields
    object_id = fields.Many2one(comodel_name="bms.maintainance_object", string="Maintainance Object", required=True, ondelete="cascade")
    object_type_id = fields.Many2one(comodel_name="bms.object_type", string="obj type name")
    attr_def_id = fields.Many2one(comodel_name="bms.attribute_definition", string="attr def name")
    enumeration_value_id = fields.Many2one(comodel_name="bms.oslo_enumeration_values")
    

    @api.constrains('value_non_negative_integer')
    def _check_description(self):
        for rec in self:
            if rec.value_non_negative_integer < 0:
                raise ValidationError("The expected value has to be a non negative integer")
    
    @api.model
    def copy_attr_value_to_siblings(self, args):
        """
            copy the attr value of an object to its siblings of the same type
            param: list
                [object_id, object_type_id, attr_def_id, 
                 value_char, value_boolean, value_date, value_datetime, value_float, value_non_negative_integer, enumeration_value_id ]    
        """
        print("_copy_attr_value_to_siblings called: ", args)
        [object_id, object_type_id, attr_def_id, 
         value_char, value_boolean, value_date, value_datetime, value_float,
         value_non_negative_integer, value_enumeration, enumeration_value_id, value_type] = args
       
        # get siblings of same type
        siblings_obj_recs = self.env["bms.decomposition_relationship"].get_siblings(object_id)
        for sibling_obj_rec in siblings_obj_recs:
            # import pdb
            # pdb.set_trace()
            
            obj_type_ids_list = [rec.id for rec in sibling_obj_rec.object_type_ids]  # an object could have several types, one per maintainance_object_type_library
            if object_type_id in obj_type_ids_list:
                domain = [("object_id", "=", sibling_obj_rec.id), ("object_type_id", "=", object_type_id)]
                rec = self.env['bms.oslo_attributen_value'].search(domain) 
                print("rec", rec)
                vals = {'object_id': sibling_obj_rec.id, 'object_type_id': object_type_id, 'attr_def_id': attr_def_id,
                        'value_char': value_char, 'value_boolean': value_boolean, 'value_date': value_date,
                        'value_datetime': value_datetime, 'value_float': value_float, 'value_non_negative_integer': value_non_negative_integer,
                        'value_enumeration': value_enumeration, 'enumeration_value_id': enumeration_value_id,
                        'value_type': value_type}
                # import pdb
                # pdb.set_trace()   
                if rec.id is False:
                    result = self.env['bms.oslo_attributen_value'].create(vals)
                    print('create', sibling_obj_rec.mo_id, vals)
                else:
                    result = rec.write(vals)
                    print('write', sibling_obj_rec.mo_id, vals)
                print('do you this', sibling_obj_rec.mo_id)
                print(result)
         
        print("_copy_attr_value_to_siblings", object_id,  siblings_obj_recs)
        

