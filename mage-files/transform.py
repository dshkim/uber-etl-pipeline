import pandas as pd
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(df, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here

    df = df.drop(columns=['Unnamed: 0'])

    # Ensure proper conversion to datetime
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])

    df = df.drop_duplicates().reset_index(drop=True)
    df['trip_id'] = df.index

    #Create datetime_dim table
    datetime_dim = df[['tpep_pickup_datetime','tpep_dropoff_datetime']].reset_index(drop=True)
    #Add pickup data
    datetime_dim['tpep_pickup_datetime'] = datetime_dim['tpep_pickup_datetime']
    datetime_dim['pickup_year'] = datetime_dim['tpep_pickup_datetime'].dt.year
    datetime_dim['pickup_month'] = datetime_dim['tpep_pickup_datetime'].dt.month
    datetime_dim['pickup_weekday'] = datetime_dim['tpep_pickup_datetime'].dt.weekday
    datetime_dim['pickup_day'] = datetime_dim['tpep_pickup_datetime'].dt.day
    datetime_dim['pickup_hour'] = datetime_dim['tpep_pickup_datetime'].dt.hour
    #Add dropoff data
    datetime_dim['tpep_dropoff_datetime'] = datetime_dim['tpep_dropoff_datetime']
    datetime_dim['dropoff_year'] = datetime_dim['tpep_dropoff_datetime'].dt.year
    datetime_dim['dropoff_month'] = datetime_dim['tpep_dropoff_datetime'].dt.month
    datetime_dim['dropoff_weekday'] = datetime_dim['tpep_dropoff_datetime'].dt.weekday
    datetime_dim['dropoff_day'] = datetime_dim['tpep_dropoff_datetime'].dt.day
    datetime_dim['dropoff_hour'] = datetime_dim['tpep_dropoff_datetime'].dt.hour

    #Add datetime_id
    datetime_dim['datetime_id'] = datetime_dim.index


    #Format datetime_dim table
    datetime_dim = datetime_dim[['datetime_id', 'tpep_pickup_datetime', 'pickup_year', 'pickup_month', 'pickup_weekday', 'pickup_day', 'pickup_hour',
                                'tpep_dropoff_datetime', 'dropoff_year', 'dropoff_month', 'dropoff_weekday', 'dropoff_day', 'dropoff_hour']]

    #Create pickup_location_dim table
    pickup_location_dim = df[['pickup_longitude', 'pickup_latitude']].reset_index(drop=True)
    pickup_location_dim['pickup_location_id'] = pickup_location_dim.index
    pickup_location_dim = pickup_location_dim[['pickup_location_id','pickup_latitude','pickup_longitude']] 

    #Create dropoff_location_dim table
    dropoff_location_dim = df[['dropoff_longitude', 'dropoff_latitude']].reset_index(drop=True)
    dropoff_location_dim['dropoff_location_id'] = dropoff_location_dim.index
    dropoff_location_dim = dropoff_location_dim[['dropoff_location_id','dropoff_latitude','dropoff_longitude']]

    rate_code_type = {
    1:"Standard rate",
    2:"JFK",
    3:"Newark",
    4:"Nassau or Westchester",
    5:"Negotiated fare",
    6:"Group ride"
    }

    #Create rate_code_dim table
    rate_code_dim = df[['RatecodeID']].reset_index(drop=True)
    rate_code_dim['rate_code_id'] = rate_code_dim.index
    rate_code_dim['rate_code_name'] = rate_code_dim['RatecodeID'].map(rate_code_type)
    rate_code_dim = rate_code_dim[['rate_code_id','RatecodeID','rate_code_name']]

    payment_type_name = {
    1:"Credit card",
    2:"Cash",
    3:"No charge",
    4:"Dispute",
    5:"Unknown",
    6:"Voided trip"
    }

    #Create payment_type_dim
    payment_type_dim = df[['payment_type']].reset_index(drop=True)
    payment_type_dim['payment_type_id'] = payment_type_dim.index
    payment_type_dim['payment_type_name'] = payment_type_dim['payment_type'].map(payment_type_name)
    payment_type_dim = payment_type_dim[['payment_type_id','payment_type','payment_type_name']]

    fact_table = df.merge(datetime_dim, left_on='trip_id', right_on='datetime_id') \
               .merge(pickup_location_dim, left_on='trip_id', right_on='pickup_location_id') \
               .merge(dropoff_location_dim, left_on='trip_id', right_on='dropoff_location_id') \
               .merge(rate_code_dim, left_on='trip_id', right_on='rate_code_id') \
               .merge(payment_type_dim, left_on='trip_id', right_on='payment_type_id') \
             [['trip_id','VendorID', 'datetime_id', 'pickup_location_id', 'dropoff_location_id',
               'rate_code_id', 'payment_type_id' , 'passenger_count', 'trip_distance',
               'fare_amount', 'extra', 'mta_tax', 'tip_amount', 'tolls_amount',
               'improvement_surcharge', 'total_amount']]

    return {"datetime_dim":datetime_dim,
    "pickup_location_dim":pickup_location_dim,
    "dropoff_location_dim":dropoff_location_dim,
    "rate_code_dim":rate_code_dim,
    "payment_type_dim":payment_type_dim,
    "fact_table":fact_table}


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
