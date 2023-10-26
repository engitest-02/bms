from odoo import models, fields, api
import json 

class OsloGenericModel(models.Model):
    """
    """
    _name = "bms.oslo_generic_model"
    _description = "test to regroup all the object <--> type <--> attributes <--> attr def <--> values <--> object"
    _inherits = {"bms.maintainance_object": "object_id",
                 "bms.object_type": "object_type_id",
                 "bms.oslo_attributen": "oslo_attributen_id",
                 "bms.oslo_enumeration_values": "oslo_enumeration_values_ids"}
    
    # name = fields.Char("name")
    object_name = fields.Char(related="object_id.name")
    attributen_name = fields.Char(related="oslo_attributen_ids.name")

    object_id = fields.Many2one(comodel_name="bms.maintainance_object", string="object_id")
    object_type_id = fields.Many2one(comodel_name="bms.object_type", string="object_type_id")
    oslo_attributen_ids = fields.Many2many(comodel_name="bms.oslo_attributen", string="oslo_attributen_id")
    oslo_enumeration_values_ids = fields.Many2many(comodel_name="bms.oslo_enumeration_values", string="oslo_enumeration_values_id")  

    attributen_ids_domain = fields.Binary(
       compute="_compute_attributen_ids_domain",
       readonly=True,
       store=False,
   )
    enumeration_values_ids_domain = fields.Binary(
       compute="_compute_enumeration_values_ids_domain",
       readonly=True,
       store=False,
   )

    @api.depends('object_type_id')
    def _compute_attributen_ids_domain(self):
        for rec in self:
            rec.attributen_ids_domain = [('class_uri', '=',  rec.otl_type_internal_id)]

    @api.depends('oslo_attributen_ids','object_type_id')
    def _compute_enumeration_values_ids_domain(self):
        for rec in self:
            print(str([('uri', '=',  rec.oslo_attributen_ids.type)]))
            rec.enumeration_values_ids_domain = [('uri', 'in',  rec.oslo_attributen_ids.type)]
