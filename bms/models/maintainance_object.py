from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class MaintainanceObject(models.Model):
    """
    Maintenance object table
    """

    _name = "bms.maintainance_object"
    _description = "Maintenance object definition"
    _sql_constraints = [('unique_internal_id', 'unique(internal_id)', 'internal_id must be unique otherwise mo_id is not unique')]

    name = fields.Char("name", required=True)
    import_id = fields.Char("sourced data id")
    import_source = fields.Char("sourced from")
    internal_id = fields.Integer("Lantis internal id", required=True, readonly=True)
    mo_id = fields.Char(compute="_compute_mo_id", store=True, string="maintainance object id", readonly=True)
    mo_semantic_id = fields.Char(string="object code project")
    awv_id = fields.Char(string="AWV id")

    bo_temporary_type = fields.Char(string="proposed new type")
    awv_type_not_found = fields.Boolean(string="AWV type not found?")

    ownership_doc = fields.Char(string="link ownership doc")

    is_managing_level = fields.Boolean(string="Is managing level?" ) 
    contract_mgr_lantis = fields.Many2one(comodel_name="bms.agent", string="contract mgr Lantis")
    contract_mgr_contractor = fields.Many2one(comodel_name="bms.agent", string="contract mgr Contractor")
    maintainance_mgr_lantis = fields.Many2one(comodel_name="bms.agent", string="maintainance mgr Lantis")
    maintainance_mgr_contractor = fields.Many2one(comodel_name="bms.agent", string="maintainance mgr Contractor")
    technical_mgr_lantis = fields.Many2one(comodel_name="bms.agent", string="technical mgr Lantis")
    technical_mgr_contractor = fields.Many2one(comodel_name="bms.agent", string="technical mgr Contractor")

    loc_pt_wgs84_x = fields.Float(string="x coordinate wgs84")
    loc_pt_wgs84_y = fields.Float(string="y coordinate wgs84")
    loc_pt_wgs84_z = fields.Float(string="z coordinate wgs84")
    loc_pt_wgs84_source = fields.Selection(selection= [('0',"MANUEEL"),('1', "MEETTOESTEL")], string="ref point wgs84 source")
    loc_pt_wgs84_precision = fields.Selection(selection=[('0', 'METER'), ('1', 'PLUS_METER')], string="ref point wgs84 precision")
    loc_ident = fields.Char(string="ident")
    loc_ref_milestone = fields.Float(string="ident ref milestone")
    loc_ref_distance = fields.Float(string="distance ref milestone")
    

    #related
    owner_contact = fields.Many2one(related="owner_id.contact_person", string="contact person")
    managing_org_contact = fields.Many2one(related="managing_org_id.contact_person", string="contact person")
   
    inherited_managing_org_id = fields.Many2one(related="mg_level_obj_id.managing_org_id", string="managing organisation")
    inherited_managing_org_contact = fields.Many2one(related="inherited_managing_org_id.contact_person", string="contact person")
    inherited_contract_mgr_lantis = fields.Many2one(related="mg_level_obj_id.contract_mgr_lantis", string="contract mgr Lantis")
    inherited_contract_mgr_contractor = fields.Many2one(related="mg_level_obj_id.contract_mgr_contractor", string="contract mgr Contractor")
    inherited_maintainance_mgr_lantis = fields.Many2one(related="mg_level_obj_id.maintainance_mgr_lantis", string="maintainance mgr Lantis")
    inherited_maintainance_mgr_contractor = fields.Many2one(related="mg_level_obj_id.maintainance_mgr_contractor", string="maintainance mgr Contractor")
    inherited_technical_mgr_lantis = fields.Many2one(related="mg_level_obj_id.technical_mgr_lantis", string="technical mgr Lantis")
    inherited_technical_mgr_contractor = fields.Many2one(related="mg_level_obj_id.technical_mgr_contractor", string="technical mgr Contractor")

    #compute
    has_object_type_ids = fields.Boolean(compute="_compute_has_object_type_ids" ,store=False) # field for visualisation purpose. Invisibilize object_type_ids in view

    # relational fields
    object_type_ids = fields.Many2many(
        comodel_name="bms.object_type",
        relation="bms_objects_to_types",
        column1="object_id",
        column2="object_type_id",
    )

    event_handover_ids = fields.Many2many(comodel_name="bms.event_handover",
                                          relation="bms_event_handovers_to_objects",
                                          column1="object_id", column2="event_handover_id", string=" ")

    decomposition_ids = fields.One2many(comodel_name="bms.decomposition_relationship", inverse_name="object_id")  
    oslo_attributen_value_id = fields.One2many(comodel_name="bms.oslo_attributen_value", inverse_name="object_id")

    owner_id = fields.Many2one(comodel_name="bms.organisation", string="owner")
    managing_org_id = fields.Many2one(comodel_name="bms.organisation", string="managing organisation")
    mg_level_obj_id = fields.Many2one(comodel_name="bms.maintainance_object", string="management level object")

    maintainance_regime_id = fields.Many2one(comodel_name="bms.maintainance_regime", string="Maintainance regime")

    @api.depends("object_type_ids")  
    def _compute_has_object_type_ids(self):
        for rec in self:
            if rec.object_type_ids:
                rec.has_object_type_ids = True
            else:
                rec.has_object_type_ids = False
    
    @api.depends("internal_id")
    def _compute_mo_id(self):
        for rec in self:
            rec.mo_id = "MO-" + str(rec.internal_id)

    @api.constrains("decomposition_ids")
    def _constraints_decomposition_ids(self):
        for rec in self:
            if not rec.decomposition_ids:
                raise ValidationError("You have to assign at least one decomposition")

    def copy(self, default=None):
        """ overwritte copy method to feed the bms_decomposition_relationship,
            bms_oslo_attributen_value tables too """
        
        copied_rec =  super().copy(default)

        tables = ["bms.decomposition_relationship", "bms.oslo_attributen_value"] 
        domain = [("object_id", "=", self.id)]

        for table in tables:
            recs = self.env[table].search(domain)
            for rec in recs:
                rec.copy(default={"object_id": copied_rec.id})

        return copied_rec

    @api.model
    def create(self, vals):
        # create the right value for internal_id
        vals = self._update_internal_id(vals)
        recs = super(MaintainanceObject, self).create(vals)
        # update mgt_level_object_id accroding to is_managing_level
        for rec in recs:
            rec._update_mg_object(rec)    
        return recs
                
    def write(self, vals):
        if vals.get('is_managing_level') is not None and self.is_managing_level != vals.get('is_managing_level'):

            self._update_mg_object(vals)
        result = super(MaintainanceObject, self).write(vals)
        return result

    def get_view(self, view_id=None, view_type='form', **options):
        res = super().get_view(view_id, view_type, **options)
        return res
    
    # @api.model
    # def get_siblings(self, object_id, object_type_id=None):
    #     """ 
    #         get siblings of object_id. iven, if object_type is given only the object of same type of the same type are returned. 
    #         !!! Decomposition is hardcoded to 1 (Lantis decomposition) !!!
    #     """
    #     # getparent
    #     parent_obj_rec = self.env["bms.decomposition_relationship"].get_parent(object_id, decomposition_type_id = 1)
    #     domain = 
    #     # sibling_object_recs = self.env["bms.maintainance_object"].get_siblings(object_id, object_type_id)
    #     print("get_siblings parent", parent_obj_rec)
    #     sibling_object_recs = "to do"
    #     return sibling_object_recs
        

    def _update_internal_id(self, vals):
        """retun vals with the the incremented internal_id before creation"""
        max_internal_id_rec = self.env["bms.maintainance_object"].read_group([], ["internal_id:max(internal_id)"], [])
        max_id = max_internal_id_rec[0].get("internal_id")
        if max_id is None:
            max_id = 0
        
        if type(vals) == dict:
            # assign internal_id
            max_id +=  1
            vals.update(internal_id=max_id)
            
        if type(vals) == list:
            for vals_item in vals:
                max_id +=  1
                vals_item.update(internal_id=max_id)
       
        return vals

    def _update_mg_object(self, vals):
        """ when is_managing_level field is True: the managing level object is the object itself and all its children are updated with its id down to the object where is_managing_level is True
            when is_managing_level field is False: the managing level is the first of the parent objects with is_managing_level on True. If it does not exist then it remains null            
            Technical note:
                use of super(...).write to avoid to fall in infinite loop with the orveridden write() method
        """
        # if self.is_managing_level != vals.get("is_managing_level"):
        if vals["is_managing_level"] is True:
            self._set_mg_level_to_children(self.id)
            self._set_mg_level_obj_id(None)
        if vals is None or vals["is_managing_level"] is False: #vals None if created and not filled-in.
            mg_level_obj_id = self._get_mg_level_from_parent(self.id)
            self._set_mg_level_to_children(mg_level_obj_id)
            self._set_mg_level_obj_id(mg_level_obj_id, reset_mgt_fields=True)
            
    def _set_mg_level_obj_id(self, mg_level_obj_id, reset_mgt_fields=False):
        vals = {'mg_level_obj_id': mg_level_obj_id}
        if reset_mgt_fields:
            vals = {**vals,
                'managing_org_id': None,
                'contract_mgr_lantis': None,
                'contract_mgr_contractor': None,
                'maintainance_mgr_lantis': None,
                'maintainance_mgr_contractor': None,
                'technical_mgr_lantis': None,
                'technical_mgr_contractor': None
            }
        super(MaintainanceObject, self).write(vals)
                
    def _set_mg_level_to_children(self, mg_level_obj_id):
        """assign to the children of mg_level_obj_id, the id down to the first object which is also a 
            manegement level.    
        """
        children_recs = self.get_children(self.id)
        if children_recs:
            for child_rec in children_recs:
                if child_rec.is_managing_level is False:
                    self._set_mg_level_obj_id(mg_level_obj_id)
                    child_rec._set_mg_level_to_children(mg_level_obj_id)
        else:
            if self.is_managing_level is False:
                self._set_mg_level_obj_id(mg_level_obj_id)


    def get_children(self, object_id):
        """ Attention: decompostion_type_id is hardcoded!"""
        domain = [("parent_object_id", "=", object_id), ("decomposition_type_id", "=", 1)] 
        recs = self.env["bms.decomposition_relationship"].search(domain)
        return [rec.object_id for rec in recs]
    
    def _get_mg_level_from_parent(self, object_id):
        """get the first occurence among the parent objects of an object where the managing is performed (could be None)
           Attention: decompostion_type_id is hardcoded! """
        domain = [("object_id", "=", object_id), ("decomposition_type_id", "=", 1)]
        rec = self.env["bms.decomposition_relationship"].search(domain)
        if rec:
            if rec.parent_object_id.is_managing_level is True:
                return rec.parent_object_id
            else:
                self._get_mg_level_from_parent(rec.parent_object_id.id)
        else: 
            return None

    

    # def _copy_attributen_value(self, mo_id):
    #     """create a new record by copying th    e values of mo_id"""
    #     attr_val_recs = self.env["bms.oslo_attributen_value"]
        
      
        
