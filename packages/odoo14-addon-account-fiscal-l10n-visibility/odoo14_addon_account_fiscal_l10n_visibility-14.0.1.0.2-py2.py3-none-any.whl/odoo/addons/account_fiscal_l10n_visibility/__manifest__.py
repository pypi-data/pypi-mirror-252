# -*- coding: utf-8 -*-
{
    'name': "account_fiscal_l10n_visibility",

    'summary': """
        Enhances fiscal localization settings in Odoo by customizing visibility and editability based on existing accounting entries.""",

    'description': """
        Shows the fiscal localization settings in read-only mode where accounting entries exist. The default behavior is to hide completely this section.
    """,

    'author': "Coopdevs",

    'website': "https://git.coopdevs.org/coopdevs/odoo/odoo-addons/odoo14-addons",

    'Project-URL': "Bug Tracker, https://git.coopdevs.org/coopdevs/odoo/odoo-addons/odoo14-addons/-/issues",

    'category': 'Accounting',

    'version': '14.0.1.0.2',

    'depends': ['base', 'account'],

    'data': [
        'views/account_settings_views.xml',
    ],
}
