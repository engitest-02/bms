from odoo import api, fields, models, tools

class AttrVisibilityWidget(models.Model):
    _name = "bms.attr_visibility_widget"
    _description = """Join bms.attribute_definition with bms.attribute_visualisation to determine
                      if the attribute has to be displayed (invisible is false) and the optional widget to use"""
    _auto = False

    
    attr_def_id = fields.Integer()
    label_nl = fields.Char()
    definition_nl = fields.Char()
    oslo_datatype = fields.Char()
    class_uri = fields.Char()
    uri = fields.Char()
    invisible = fields.Boolean()
    js_component_name = fields.Char()

    
    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute( """
            CREATE view %s as
            select
                    row_number() OVER () as id
                    , ad.id as attr_def_id
                    , a.label_nl
                    , a.definition_nl
                    -- ,tlt.item_tabel as oslo_datatype
                    , 'OSLOAttributen' as oslo_datatype
                    , a.class_uri
                    , a.uri
                    , av.invisible
                    , aw.js_component_name
                    from bms_oslo_attributen a
                    inner join bms_attribute_definition ad on ad.parent_uri= a.class_uri and a.uri = ad.uri
                    inner join bms_attribute_visualisation av on a.uri = av.uri  and (av.invisible is false or av.invisible is null)
                    left join bms_attribute_widget aw on aw.id = av.widget_id
                    --inner join bms_oslo_type_link_tabel tlt on tlt.item_uri = a.type

            """
            % (self._table)
        )

    @api.model
    def get_attr(self, class_uri):
        """ method created because env.[model].search() method has unwante weird behavior with views
            probalby because search looks for the ids and the retrieves the other fields but in the meanwhile
            the ids have ..."""

        class Record():
            """ so that the returned recs behave as an object and not as a tuple"""
            def __init__(self, sql_fetched_row):
                self.id = sql_fetched_row[0]
                self.label_nl = sql_fetched_row[1]
                self.definition_nl = sql_fetched_row[2]
                self.class_uri = sql_fetched_row[3]
                self.uri = sql_fetched_row[4]
                self.invisible = sql_fetched_row[5]
                self.js_component_name = sql_fetched_row[6]
                self.oslo_datatype = sql_fetched_row[7]
                self.class_uri = sql_fetched_row[8]


        to_flush = ['attr_def_id', 'label_nl', 'definition_nl'
                    , 'class_uri', 'uri', 'invisible','js_component_name']
        self.env['bms.attr_visibility_widget'].flush_model(to_flush) 

        sql = tools.SQL(
                 """select  attr_def_id , label_nl, definition_nl
                    , class_uri, uri, invisible, js_component_name, 
                 oslo_datatype, class_uri 
                 from bms_attr_visibility_widget 
                 where class_uri = '{0}'""" .format(class_uri))
        self.env.cr.execute(sql)
        
        recs = [Record(row) for row in self.env.cr.fetchall()]
        return recs
