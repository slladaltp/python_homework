import pytest

pytest_plugins = ('celery.contrib.pytest', )

@pytest.fixture(scope='session')
def celery_config():
    return {
        'broker_url': 'redis://localhost:8001',
        'result_backend': 'redis://localhost:8001'
    }