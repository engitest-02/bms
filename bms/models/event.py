from odoo import models, fields, Command



class EventHandover(models.Model):
    _name = "bms.event_handover"
    _description = "Handover event"

    description = fields.Char(compute="_compute_name", readonly=True)
    handover_type = fields.Selection(selection=[('temporary', 'temporary'), ('final', 'final'), ('unknown', 'unknown')], string="type")
    handover_date = fields.Date(string="transfer date")
    transferring_org_id = fields.Many2one(comodel_name="bms.organisation", string="transferring organisation")
    receiving_org_id = fields.Many2one(comodel_name="bms.organisation", string="receiving organisation")
    comment = fields.Text(string="comment")
    # TODO: Documens = fields.one2Many(comodel_name="bms.document")

    object_ids = fields.Many2many(comodel_name="bms.maintainance_object", relation="bms_event_handovers_to_objects"
                                 , column1="event_handover_id", column2="object_id", string="object")

    def _compute_name(self):
        for record in self:
            transferring_org = self.transeferring_org_id.name if self.transferring_org_id.name else ' '
            receiving_org = self.receiving_org_id.name if self.receiving_org_id else ' '
            type = self.handover_type if self.handover_type else ' '
            handover_date = str(self.handover_date) if self.handover_date else ' '
            return "{0} > {1} ({2}) [{3}]".format(transferring_org, receiving_org, type, handover_date)
           
    def assign_to_children(self):
        print('assing_to_chidren', self.env.context)    
        ctx_params = self.env.context.get('params')
        object_id = ctx_params.get('id')
        self._recursive_assign(object_id)

    def _recursive_assign(self, object_id):
        for child in self._get_children(object_id):
            self._recursive_assign(child)
        
        self.write({'object_ids': [Command.link(object_id)]})

    def _get_children(self, object_id):
        """ Attention: decompostion_type_id is hardcoded!"""
        domain = [("parent_object_id", "=", object_id), ("decomposition_type_id", "=", 1)] 
        recs = self.env["bms.decomposition_relationship"].search(domain)
        return [rec.object_id.id for rec in recs]
    
    def link_objects(self, object_id_list):
        command = []
        for object_id in object_id_list:
            command.append(Command.link(object_id))
        self.object_ids.write({'object_ids': command})
