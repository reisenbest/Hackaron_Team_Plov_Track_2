#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import os
from django.core.management import execute_from_command_line
from django.contrib.auth.models import User

def create_superuser():
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@admin.com', 'password1234')

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Hackaton_SBER.settings")
    create_superuser()  # Создание суперпользователя перед выполнением других команд
    execute_from_command_line()

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Hackaton_SBER.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
