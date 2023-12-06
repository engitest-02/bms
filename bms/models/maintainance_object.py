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
    msa_unique_id = fields.Char("Lantis MS Access id", readonly=True)
    internal_id = fields.Integer("Lantis internal id", required=True, readonly=True)
    mo_id = fields.Char(compute="_compute_mo_id", store=True, string="maintainance object id", readonly=True)
    mo_semantic_id = fields.Char(string="object semantic id")

    bo_temporary_type = fields.Char(string="proposed new type")
    awv_type_not_found = fields.Boolean(string="AWV type not found?")

    is_managing_level = fields.Boolean(string="Is managing level?" )

    ownership_doc = fields.Char(string="link ownership doc")
    contract_mgr_lantis = fields.Many2one(comodel_name="bms.agent", string="contract mgr Lantis")
    contract_mgr_contractor = fields.Many2one(comodel_name="bms.agent", string="contract mgr Contractor")
    maintainance_mgr_lantis = fields.Many2one(comodel_name="bms.agent", string="maintainance mgr Lantis")
    maintainance_mgr_contractor = fields.Many2one(comodel_name="bms.agent", string="maintainance mgr Contractor")
    technical_mgr_lantis = fields.Many2one(comodel_name="bms.agent", string="technical mgr Lantis")
    technical_mgr_contractor = fields.Many2one(comodel_name="bms.agent", string="technical mgr Contractor")

    # #related
    owner_contact = fields.Many2one(related="owner_id.contact_person", string="contact person")
    managing_org_contact = fields.Many2one(related="managing_org_id.contact_person", string="contact person")

    #compute
    has_object_type_ids = fields.Boolean(compute="_compute_has_object_type_ids" ,store=False) # field for visualisation purpose. Invisibilize object_type_ids in view

    # relational fields
    object_type_ids = fields.Many2many(
        comodel_name="bms.object_type",
        relation="bms_objects_to_types",
        column1="object_id",
        column2="object_type_id",
    )
    decomposition_ids = fields.One2many(comodel_name="bms.decomposition_relationship", inverse_name="object_id")  
    oslo_attributen_value_id = fields.One2many(comodel_name="bms.oslo_attributen_value", inverse_name="object_id")

    owner_id = fields.Many2one(comodel_name="bms.organisation", string="owner")
    managing_org_id = fields.Many2one(comodel_name="bms.organisation", string="managing organisation")



    # @api.depends("object_type_ids")
    # def _compute_awv_type_not_found(self):
    #     for rec in self:
    #         domain = [("object_id", "=", rec.id),("otl_id", "=", 1)]
    #         record = self.env["bms.object_type"].search(domain)
    #         if len(record) < 1:
    #             rec.awv_type_not_found = True
    #         else:
    #             rec.awv_type_not_found = False
    @api.depends("object_type_ids")  
    def _compute_has_object_type_ids(self):
        for rec in self:
            if rec.object_type_ids:
                rec.has_object_type_ids = True
                return
        rec.has_object_type_ids = False
    

    @api.depends("internal_id")
    def _compute_mo_id(self):
        for rec in self:
            rec.mo_id = "MO-" + str(rec.internal_id)

    @api.constrains("decomposition_ids")
    def _constraints_decomposition_ids(self):
        print("constraints decompostion")
        for rec in self:
            if not rec.decomposition_ids:
                raise ValidationError("You have to assign at least one decomposition")

    @api.model
    def create(self, vals_list):
        # create the right value for internal_id
        print("create maintainace", vals_list)
        max_internal_id_rec = self.env["bms.maintainance_object"].read_group([], ["internal_id:max(internal_id)"], [])
        max_id = max_internal_id_rec[0].get("internal_id")
        if max_id is None:
            max_id = 0
        
        if type(vals_list) == dict:
            # assign internal_id
            max_id +=  1
            vals_list.update(internal_id=max_id)
            return super(MaintainanceObject,self).create(vals_list)
        if type(vals_list) == list:
            for vals in vals_list:
                max_id +=  1
                vals.update(internal_id=max_id)
                print("create maintainace after update list", vals)
                return super(MaintainanceObject,self).create(vals)
                
    def get_view(self, view_id=None, view_type='form', **options):
        res = super().get_view(view_id, view_type, **options)
        return res