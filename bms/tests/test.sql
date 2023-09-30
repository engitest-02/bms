SELECT 
             row_number() OVER () as id
            , att_def.id as att_def_id
            , att_def.name as name
            , att_def.description as description
            , ot.id as object_type_id
            , ot.otl_id as otl_id
            , ot.name as object_type_name
--            , att_def.value_type
--            , att_val.id as att_val_id
--            , value_string
--            , value_boolean
--            , value_date
--            , value_float
--            , value_integer
            , mo.id as object_id
                
            
                FROM 
                bms_maintainance_object mo
                left join bms_objects_to_types o2t on o2t.object_id = mo.id
                left join bms_object_type ot on ot.id = o2t.object_type_id
                left join bms_attributes_to_types at on at.type_id = ot.id
                left join bms_attribute_definition att_def on att_def.id = at.attribute_id
             --   left join bms_attribute_value att_val on att_val.object_id = mo.id and att_val.attr_def_id = att_def.id
             ;

            select mo.id, mo.name, ot.id, ot.name
                   FROM 
                bms_maintainance_object mo
                inner join bms_objects_to_types o2t on o2t.object_id = mo.id
                inner join bms_object_type ot on ot.id = o2t.object_type_id
                inner join bms_attributes_to_types at on at.type_id = ot.id
                ;