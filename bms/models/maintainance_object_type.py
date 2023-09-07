from odoo import models, fields


class MaintainanceObjectType(models.Model):
    '''
        Maintenance object type
    '''
    _name = 'bms.maintainance_object_type'
    _description = 'Maintenance object type'

    name = fields.Char('name', required=True)
    description = fields.Char("Lantis ID")
    maintainance_object_ids = fields.Many2many(
        comodel_name="bms.maintainance_object"
    )
