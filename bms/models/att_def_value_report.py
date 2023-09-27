from odoo import fields, models, tools, api


class AttDefValueReport(models.Model):
    _name = "bms.att_def_value_report"
    _description = "Help to display the definitions and values for the type of object"
    _auto = False
    # _rec_name = 'name'
    # _order = 'invoice_date desc'
    
    att_def_id = fields.Integer()
    name = fields.Char(readonly=True)
    description = fields.Char(readonly=True)
    type_id = fields.Integer()
    # fields.Many2many(
    #     comodel_name="bms.object_type",
    #     relation="bms_attributes_to_types",
    #     column1="attribute_id",
    #     column2="type_id",
    # )
    otl_id = fields.Integer()
    value_type = fields.Char()
    att_val_id = fields.Integer()
    value_string = fields.Char()
    value_boolean = fields.Boolean()
    value_date = fields.Date()
    value_float = fields.Float()
    value_binary = fields.Binary()
    value_integer = fields.Integer()
    object_id = fields.Integer()

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute(
            """
    CREATE view %s as
         SELECT %s
           FROM %s
        """
            % (self._table, self._select(), self._from())
        )

    # @property
    # def _table_query(self):
    #     return "%s %s %s" % (self._select(), self._from(), self._where())

    @api.model
    def _select(self):
        return """
             row_number() OVER () as id
            , att_def.id as att_def_id
            , att_def.name as name
            , att_def.description as description
            , ot.id as type_id
            , ot.otl_id as otl_id
            , att_def.value_type
            , att_val.id as att_val_id
            , value_string
            , value_boolean
            , value_date
            , value_float
            , value_integer
            , mo.id as object_id
                
            """

        # ,  attr_val.object_id

    @api.model
    def _from(self):
        return """
                bms_maintainance_object mo
                inner join bms_objects_to_types o2t on o2t.object_id = mo.id
                inner join bms_object_type ot on ot.id = o2t.object_type_id
                inner join bms_attributes_to_types at on at.type_id = ot.id
                inner join bms_attribute_definition att_def on att_def.id = at.attribute_id
                left join bms_attribute_value att_val on att_val.object_id = mo.id and att_val.attr_def_id = att_def.id;
                """
        #

    @api.model
    def _where(self):
        return """
                """
