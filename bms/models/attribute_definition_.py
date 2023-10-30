from typing import Any
from odoo import models, fields, api


class AttributeDefinition(models.Model):
    _name = "bms.attribute_definition_"
    _description = """ Centralize all the attributes types with a child-parent patter
         """

    uri = fields.Char("uri")
    name = fields.Char("name")
    label_nl = fields.Char("label_nl")
    definition_nl = fields.Char("definition_nl")
    type = fields.Char("type")
    oslo_datatype = fields.Char("oslo data type")
    constraints = fields.Char("constraints")
    parent_id = fields.Many2one(
        comodel_name="bms.attribute_definition_", string="parent_id"
    )
    parent_uri = fields.Char("parent_uri")

    @api.model
    def populate_table_with_awv_otl(self, oslo_class_id):
        """use to populte the table with the awv tables :
        oslo_class, oslo_attributen, oslo_datatype_primitive, oslo_datatype_primitive_attributen,
        oslo_enumeration, oslo_datatype_complex, oslo_datatype_complex_attributen
        If other OTL than awv are considered, this method has to be adapted.
        """
        awv_attributen = AWVAttributen(self, oslo_class_id)
        awv_attributen.populate()

    @api.model
    def get_att_def(self, class_id):
        from pprint import pprint

        pprint(class_id)
        pprint(JSONAttrDef(self, class_id).get_data())


# utility classes

import logging

logger = logging.getLogger(__name__)


def get_datatype(model, attribute_uri):
    """note: model is the self of self.env[my_table]"""
    domain = [("item_uri", "=", attribute_uri)]
    attribute_datatype = model.env["bms.oslo_type_link_tabel"].search(domain).item_tabel
    return attribute_datatype


class AttributeDefinitionRecord:
    def __init__(
        self, model, record, parent_id=None, parent_uri=None, oslo_datatype=None
    ):
        """kwargs is an odoo record"""
        self.model = model
        self.attr_def = {
            "uri": record.uri,
            "name": record.name,
            "label_nl": record.label_nl,
            "definition_nl": record.definition_nl,
            "type": record.type if hasattr(record, "type") else None,
            "oslo_datatype": oslo_datatype,
            "constraints": record.constraints
            if hasattr(record, "constraints")
            else None,
            "parent_id": parent_id,
            "parent_uri": parent_uri,
        }

    def create(self):
        created_rec = self.model.env["bms.attribute_definition_"].create(
            [self.attr_def]
        )
        return (created_rec.id, created_rec.uri)


class AwvDatatypePrimitive(AttributeDefinitionRecord):
    def __init__(
        self, model, datatype_primitive_rec, parent_id, parent_uri, oslo_datatype
    ):
        super().__init__(
            model, datatype_primitive_rec, parent_id, parent_uri, oslo_datatype
        )

    def populate(self):
        # create datatype_primitive record in attribute defintion table
        parent_id, parent_uri = self.create()

        # create datatype_primitive_attributen records in attribute definiton table
        domain = [("class_uri", "=", self.attr_def["uri"])]
        datatype_primitive_attr_recs = self.model.env[
            "bms.oslo_datatype_primitive_attributen"
        ].search(domain)
        for datatype_primitive_attr_rec in datatype_primitive_attr_recs:
            AttributeDefinitionRecord(
                self.model,
                datatype_primitive_attr_rec,
                parent_id,
                parent_uri,
                "OSLODatatypePrimitiveAttributen",
            ).create()


class AwvEnumeration(AttributeDefinitionRecord):
    def __init__(self, model, enumeration_record, parent_id, parent_uri, oslo_datatype):
        super().__init__(
            model, enumeration_record, parent_id, parent_uri, oslo_datatype
        )

    def populate(self):
        # create enumeration record in attribute definition table
        _, _ = self.create()
        # the choices of the choise lists (keuzelijst) are not added to the attribute definition table
        pass


class AwvDatatypeComplex(AttributeDefinitionRecord):
    def __init__(
        self, model, datatype_complex_record, parent_id, parent_uri, oslo_datatype
    ):
        super().__init__(
            model, datatype_complex_record, parent_id, parent_uri, oslo_datatype
        )

    def populate(self):
        # create datatypecomplex record in attribute definition table
        parent_id, parent_uri = self.create()

        # datatypecomplex attributen
        domain = [("class_uri", "=", self.attr_def["uri"])]
        oslo_datatype_complex_attributen_recs = self.model.env[
            "bms.oslo_datatype_complex_attributen"
        ].search(domain, [])

        for (
            oslo_datatype_complex_attributen_rec
        ) in oslo_datatype_complex_attributen_recs:
            attribute_datatype = get_datatype(
                self.model, oslo_datatype_complex_attributen_rec.type
            )
            AWVAttributen.getDatatypePopulator(
                self.model,
                attribute_datatype,
                oslo_datatype_complex_attributen_rec,
                parent_id,
                parent_uri,
            ).populate()
            # _, _ = AttributeDefinitionRecord(self.model, oslo_datatype_complex_attributen_rec, parent_id, parent_uri, attribute_datatype).create()

            # if datatypecomplex attributen is a dataypecomplex iterate otherwise do nothing
            # if attribute_datatype == 'OSLODatatypeComplex':
            #     AwvDatatypeComplex(self.model, oslo_datatype_complex_attributen_rec, parent_id, parent_uri, attribute_datatype).populate()


