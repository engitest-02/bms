from odoo import fields, models, tools, api


class AWVPrimitiveDatypeAttributes(models.Model):
    _name = "bms.awv_attributen_primitive_datatype"
    _description = "Help to display the definitions and values of the attributes for AWV classes"
    _auto = False

    class_name = fields.Char("class_name")
    class_uri = fields.Char("class_uri")
    att_name = fields.Char("att_name")
    att_uri = fields.Char("att_uri")
    att_type = fields.Char("att_type")
    datatype_name = fields.Char("datatype_name")
    datatype_uri = fields.Char("datatype_uri")
    datatype_def_nl = fields.Char("datatype_def_nl")
    datatype_attributen_name = fields.Char("datatype_attributen_name")
    datatype_attributen_uri = fields.Char("datatype_attributen_uri")
    datatype_attributen_def_nl = fields.Char("datatype_attributen_def_nl")

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute(
            """
            CREATE view %s as
                SELECT %s
                FROM %s
                ;
            """
            % (self._table, self._select(), self._from())
        )

    @api.model
    def _select(self):
        return """
            c.name as class_name
            , c.uri as class_uri
            , a.name as att_name
            , a.uri as att_uri
            , a.type as att_type
            , dp.name as datatype_name
            , dp.uri as datatype_uri
            , dp.definition_nl as datatype_def_nl
            , dpa.name as datatype_attributen_name
            , dpa.uri as datatype_attributen_uri
            , dpa.definition_nl as datatype_attributen_def_nl
        """
    
    @api.model
    def _from(self):
        return """ 
            bms_oslo_class c
            inner join bms_oslo_attributen a on a.class_uri = c.uri
            inner join bms_oslo_datatype_primitive dp on dp.uri = a.type
            inner join bms_oslo_datatype_primitive_attributen dpa on dpa.class_uri = dp.uri
        """

