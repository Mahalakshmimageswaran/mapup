import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here
    car_matrix = df.pivot_table(index='id_1', columns='id_2', values='car', aggfunc='first', fill_value=0)
    np.fill_diagonal(car_matrix.values, 0)

    return car_matrix
result_matrix = generate_car_matrix(df)
print(result_matrix)


return df


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')], labels=['low', 'medium', 'high'], right=False)
    type_count = df['car_type'].value_counts().to_dict()
    sorted_type_count = dict(sorted(type_count.items()))

    return sorted_type_count

result_dict = get_type_count(df)
print(result_dict)

return dict()


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    bus_mean = df['bus'].mean()
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()
    bus_indexes.sort()
    return bus_indexes

result_indexes = get_bus_indexes(df)
print(result_indexes)
return list()


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    route_avg_truck = df.groupby('route')['truck'].mean()
    selected_routes = route_avg_truck[route_avg_truck > 7].index.tolist()
    selected_routes.sort()

    return selected_routes

result_routes = filter_routes(df)
print(result_routes)    

return list()


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    modified_df = df.copy()
    modified_df = modified_df.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    modified_df = modified_df.round(1)

    return modified_df
modified_result_matrix = multiply_matrix(result_matrix)
print(modified_result_matrix)
return matrix


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    try:
        df['start_datetime'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
        df['end_datetime'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])
    except pd.errors.OutOfBoundsDatetime:
        print("Error: Timestamps contain out-of-bounds values.")
        return pd.Series(index=pd.MultiIndex.from_arrays([[], []]), dtype=bool)


    df['start_day_of_week'] = df['start_datetime'].dt.dayofweek
    df['start_hour'] = df['start_datetime'].dt.hour
    df['end_day_of_week'] = df['end_datetime'].dt.dayofweek
    df['end_hour'] = df['end_datetime'].dt.hour

    incorrect_start_timestamps = df.groupby(['id', 'id_2']).apply(lambda group: not (
        set(group['start_day_of_week']) == set(range(7)) and
        set(group['start_hour']) == set(range(24))
    ))

    incorrect_end_timestamps = df.groupby(['id', 'id_2']).apply(lambda group: not (
        set(group['end_day_of_week']) == set(range(7)) and
        set(group['end_hour']) == set(range(24))
    ))

    incorrect_timestamps = incorrect_start_timestamps | incorrect_end_timestamps

    return incorrect_timestamps


result_series = check_timestamp_completeness(df[['id', 'id_2', 'startDay', 'startTime', 'endDay', 'endTime']])
print(result_series)


    return pd.Series()
