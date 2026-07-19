import sys
sys.path.insert(0, 'src')

from urms import theme
import pandas as pd
import math


def test_cell_none_and_nan():
    assert theme._cell(None) == '—'
    assert theme._cell(float('nan')) == '—'
    assert theme._cell(123) == '123'


def test_stat_card_outputs_html():
    html = theme.stat_card('👥', 'Total Students', 42)
    assert '<div class="urms-card"' in html
    assert 'Total Students' in html
    assert '42' in html
