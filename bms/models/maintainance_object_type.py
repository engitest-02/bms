from odoo import models, fields


class MaintainanceObjectTypeLibrary(models.Model):
    '''
        Maintenance object type
    '''
    _name = 'bms.maintainance_object_type_library'
    _description = 'Maintenance object type library'

    name = fields.Char('name', required=True)
    description = fields.Char("Description")
    # maintainance_object_ids = fields.Many2many(
    #     comodel_name="bms.maintainance_object"
    # )