class AwvDatatypeUnion(AttributeDefinitionRecord):
    def __init__(
        self, model, datatype_complex_record, parent_id, parent_uri, oslo_datatype
    ):
        super().__init__(
            model, datatype_complex_record, parent_id, parent_uri, oslo_datatype
        )

    def populate(self):
        # create datatypecomplex record in attribute definition table
        parent_id, parent_uri = self.create()

        # datatypeunion attributen
        domain = [("class_uri", "=", self.attr_def["uri"])]
        oslo_datatype_union_attributen_recs = self.model.env[
            "bms.oslo_datatype_union_attributen"
        ].search(domain, [])

        for oslo_datatype_union_attributen_rec in oslo_datatype_union_attributen_recs:
            attribute_datatype = get_datatype(
                self.model, oslo_datatype_union_attributen_rec.type
            )
            # if oslo_datatype_complex_attributen_rec == 'OSLODatatypeComplex': breakpoint()
            AWVAttributen.getDatatypePopulator(
                self.model,
                attribute_datatype,
                oslo_datatype_union_attributen_rec,
                parent_id,
                parent_uri,
            ).populate()


class AWVAttributen:
    def __init__(self, model, oslo_class_id):
        self.model = model  # odoo model self of self.env["my_model"]
        self.oslo_class_id = oslo_class_id  # item of table bms.oslo_class

    def populate(self):
        """
        Take all the attributes link to a class id, and populate with a factory of populators based on the type of each attribute
        """
        oslo_class_rec = self.model.env["bms.oslo_class"].browse(self.oslo_class_id)
        parent_id, parent_uri = AttributeDefinitionRecord(
            self.model, oslo_class_rec, oslo_datatype="OSLOclass"
        ).create()

        domain = [("class_uri", "=", oslo_class_rec.uri)]
        oslo_attributen_recs = self.model.env["bms.oslo_attributen"].search(domain, [])

        for oslo_attributen_rec in oslo_attributen_recs:
            attribute_datatype = get_datatype(self.model, oslo_attributen_rec.type)
            attr_id, attr_uri = AttributeDefinitionRecord(
                self.model, oslo_attributen_rec, parent_id, parent_uri, "OSLOAttributen"
            ).create()
            self.getDatatypePopulator(
                self.model, attribute_datatype, oslo_attributen_rec, attr_id, attr_uri
            ).populate()

    @classmethod
    def getDatatypePopulator(
        cls, model, attribute_datatype, attributen_record, parent_id, parent_uri
    ):
        """Factory based on attribute_datatype"""
        match attribute_datatype:
            case "OSLODatatypePrimitive":
                domain = [("uri", "=", attributen_record.type)]
                datatype_primitive_rec = model.env[
                    "bms.oslo_datatype_primitive"
                ].search(domain)
                return AwvDatatypePrimitive(
                    model,
                    datatype_primitive_rec,
                    parent_id,
                    parent_uri,
                    attribute_datatype,
                )

            case "OSLOEnumeration":
                domain = [("uri", "=", attributen_record.type)]
                datatype_enumeration_rec = model.env["bms.oslo_enumeration"].search(
                    domain
                )
                return AwvEnumeration(
                    model,
                    datatype_enumeration_rec,
                    parent_id,
                    parent_uri,
                    attribute_datatype,
                )

            case "OSLODatatypeComplex":
                domain = [("uri", "=", attributen_record.type)]
                datatype_complex_rec = model.env["bms.oslo_datatype_complex"].search(
                    domain
                )
                return AwvDatatypeComplex(
                    model,
                    datatype_complex_rec,
                    parent_id,
                    parent_uri,
                    attribute_datatype,
                )

            case "OSLODatatypeUnion":
                domain = [("uri", "=", attributen_record.type)]
                datatype_union_rec = model.env["bms.oslo_datatype_union"].search(domain)
                return AwvDatatypeUnion(
                    model, datatype_union_rec, parent_id, parent_uri, attribute_datatype
                )

            case default:
                msg = """Oslo attribute_type '{0}' unknown. Check TypeLinkTabel in OSLO sqlite database. Tip: 'select distinct item_tabel
                         from TypeLinkTabel' """.format(
                    str(attribute_datatype)
                )
                raise Exception(msg)


