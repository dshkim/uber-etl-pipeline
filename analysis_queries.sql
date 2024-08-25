-- AVG fare amount per vendor
SELECT 
  VendorID, 
  AVG(fare_amount) 
FROM my-test-project-433607.uber_de_dataset.fact_table
GROUP BY VendorID;

-- AVG tip amount for each payment type
SELECT 
  payment.payment_type_name,
  AVG(fact.tip_amount)
FROM my-test-project-433607.uber_de_dataset.fact_table AS fact
JOIN my-test-project-433607.uber_de_dataset.payment_type_dim AS payment
  ON fact.payment_type_id = payment.payment_type_id
GROUP BY payment.payment_type_name;

-- Top 5 busiest pick up time (by hour)
SELECT
  dt.pickup_hour,
  COUNT(dt.datetime_id) as num_pickups
FROM my-test-project-433607.uber_de_dataset.fact_table AS fact
JOIN my-test-project-433607.uber_de_dataset.datetime_dim AS dt
  ON fact.datetime_id = dt.datetime_id
GROUP BY dt.pickup_hour
ORDER BY COUNT(dt.datetime_id) DESC
LIMIT 5;

-- Total # of trips by passenger count
SELECT
  fact.passenger_count,
  COUNT(trip_id) AS number_of_trips
FROM my-test-project-433607.uber_de_dataset.fact_table AS fact
GROUP BY fact.passenger_count
ORDER BY COUNT(trip_id) DESC;

-- Average fare amount by hour of the day
SELECT
  dt.pickup_hour,
  AVG(fact.fare_amount)
FROM my-test-project-433607.uber_de_dataset.fact_table AS fact
JOIN my-test-project-433607.uber_de_dataset.datetime_dim AS dt
  ON fact.datetime_id = dt.datetime_id
GROUP BY dt.pickup_hour
ORDER BY AVG(fact.fare_amount) DESC;