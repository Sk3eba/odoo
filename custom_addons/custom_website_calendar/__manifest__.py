{
    'name': 'Website Custom Calendar',
    'category': 'Website/Website',
    'version': '18.0.1.0',
    'depends': ['website'],
    'data': [
        'security/ir.model.access.csv',
        'views/backend_views.xml',
        'views/snippets/s_calendar.xml',
        'views/snippets/snippets.xml',
        'views/snippets/options.xml',
    ],
    'assets': {
        # Front-end: CSS, JS kalendarza i szablon OWL
        'web.assets_frontend': [
            'custom_website_calendar/static/src/snippets/s_calendar/000.scss',
            'custom_website_calendar/static/src/snippets/s_calendar/000.js',
            'custom_website_calendar/static/src/snippets/s_calendar/000.xml',
        ],
        # Backend: Rejestracja opcji kalendarza w edytorze
        'website.assets_wysiwyg': [
            'custom_website_calendar/static/src/snippets/s_calendar/options.js',
        ],
    },
    'license': 'LGPL-3',
}