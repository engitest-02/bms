# MS Access migration and BMS app initialization#

## Import Object data from MSAcess db ##
1. Export object table from MS Access into  'msa_object.xlsx'
```
SELECT object.OBJECT_ID, object.NAME, object.PARENT_ID, object.OTL_TYPE_ID, OSLOClass.uri, object.Tree_Level, object.AWV_type_not_found, object.BO_temporary_type, object.Tree_node_order
FROM [object] LEFT JOIN OSLOClass ON object.OTL_TYPE_ID = OSLOClass.ID;
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

## Create AWV Type Library ##
1. Go to the shell and psql command
2. execute query
```
insert into bms_object_type_library (name, description)
select 'OTL AWV', 'Object Type Library defined by Agentschap Wegen en Verkeer';
```

## Update bms.object_type table ##
1. Go to the shell and psql command
2. link objects with object_type base on bms_msa_object table. Check that internal id of otl awv is 1, otherwise adapt query accordingly. 
```
insert into bms_object_type (name, definition, otl_type_internal_id, otl_id)
select 
    oc.label_nl, oc.definition_nl, oc.uri, 1
    from bms_oslo_class oc
;
```

## Update bms_objects_to_types ##
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

## Create decompostion_type ##
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
<br>Tip: if for any reason you have to delete the records, use `truncate bms_attribute_definition cascade;` 
<br>Be carefull impact on:
* NOTICE:  truncate cascades to table "bms_oslo_attributen_value"
* NOTICE:  truncate cascades to table "bms_oslo_attributen_value_edit"

## Import enumeration values ##
1. go to menu ´imports´
2. launch the import by clicking `import enumeration values` and wait for the import is done. 

## Import Agent from staging env ##
1. Export .xlsx of Agent table from main_staging environment
2. Import .xlsx into Agent table into main environment
3. Delete the 7 B&O members from the maintainance_object table

## Populate ``bms.attribute_visualisation`` table ##
1. Check there is no record yet
2. Run query: 
``` 
insert into bms_attribute_visualisation(label_nl, uri)
SELECT distinct label_nl, uri
FROM bms_oslo_attributen;
 ```
# TIPS #
## GIT ##
### create new branch from Prod ###
1. In odoo.sh, drag and drop build into staging and name new staging build like 'main_staging_vxxx'
2. In your shell: 
```
git fetch
```
```
git checkout -b main_staging_vxxx origin/main_staging_vxxx
```
<br> Your local repository contains the code which is currently in prod for further development. You can check that you are on the right branch with 
```
git status
``` 
or
```
git branch
```
You can see all the branches available (even if not yet on your local repository) with:
```
git branch -a
```

### Commit and push ###
1. Add all the changes to your local repository index 
```
git add *
```
2. Commit all the changes in your repository index to your local repository 
```
git commit -m [yyy] BMS: my notes
```
See Odoo doc for the [yyy]: https://odoo.com/documentation/17.0/contributing/development/git_guidelines.html#tag-and-module-name
3. Push to the master  git repository. It will update the code on Odoo.sh
```
git push
```
Note that you can change the `settings` in Odoo.sh to activate the rebuild of the code at each new push.
### Pass from staging to prod ###
Just drag and drop your staging branch into prod. Choose 'rebase and merge' to keep track on the commits. 
<br>Note:
* If you get an error `pull request already existing`, it is because you have already merge and base the branch in staging a same name
* Don't forget to update your module (`app>update`) or change the version in the ``manifest.py``

# TODO # 
## Technical ##
- [x] lazy loading for the decomposition to improve loading performance
- [X] create new object
- [x] automatic refresh of decomposition
- [x] change parent via drag&drop on decomposition
- [x] look&feel attributes
- [x] hover defintion attibutes
- [ ] make the import mechanism of awv list ("keuzelijsten") better by taking into account the status change (don't  know if it happens but 
theoritically it could)
- [x] fix tree_level which should be filled in (after having checked it's still useful)
- [ ] keep common attributes when user changes of type
- [ ] quid managing_level_obj_id if there are several decompositions? 


## Migration ##
- [x] internal_id -> unique constraint


## Governance ##
- [x] Unique ID asset format -> decision: MO-xxx
- [ ] Quid awv type not found -> use OTL lantis (and potentially create a new type? ) + problem no attribute in Relatics (no meta-model)
- [ ] quid versionning AWV type ? by object or by "sqlite" model
- [ ] check status of values for the value lists (oslo enumeration)?
- [x] logo app
- [x] icons decomposition

## Refactoring ##
- [x] delete modle oslo_generic_model
- [x] attribute_value.py + views + menus + security
- [x] delete demo_agent.py
- [ ] remove bms_msa_object model, table, menu + field msa_object_id from maintainance_object.py (and table)
- [ ] change oslo datatype in CONSTANT VALUE defined on one place
- [ ] owl components implements props validation
- [ ] use of AWV OWL library type hardcoded in .js code
- [ ] store json of get_att_def() instead of recalulate on the fly to increase loading speed
- [ ] change res_id by default of `bms_decomposition_action`
- [ ] `get_oslo_attr_def` of `object_type.py`
- [x] change view "decomposition type" in order to not display the decomposition_relationships
- [ ] check if get_view() in maintainance_object.py is still useful
- [ ] `bms.maintainance_object._get_children()` use hardcoded ´decomposition_type_id´ for 'OTL AWV'
- [ ] At creation, display which managing organisation the future will inherit if it is not an 'managing level' (and probaly the same for the ownership)
