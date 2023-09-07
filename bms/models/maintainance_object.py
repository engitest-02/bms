from odoo import models, fields


class MaintainanceObject(models.Model):
    '''
        Maintenance object table
    '''
    _name = 'bms.maintainance_object'
    _description = 'Maintenance object'

    name = fields.Char('name')
    lantis_unique_id = fields.Char("Lantis ID")
    is_active = fields.Boolean("Is active")
    is_asset = fields.Boolean("IS asset")
