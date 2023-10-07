{
    "name": "bms",
    "version": "0.0.2",
    "sequence": 1,
    "category": "asset",
    "author": "frederic.vigin@engiforce.com",
    "summary": "Asset Beheermanagement Systeem",
    "dascription": """POC to evaluate odoo as target tool for the BMS""",
    "demo": [],
    "depends": ["base", "web"],
    "data": [
        "views/view.xml",
        "security/ir.model.access.csv",
        "wizards/otl_type_view.xml"
    ],
    "assets": {
        "web.assets_backend": [
            "bms/static/src/**/*",
            
        ],
        "web.assets_common":[
            "bms/static/lib/fancytree/js/jquery.fancytree-all-deps.js",
            "bms/static/lib/fancytree/css/skin-odoo-bms/ui.fancytree.css",
        ]
    },
    "application": True,
    "license": "LGPL-3",
    "auto-install": True,
}
