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
    ],
    "assets": {
        # "web.assets_frontend": [
        #     "web/static/lib/bootstrap/js/*",
        #     "web/static/lib/bootstrap/scss/*",
        # ],
        "web.assets_backend": [
            "bms/static/src/**/*",
        ],
    },
    "application": True,
    "license": "LGPL-3",
    "auto-install": True,
}
