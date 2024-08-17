import pytest

FULL_INSTALLATION_MARKER = 'full_installation'
MINIMAL_INSTALLATION_MARKER = 'minimal_installation'


def pytest_addoption(parser):
    parser.addoption(
        '--without-extra-dependencies', action='store_true', default=False,
        help='Run tests assuming extra dependencies are not installed'
    )


def pytest_configure(config):
    config.addinivalue_line('markers', f'{FULL_INSTALLATION_MARKER}: Test requires optional dependencies')
    config.addinivalue_line('markers',
                            f'{MINIMAL_INSTALLATION_MARKER}: Test requires optional dependencies to be absent')


def pytest_collection_modifyitems(config, items):
    if config.getoption('--without-extra-dependencies'):
        skip_extra_dependencies = pytest.mark.skip(reason='Skipping test requiring extra dependencies')
        for item in items:
            if FULL_INSTALLATION_MARKER in item.keywords:
                item.add_marker(skip_extra_dependencies)
    else:
        skip_extra_dependencies = pytest.mark.skip(reason='Skipping tests requiring extra dependencies to be absent')
        for item in items:
            if MINIMAL_INSTALLATION_MARKER in item.keywords:
                item.add_marker(skip_extra_dependencies)
