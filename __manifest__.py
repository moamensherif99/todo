{
    'name': 'Todo',
    'author': 'Moamen Sherif Abdelkader',
    'version': '18.0.1.0',
    'depends': ['base', 'mail',
                ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'reports/todo_report.xml',
        'wizard/assign_task_wizard.xml',
        'views/todo_view.xml',
        'views/base_menu.xml',
    ],
    'application': True,
}
