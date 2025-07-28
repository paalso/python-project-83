import os
import platform
import sys
from datetime import datetime
from typing import Dict, Optional

from flask import request


def detect_hosting_provider(hostname: str) -> Optional[Dict[str, str]]:
    if hostname.startswith('127.') or 'localhost' in hostname:
        return None

    known_providers = {
        'pythonanywhere.com': {
            'name': 'PythonAnywhere',
            'url': 'https://www.pythonanywhere.com/',
        },
        'vercel.app': {
            'name': 'Vercel',
            'url': 'https://vercel.com/',
        },
        'render.com': {
            'name': 'Render',
            'url': 'https://render.com/',
        },
        'railway.app': {
            'name': 'Railway',
            'url': 'https://railway.app/',
        },
    }

    for domain, info in known_providers.items():
        if hostname.rstrip('/').endswith(domain):
            return info

    return None


def get_debug_info():
    hostname = request.host
    provider = detect_hosting_provider(hostname)

    debug_info = {
        'env': {
            'DEBUG': os.getenv('DEBUG'),
            'ALLOWED_HOSTS': os.getenv('ALLOWED_HOSTS'),
            # ⚠️ DANGEROUS: DATABASE_URL may contain credentials!
            # Avoid exposing in production environments.
            'DATABASE_URL': os.getenv('DATABASE_URL'),
            'TIMEZONE': os.getenv('TIMEZONE'),
        },
        'request': {
            'host': hostname,
            'path': request.path,
            'hosting_provider': provider or {},
            'method': request.method,
            'user_agent': request.user_agent.string,
            'ip': request.remote_addr,
            'lang': request.accept_languages.best or 'unknown',
            'user': 'Anonymous',
        },
        'server': {
            'timestamp': datetime.utcnow().isoformat(),
            'python_version': sys.version,
            'platform': platform.platform(),
        }
    }

    return debug_info
