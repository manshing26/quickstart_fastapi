ROLE = {
    'admin': 10,
    'user': 1
}
PERMISSION = {
    'users': {
        'show_myself': ['admin', 'user'],
        'update_myself': ['admin', 'user'],
        'list_users': ['admin', 'user'],
        'show_user': ['admin', 'user'],
        'admin_only': ['admin']
    },
    'audit_log': {
        'query': ['admin']
    },
    'test': {
        'full': ['admin', 'user']
    }
}