from datetime import datetime

data = [
    {'id': 1, 'name': 'https://example.com',
     'last_check':  datetime.strptime("12.02.2025 12:57", "%d.%m.%Y %H:%M"),
     'response_code': 200},
    {'id': 2, 'name': 'https://guugle.net',
     'last_check':  datetime.strptime("14.02.2025 23:13", "%d.%m.%Y %H:%M"),
     'response_code': 404},
]