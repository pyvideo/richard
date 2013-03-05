from django.core.management import call_command


def test_generate_data():
    """Make sure ./manage.py generatedata runs."""
    call_command('generatedata')
