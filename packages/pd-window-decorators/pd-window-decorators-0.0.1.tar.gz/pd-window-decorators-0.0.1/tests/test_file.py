from datetime import timedelta
import pandas as pd
from ..src.pd_window_decorators.decorators import df_sliding_window

time_series_df = pd.DataFrame(pd.date_range(start='2020-01-01', end='2020-01-06', freq='1D'), columns=['ds'])
time_series_df['y'] = range(1, len(time_series_df) + 1)

SLIDING_WINDOW_SIZE = timedelta(days=2)

@df_sliding_window(window_size=SLIDING_WINDOW_SIZE)
def sum_all(df):
    df.loc[:, 'sum'] = df['y'].sum()
    return df

def test_successful_window_sum():
    result = sum_all(time_series_df)
    if result.empty:
        assert False
    
    if result['sum'].iloc[0] != 3:
        assert False

    if result['sum'].iloc[1] != 3:
        assert False

    if result['sum'].iloc[2] != 7:
        assert False

    if result['sum'].iloc[3] != 7:
        assert False

    if result['sum'].iloc[4] != 11:
        assert False

    if result['sum'].iloc[5] != 11:
        assert False