class JSONAttrDef:
    def __init__(self, model, oslo_class_uri):
        """class_id is an oslo identifier of an object type"""
        self.model = model
        self.oslo_class_uri = oslo_class_uri[0]  # TODO [0] only for testing
        self.attr_def = self._generate_json()

    def get_data(self):
        import json

        return json.dumps(self.attr_def)

    def _generate_json(self):
        attr_defs = {"oslo_class_uri": self.oslo_class_uri, "attributes": []}
        attribute_recs = self._get_attributes()
        if len(attribute_recs) == 0:
            return attr_defs

        for attribute_rec in attribute_recs:
            datatype_recs = self._get_children(attribute_rec.id)
            attr_def = {
                "attr_name": attribute_rec.label_nl,
                "attr_definition_nl": attribute_rec.definition_nl,
                "attr_datatype": datatype_recs.oslo_datatype
                # "oslo_datatype_primitive": [],
                # "oslo_datatype_enumeration": [],
                # "oslo_datatype_complex": [],
                # "oslo_datatype_union": [],
            }
            # breakpoint()
            for datatype_rec in datatype_recs:
                match datatype_rec.oslo_datatype:
                    case "OSLODatatypePrimitive":
                        attr_def[
                            "oslo_datatype_primitive"
                        ] = self._format_datatype_primitive(datatype_rec)

                    case "OSLOEnumeration":
                        attr_def[
                            "oslo_datatype_enumeration"
                        ] = self._format_datatype_enumeration(attribute_rec)

                    case "OSLODatatypeComplex":
                        pass

                    case "OSLODatatypeUnion":
                        pass

                    case default:
                        msg = """Oslo attribute_type '{0}' unknown. ('{1}')  Check TypeLinkTabel in OSLO sqlite database. Tip: 'select distinct item_tabel
                            from TypeLinkTabel' """.format(
                            str(attribute_rec.oslo_datatype, attribute_rec.uri)
                        )
                        raise Exception(msg)

                attr_defs["attributes"].append(attr_def)

        return attr_defs

    def _format_datatype_primitive(self, datatype_rec):
        """returns an dictionnary like :
        {
         "datatype_label_nl": "Kwantitatieve waarde in meter TAW",
         "datatype_definition_nl": "Een kwantitatieve waarde die de hoogte weergeeft in meter van een locatie tov het TAW-referentiepeil.",
         "oslo_datatype": "OSLODatatypePrimitive",
         "unit": "\"m\"^^cdt:ucumunit",
         "value_id": 140282,
         "att_type": "http://www.w3.org/2001/XMLSchema#decimal"
        }
        """

        datatype_def = {
            "datatype_label_nl": datatype_rec.label_nl,
            "datatype_definition_nl": datatype_rec.definition_nl,
            "oslo_datatype": datatype_rec.oslo_datatype,
        }
        datatype_att_recs = self._get_children(datatype_rec.id)
        if (
            len(datatype_att_recs) == 0
        ):  # datatype of kind http://www.w3.org/2001/XMLSchema#xxx
            datatype_def = {
                **datatype_def,
                "value_id": datatype_rec.id,
                "att_type": datatype_rec.uri,
            }
        else:
            for datatype_att_rec in datatype_att_recs:
                if datatype_att_rec.name == "waarde":
                    datatype_def = {
                        **datatype_def,
                        "value_id": datatype_att_rec.id,
                        "att_type": datatype_att_rec.type,
                    }
                if datatype_att_rec.name == "standaardEenheid":
                    datatype_def = {
                        **datatype_def,
                        "unit": datatype_att_rec.constraints,
                    }
        return datatype_def

    def _format_datatype_enumeration(self, datatype_rec):
        datatype_def = {
            "datatype_label_nl": datatype_rec.label_nl,
            "datatype_definition_nl": datatype_rec.definition_nl,
            "oslo_datatype": datatype_rec.oslo_datatype,
            "value_id": datatype_rec.id,
            "selection_values": [],
        }
        enumeration_value_recs = self._get_enumeration_values(datatype_rec.type)
        if len(enumeration_value_recs) == 0:
            pass  # TODO give advices to submit new proposal to AWV

        for enumeration_value_rec in enumeration_value_recs:
            selection_value = {
                "status": enumeration_value_rec.status,
                "definition": enumeration_value_rec.definition,
                "notation": enumeration_value_rec.notation,
                "selection_id": enumeration_value_rec.selection_id,
            }
            datatype_def["selection_values"].append(selection_value)
        breakpoint()
        return datatype_def

    def _get_children(self, parent_id):
        domain = [("parent_id", "=", parent_id)]
        return self.model.env["bms.attribute_definition_"].search(domain)

    def _get_enumeration_values(self, enumeration_uri):
        domain = [("uri", "=", enumeration_uri)]
        return self.model.env["bms.oslo_enumeration_values"].search(domain)

    def _get_attributes(self):
        """ " Get OSLOAttributen of OSLOClass based on class_uri"""
        domain = [("parent_id", "=", self.oslo_class_uri)]
        attr_def_recs = self.model.env["bms.attribute_definition_"].search(domain)
        return attr_def_recs

        # children_nodes = []
        # for record in children_records:
        #     child_node = self._record2node(record)
        #     # import pdb; pdb.set_trace()
        #     little_children_nodes = self._get_children(child_node)

        #     if little_children_nodes:
        #         child_node["folder"] = True
        #         child_node["children"] = little_children_nodes

        #     children_nodes.append(child_node)

        # return children_nodes
