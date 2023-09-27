from odoo import models, fields, api, Command


class OtlAndType(models.TransientModel):
    _name = "bms.otl_type"
    _description = (
        "Transient db for the assignation of an otl and a type to an existing object."
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
        print(".........", 'overridden WRITE')
        self._change_object_type(vals)
        return super(OtlAndType, self).write(vals)

    
  
    @api.model
    def create(self, vals):
        print(".........", 'overridden CREATE', "vals", str(vals))
        self._change_object_type(vals)
        return super(OtlAndType, self).create(vals)

 
    def _change_object_type(self, vals):
        maintainance_object_id = self._context["default_object_ids"]
        current_object_type_id = self._context["default_object_type"]
        new_object_type_id = vals['object_type']

        domain = [('id', '=', maintainance_object_id)]
        rec_maintainance_object = self.env['bms.maintainance_object'].search(domain)
        # import pdb
        # pdb.set_trace()
        current_object_type_ids = rec_maintainance_object.object_type_ids
        print("current_object_type_ids", current_object_type_ids)
        
        print("rec_maintainance_object", rec_maintainance_object,
              "current_object_type_id", current_object_type_id,
              "new_object_type_id", new_object_type_id)
        
        command = [Command.set([new_object_type_id])]
        print("command", command)
        # import pdb
        # pdb.set_trace()

        result = rec_maintainance_object.write({'object_type_ids': command})
        print(result)
        
        return result