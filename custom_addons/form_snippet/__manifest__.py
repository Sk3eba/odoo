{
    'name': 'Custom Form Snippet',
    'category': 'Website/Website',
    'version': '1.0',
    'depends': ['website'],
    'data': [
        'views/snippets/s_custom_form.xml',
        'views/snippets/snippets.xml',
        'views/snippets/options.xml',
    ],
    'assets': {
        # Front-end: To widzi użytkownik, tu ładuje się skrypt obsługujący przeciąganie i style
        'web.assets_frontend': [
            'form_snippet/static/src/snippets/s_custom_form/000.scss',
            'form_snippet/static/src/snippets/s_custom_form/000.js',
        ],
        # Backend/Wysiwyg: Logika edytora opcji oraz ładowanie struktury w locie z XML
        'website.assets_wysiwyg': [
            'form_snippet/static/src/snippets/s_custom_form/000.xml',
            'form_snippet/static/src/snippets/s_custom_form/options.js',
        ],
    },
    'license': 'LGPL-3',
}