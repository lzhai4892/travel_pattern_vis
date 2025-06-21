import pandas as pd
import pytest


def test_single_row_normalized_width():
    df = pd.DataFrame({'annual_total_trips': [100]})
    min_width = 0.5
    max_width = 10
    min_trips = df['annual_total_trips'].min()
    max_trips = df['annual_total_trips'].max()

    if max_trips == min_trips:
        df['normalized_width'] = (max_width + min_width) / 2
    else:
        df['normalized_width'] = (
            min_width
            + (df['annual_total_trips'] - min_trips)
            * (max_width - min_width)
            / (max_trips - min_trips)
        )

    expected = (max_width + min_width) / 2
    assert df.loc[0, 'normalized_width'] == pytest.approx(expected)
