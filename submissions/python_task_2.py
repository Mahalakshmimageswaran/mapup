import pandas as pd


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic hereimport pandas as pd

def calculate_distance_matrix(filename):
    
    df = pd.read_csv(filename)
    unique_ids = df['id_start'].unique().tolist()
    distance_matrix = {}


    for id1 in unique_ids:
        distance_matrix[id1] = {}
        for id2 in unique_ids:
            
            if id1 == id2:
                distance_matrix[id1][id2] = 0
            else:
                # Retrieve the known distance between id1 and id2 from the dataset
                distance = df[(df['id_start'] == id1) & (df['id_end'] == id2)]['distance'].values
                
                if len(distance) > 0:
                    distance_matrix[id1][id2] = distance[0]
                else:
                    # If no direct distance was found, calculate the distance using a known route
                    for id3 in unique_ids:
                        if id3 != id1 and id3 != id2:
                          distance1 = df[(df['id_start'] == id1) & (df['id_start'] == id3)]['distance'].values
                          distance2 = df[(df['id_start'] == id3) & (df['id_end'] == id2)]['distance'].values
                          if len(distance1) > 0 and len(distance2) > 0:
                            distance_matrix[id1][id2] = distance1[0] + distance2[0]
                            break

   
    result = pd.DataFrame(distance_matrix)

   
    result.fillna(0, inplace=True)

    return result


filename = 'dataset-3.csv'
distance_matrix = calculate_distance_matrix(filename)
print(distance_matrix)

return df


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    distance_matrix_reset = distance_matrix.reset_index()
    unrolled_df = pd.melt(
        distance_matrix_reset, id_vars=['id_start'], var_name='id_end', value_name='distance'
    )
    unrolled_df['id_end'] = unrolled_df['id_end'].astype(distance_matrix.index.dtype)
    unrolled_df = unrolled_df[unrolled_df['id_start'] != unrolled_df['id_end']]

    return unrolled_df

unrolled_df = unroll_distance_matrix(result_matrix)
print(unrolled_df)
return df


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here
   
    reference_df = unrolled_df[unrolled_df['id_start'] == reference_value]
    reference_avg_distance = reference_df['distance'].mean()
    threshold_range = 0.1 * reference_avg_distance
    selected_ids = unrolled_df[
        (unrolled_df['distance'] >= reference_avg_distance - threshold_range) &
        (unrolled_df['distance'] <= reference_avg_distance + threshold_range)
    ]['id_start'].unique()
    selected_ids.sort()

    return selected_ids

reference_value = 1001400


selected_ids = find_ids_within_ten_percentage_threshold(unrolled_df, reference_value)
print(selected_ids)

return df


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        df[vehicle_type] = df['distance'] * rate_coefficient

result_with_toll_rates = calculate_toll_rate(unrolled_df)
print(result_with_toll_rates)
return df


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    

    weekday_time_ranges = [(time(0, 0, 0), time(10, 0, 0)),
                           (time(10, 0, 0), time(18, 0, 0)),
                           (time(18, 0, 0), time(23, 59, 59))]

    weekend_time_ranges = [(time(0, 0, 0), time(23, 59, 59))]

    weekday_discount_factors = [0.8, 1.2, 0.8]
    weekend_discount_factor = 0.7

    
    df['time_based_toll'] = 0.0  # Initialize with 0.0

    
    for time_range, discount_factor in zip(weekday_time_ranges, weekday_discount_factors):
        mask = (df['start_time'] >= time_range[0]) & (df['start_time'] <= time_range[1])
        df.loc[mask, 'time_based_toll'] = df.loc[mask, 'time_based_toll'] + discount_factor * df['distance']

    for time_range in weekend_time_ranges:
        mask = (df['start_time'] >= time_range[0]) & (df['start_time'] <= time_range[1])
        df.loc[mask, 'time_based_toll'] = df.loc[mask, 'time_based_toll'] + weekend_discount_factor * df['distance']

    


result_with_time_based_toll_rates = calculate_time_based_toll_rates(result_with_toll_rates)
print(result_with_time_based_toll_rates)
return df
