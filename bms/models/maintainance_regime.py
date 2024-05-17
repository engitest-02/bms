from odoo import models, fields

FREQUENCY = [('daily', 'daily'), ('weekly', 'weekly'), ('monthly', 'monthly'), ('quarterly', 'quarterly'), ('half_yearly', 'half-yearly'), ('yearly', 'yearly')]


class MaintainanceRegime(models.Model):
    _name = "bms.maintainance_regime"
    _description = "Maintainance regime."

    name = fields.Char(string="name")
    
    service_oriented_control_required = fields.Boolean("oriented control")
    service_oriented_control_frequecy = fields.Selection(selection=FREQUENCY, string="oriented control frequency" )
    service_oriented_control_comments = fields.Char(string="comments")

    service_functional_test_required = fields.Boolean("functional test")
    service_functional_test_frequency = fields.Selection(selection=FREQUENCY, string="functional control frequency")
    service_functional_test_comments = fields.Char(string="comments")

    service_inspection_required = fields.Boolean("inspection test")
    service_inspection_frequency = fields.Selection(selection=FREQUENCY, string="inspection test frequency")
    service_inspection_comments = fields.Char(string="comments")

    #relationship
    prev_maintainance_task_ids = fields.One2many(comodel_name="bms.preventive_maintainance_task", inverse_name="maintainance_regime_id")
    billable_maintainance_work_ids = fields.One2many(comodel_name="bms.billable_maintainance_work", inverse_name="maintainance_regime_id")
    object_ids = fields.One2many(comodel_name="bms.maintainance_object", inverse_name="maintainance_regime_id")

class PreventiveMaintainanceTask(models.Model):
    _name = "bms.preventive_maintainance_task"
    _description = "Maintainance task composing a maintainance regime"

    name = fields.Char("name")
    frequency = fields.Selection(selection=FREQUENCY, string="frequency", required=True)

    #relationship
    maintainance_regime_id = fields.Many2one(comodel_name="bms.maintainance_regime")


class BillableMaintainanceWork(models.Model):
    _name = "bms.billable_maintainance_work"
    _description = "Billable maintainance work composing a maintainance regime"

    name = fields.Char("name")
    
    #relationship
    maintainance_regime_id = fields.Many2one(comodel_name="bms.maintainance_regime")