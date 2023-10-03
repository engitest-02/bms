from odoo import models, fields


class MSAObject(models.Model):
    """
    Temp table to import table object from MS Databq
    """

    _name = "bms.maintainance_object"
    _description = "Maintenance object"