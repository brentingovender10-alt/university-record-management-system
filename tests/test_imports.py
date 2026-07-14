import sys
sys.path.insert(0, 'src')

import importlib

MODULES = [
    'urms.database', 'urms.demo_db', 'urms.theme',
    'Dashboard', 'pages.1_Students', 'pages.2_Lecturers', 'pages.4_Courses', 'pages.8_Query_Builder'
]


def test_modules_import():
    for m in MODULES:
        mod = importlib.import_module(m)
        assert mod is not None
