# MS Access migration and BMS app initialization#

## Import Object data from MSAcess db ##
1. Export object table from MS Access into  'msa_object.xlsx'
```
SELECT object.OBJECT_ID, object.NAME, object.PARENT_ID, object.OTL_TYPE_ID, OSLOClass.uri, object.Tree_Level, object.AWV_type_not_found, object.BO_temporary_type, object.Tree_node_order
FROM [object] INNER JOIN OSLOClass ON object.OTL_TYPE_ID = OSLOClass.ID;
````
2. Import excel `msa_object.xlsx` into table `bms.msa_object` via favorites > `import file`

3. Initialize bms_maintainance_object table with MS Access data
```
insert into bms_maintainance_object(
    name, msa_unique_id, internal_id, mo_id, 
    mo_semantic_id, awv_type_not_found, bo_temporary_type
    )
(select 
    name, object_id as msa_unique_id, object_id as internal_id, 'MO-' || object_id as mo_id , 
    bo_codering as mo_semantic_id, awv_type_not_found, bo_temporary_type 
    from bms_msa_object
);
```

## Import AWV OTL data ##
1. initial import AWV OTL (other procedure in case of Update!!!)
2. get the SQLite db: https://wegenenverkeer.data.vlaanderen.be/doc/implementatiemodel/master/html/OTL.db
3. export all the tables to *.CSV file
4. import them via the ```favorite > import file``` of each corresponding form on the BMS

### create AWV Type Library ###
1. Go to the shell and psql command
2. execute query
```
insert into bms_object_type_library (name, description)
select 'OTL AWV', 'Object Type Library defined by Agentschap Wegen en Verkeer';
```

## Update bms.object_type table ##
1. Go to the shell and psql command
2. link objects with object_type base on bms_msa_object table. Check that internal id of otl awv is 1, otherwise adapt query accordingly. 
´´´
insert into bms_object_type (name, definition, otl_type_internal_id, otl_id)
select 
    oc.label_nl, oc.definition_nl, oc.uri, 1
    from bms_oslo_class oc
;
´´´

## update bms_objects_to_types ##
1. Go to the shell and psql command
2. link maintainance_object with object_type by executing the following SQL

```
insert into bms_objects_to_types (object_id, object_type_id)
(select mo.id as mo_id, ot.id as object_type_id
from bms_msa_object msa_o
inner join bms_maintainance_object mo on cast(mo.msa_unique_id as Integer) = msa_o.object_id 
--left join bms_oslo_class oc on oc.uri = msa_o.oslo_class_uri
left join bms_object_type ot on ot.otl_type_internal_id = msa_o.oslo_class_uri
where msa_o.otl_type_id is not null and msa_o.otl_type_id <> 0
)
;
```

## create decompostion_type ##
1. go to the shell and psql command
2. insert into bms_decomposition_type the type "Lantis"
```
insert into bms_decomposition_type (name, description)
select 'Lantis', 'Physical decomposition of the Oosterweelverbinding infrastructure';
```

## Udpate decompostion_relationship ##
1. go to the shell and psql command
2. insert into bms_decomposition_relationship the data of the msacces table
```
insert into bms_decomposition_relationship (object_id, parent_object_id, sibling_order, decomposition_type_id)
(select mo.id, mo2.id, msa.tree_node_order, 1
from bms_msa_object msa
inner join bms_maintainance_object mo on cast(mo.msa_unique_id as integer) = msa.object_id
left join bms_maintainance_object mo2 on cast(mo2.msa_unique_id as integer) = msa.parent_id
);
```

## Generate the Attribute Definition table ##
1. go to menu ´imports´
2. launch the import by clicking `populate attribute definition table` and wait for the action is done. 
Tip: if for any reason you have to delete the records, use `truncate bms_attribute_definition cascade;` Be carefull impact on
NOTICE:  truncate cascades to table "bms_oslo_attributen_value"
NOTICE:  truncate cascades to table "bms_oslo_attributen_value_edit"

## import enumeration values ##
1. go to menu ´imports´
2. launch the import by clicking `import enumeration values` and wait for the import is done. 





# TODO # 
## technical ##
- [x] lazy loading for the decomposition to improve loading performance
- [X] create new object
- [x] automatic refresh of decomposition
- [x] change parent via drag&drop on decomposition
- [ ] look&feel attributes
- [ ] hover defintion attibutes
- [ ] make the import mechanism of awv list ("keuzelijsten") better by taking into account the status change (don't  know if it happens but 
theoritically it could)
- [ ] fix tree_level which should be filled in (after having checked it's still useful)
- [ ] keep common attributes when user changes of type


## Migration ##
- [ ] internal_id -> unique constraint


## Governance ##
1. Unique ID asset format
2. Quid awv type not found -> use OTL lantis (and potentially create a new type? ) + problem no attribute in Relatics (no meta-model)
3. quid versionning AWV type ? by object or by "sqlite" model
4. check status of values for the value lists (oslo enumeration)?
5. logo app
6. icons decomposition

## Refactoring ##
- [x] delete modle oslo_generic_model
- [x] attribute_value.py + views + menus + security
- [x] delte demo_agent.py
- [ ] change oslo datatype in CONSTANT VALUE defined on one place
- [ ] owl components implments props validation
- [ ] use of AWV OWL library type hardcoded in .js code
- [ ] store json of get_att_def() instead of recalulate on the fly to increase loading speed
- [ ] change res_id by default of `bms_decomposition_action`
- [ ] `get_oslo_attr_def` of `object_type.py`
- [x] change view "decomposition type" in order to not display the decomposition_relationships
- [ ] check if get_view() in maintainance_object.py is still useful