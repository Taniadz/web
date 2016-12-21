CONFIG = {
    'mode': 'django',
    'working_dir': '/home/box/web/ask/ask',
    'args': (
        '--bind=0.0.0.0:8080',
        '--workers=4',
        '--timeout=60',
        'ask.wsgi'
    )
}
