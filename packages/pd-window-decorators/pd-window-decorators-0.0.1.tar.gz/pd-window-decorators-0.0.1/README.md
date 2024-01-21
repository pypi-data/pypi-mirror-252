# pd-window-decorators

Easily apply windowing to functions that mutate Pandas DataFrames. Useful for data science projects where you want to apply a function for a DataFrame using smaller chunks of the DataFrame automatically. A moving window can be easily applied to the function using Python decorators.

## Sliding Window

To apply a sliding window, import `df_sliding_window` from `pd_window_decorators` and apply it to your function. The decorator takes a `timedelta` object as a required argument to define the slice size. By default, the decorator will look for a Pandas DataFrame named `df` in the function arguments. The DataFrame must also have a time column. The column name is `ds` by default. The decorator also expects the function to return a DataFrame.

### Example

Using the decorator with default arguments:

```python
@df_sliding_window(window_size=timedelta(days=2))
def sum_all(df):
    df.loc[:, 'sum'] = df['y'].sum()
    return df
```

Using the decorator with custom arguments:

```python
@df_sliding_window(window_size=timedelta(days=2), df_name='my_df', time_column='my_time')
def sum_all(my_df):
    df.loc[:, 'sum'] = df['y'].sum()
    return df
```

Note that in the second example, the DataFrame is named `my_df` and the `df_name` argument is set to `my_df`, so they match.

### Arguments

| Argument | Type | Optional | Description |
| --- | --- | --- | --- |
| `window_size` | `timedelta` | `True` | The size of the window to apply to the function. |
| `df_name` | `str` | `False` | The name of the DataFrame variable to pass to the function as an argument. Defaults to `df`. |
| `time_column` | `str` | `False` | The name of the column in the DataFrame that contains the time information. Defaults to `ds`. |