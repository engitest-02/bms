{
    "name": "bms",
    "version": "0.0.4",
    "sequence": 1,
    "category": "asset",
    "author": "frederic.vigin@engiforce.com",
    "summary": "Beheermanagement Systeem",
    "dascription": """Tool om de assets van Lantis te beheren.""",
    "demo": [],
    "depends": ["base", "web"],
    "data": [
        "views/view.xml",
        "views/view_awv.xml",
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "wizards/otl_type_views.xml",
        "wizards/oslo_attributen_value_edit_views.xml"
    ],
    "assets": {
        "web.assets_backend": [
            "bms/static/src/**/*",
            
        ],
        "web.assets_common":[
            "bms/static/lib/fancytree/js/jquery.fancytree-all-deps.js",
            "bms/static/lib/fancytree/js/jquery.fancytree.dnd5",
            "bms/static/lib/fancytree/css/skin-odoo-bms/ui.fancytree.scss",        
        ]
    },
    "application": True,
    "license": "LGPL-3",
    "auto-install": True,
}
