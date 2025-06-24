#!/usr/bin/env python
"""Entry point for Django's management utility."""

import os
import sys


def main():
    """Run administrative tasks using Django's command line interface."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'memory_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH environment variable?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
