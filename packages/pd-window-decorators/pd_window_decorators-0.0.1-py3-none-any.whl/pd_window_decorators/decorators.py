from datetime import timedelta
from functools import wraps
import inspect
import pandas as pd
from pandas.api.types import is_datetime64_ns_dtype

def df_sliding_window(window_size: timedelta, df_name: str = 'df', time_column: str = 'ds'):
    '''
    Decorator for applying a sliding window to a function that consumes and returns a DataFrame.

    Parameters:
    - window_size (timedelta): The size of the sliding window.
    - df_name (str): The name of the DataFrame parameter in the decorated function. Defaults to 'df'.
    - time_column (str): The name of the time column in the DataFrame. Defaults to 'ds'.

    Returns:
    Callable: A decorator that can be applied to a function expecting a DataFrame with a time column.

    Note:
    - The results are concatenated into a single DataFrame and returned.

    Raises:
    - ValueError: If the provided DataFrame is empty, lacks a time column column, has a non-datetime time column column, or if the decorated function does not return a DataFrame.
    - TypeError: If the window_size parameter is not a timedelta object.

    Example:
    ```python
    @df_sliding_window(window_size=timedelta(days=7))
    def process_weekly_data(df):
        # Processing logic here
        return processed_df
    ```

    The decorator automatically divides the input DataFrame into sliding windows and concatenates the results.

    '''
    def __run_multiple_times(func):
        @wraps(func)
        def __wrapper(*args, **kwargs):
            _args = inspect.signature(func).bind(*args, **kwargs)
            _args.apply_defaults()
            df = _args.arguments[df_name]
            
            # Check if the provided DataFrame is empty
            if df.empty:
                raise ValueError('No dataframe provided in the decorated function')
            
            # Check if the DataFrame has a time_column column and if it is of datetime dtype
            if time_column not in df.columns or not is_datetime64_ns_dtype(df[time_column]):
                raise ValueError(f'Dataframe in the decorated function does not have a "{time_column}" (timestamp) column')
            
            # Check if the decorated function returns a DataFrame
            if not isinstance(func(*_args.args, **_args.kwargs), pd.DataFrame):
                raise ValueError('Decorated function does not return a dataframe')
            
            # Get the first and last timestamps in the DataFrame
            first_timestamp = df[time_column].iloc[0]
            last_timestamp = df[time_column].iloc[-1]
            
            # Create a list of timestamps that are window_size apart
            timestamps = pd.date_range(start=first_timestamp, end=last_timestamp, freq=window_size)
            
            # Create a list of dataframes that are window_size apart
            dfs = [df[(df[time_column] >= timestamp) & (df[time_column] < timestamp + window_size)] for timestamp in timestamps]
            _args.arguments[df_name] = dfs[0]
            results = []
            
            # Process each window individually and collect the results
            for df in dfs:
                _args.arguments[df_name] = df
                result = func(*_args.args, **_args.kwargs)
                results.append(result)
            
            # Concatenate the results into a single DataFrame and return
            return pd.concat(results)
        return __wrapper
    return __run_multiple_times