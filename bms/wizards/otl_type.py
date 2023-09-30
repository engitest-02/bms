from odoo import models, fields, api, Command


class OtlAndType(models.TransientModel):
    _name = "bms.otl_type"
    _description = (
        "Transient model for the assignation of an otl and a type to an existing object."
    )

    object_ids = fields.Many2one("bms.maintainance_object", string="maintainance object")
    otl = fields.Many2one("bms.object_type_library", string="OTL")
    object_type = fields.Many2one("bms.object_type", string="object type")

    @api.onchange("otl")
    def _get_domain(self):
        if (self.otl):
            domain = [('otl_id', '=', self.otl.id)]
        else:
            domain = []
        return {'domain': {'object_type': domain}}

    def write(self, vals):
        self._change_object_type(vals)
        return super(OtlAndType, self).write(vals)

    @api.model
    def create(self, vals):
        self._change_object_type(vals)
        return super(OtlAndType, self).create(vals)

    def _change_object_type(self, vals):      
        maintainance_object_id = self._context["default_object_ids"]
        current_object_type_id = self._context["default_object_type"] if "default_object_type" in self._context else None
        new_object_type_id = vals['object_type']

        rec_maintainance_object = self.env['bms.maintainance_object'].browse([maintainance_object_id])
        
        link_command = Command.link(new_object_type_id)
        # unlink current object type if any
        if current_object_type_id is None: 
            result = rec_maintainance_object.write({'object_type_ids': [link_command]})
            
        else: # link new current object type
            unlink_command = Command.unlink(current_object_type_id)
            result = rec_maintainance_object.write({'object_type_ids': [unlink_command, link_command]})           
               
        return result
    