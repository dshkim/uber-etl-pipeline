CREATE OR REPLACE TABLE my-test-project-433607.uber_de_dataset.analytics_table AS (
  SELECT
    f_dim.VendorID,
    dt_dim.tpep_pickup_datetime,
    dt_dim.tpep_dropoff_datetime,
    pu_dim.pickup_latitude,
    pu_dim.pickup_longitude,
    do_dim.dropoff_latitude,
    do_dim.dropoff_longitude,
    rc_dim.rate_code_name,
    pt_dim.payment_type_name,
    f_dim.passenger_count,
    f_dim.trip_distance,
    f_dim.fare_amount,
    f_dim.extra,
    f_dim.mta_tax,
    f_dim.tip_amount,
    f_dim.tolls_amount,
    f_dim.improvement_surcharge,
    f_dim.total_amount
  FROM
    my-test-project-433607.uber_de_dataset.fact_table AS f_dim
  JOIN
    my-test-project-433607.uber_de_dataset.datetime_dim AS dt_dim
    ON f_dim.datetime_id = dt_dim.datetime_id
  JOIN
    my-test-project-433607.uber_de_dataset.pickup_location_dim AS pu_dim
    ON f_dim.pickup_location_id = pu_dim.pickup_location_id
  JOIN
    my-test-project-433607.uber_de_dataset.dropoff_location_dim AS do_dim
    ON f_dim.dropoff_location_id = do_dim.dropoff_location_id
  JOIN
    my-test-project-433607.uber_de_dataset.rate_code_dim AS rc_dim
    ON f_dim.rate_code_id = rc_dim.rate_code_id
  JOIN
    my-test-project-433607.uber_de_dataset.payment_type_dim AS pt_dim
    ON f_dim.payment_type_id = pt_dim.payment_type_id);