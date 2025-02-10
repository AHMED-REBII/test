# Copyright 2024 OKTEO (<https://www.okteo.fr>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Partner Logo Finder",
    "description": """
        Extends res.partner to validate email and website fields.
        Implements logo fetching from external API.""",
    "author": "OKTEO",
    "website": "https://www.okteo.fr",
    "category": "Extra Tools",
    "version": "17.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["base"],
    "data": [
        "data/partner_logo_finder_data.xml",
        "views/res_partner_view.xml",
    ],
}
