-- TODO: This query will return a table with the differences between the real 
-- and estimated delivery times by month and year. It will have different 
-- columns: month_no, with the month numbers going from 01 to 12; month, with 
-- the 3 first letters of each month (e.g. Jan, Feb); Year2016_real_time, with 
-- the average delivery time per month of 2016 (NaN if it doesn't exist); 
-- Year2017_real_time, with the average delivery time per month of 2017 (NaN if 
-- it doesn't exist); Year2018_real_time, with the average delivery time per 
-- month of 2018 (NaN if it doesn't exist); Year2016_estimated_time, with the 
-- average estimated delivery time per month of 2016 (NaN if it doesn't exist); 
-- Year2017_estimated_time, with the average estimated delivery time per month 
-- of 2017 (NaN if it doesn't exist) and Year2018_estimated_time, with the 
-- average estimated delivery time per month of 2018 (NaN if it doesn't exist).
-- HINTS
-- 1. You can use the julianday function to convert a date to a number.
-- 2. order_status == 'delivered' AND order_delivered_customer_date IS NOT NULL
-- 3. Take distinct order_id.

WITH CTE AS (
    SELECT
        strftime('%m', order_delivered_customer_date) AS month_no,
        CASE
            WHEN strftime('%m', order_delivered_customer_date) = '01' THEN 'Jan'
            WHEN strftime('%m', order_delivered_customer_date) = '02' THEN 'Feb'
            WHEN strftime('%m', order_delivered_customer_date) = '03' THEN 'Mar'
            WHEN strftime('%m', order_delivered_customer_date) = '04' THEN 'Apr'
            WHEN strftime('%m', order_delivered_customer_date) = '05' THEN 'May'
            WHEN strftime('%m', order_delivered_customer_date) = '06' THEN 'Jun'
            WHEN strftime('%m', order_delivered_customer_date) = '07' THEN 'Jul'
            WHEN strftime('%m', order_delivered_customer_date) = '08' THEN 'Aug'
            WHEN strftime('%m', order_delivered_customer_date) = '09' THEN 'Sep'
            WHEN strftime('%m', order_delivered_customer_date) = '10' THEN 'Oct'
            WHEN strftime('%m', order_delivered_customer_date) = '11' THEN 'Nov'
            WHEN strftime('%m', order_delivered_customer_date) = '12' THEN 'Dec'
        END AS month,
        strftime('%Y', order_delivered_customer_date) AS year,
        julianday(order_delivered_customer_date) - julianday(order_purchase_timestamp) AS real_time,
        julianday(order_estimated_delivery_date) - julianday(order_purchase_timestamp) AS estimated_time
    FROM olist_orders
    WHERE order_status = 'delivered' AND order_delivered_customer_date IS NOT NULL
),
RealTime AS (
    SELECT
        month_no,
        month,
        year,
        AVG(real_time) AS avg_real_time
    FROM CTE
    WHERE year IN ('2016', '2017', '2018')
    GROUP BY month_no, month, year
),
EstimatedTime AS (
    SELECT
        month_no,
        month,
        year,
        AVG(estimated_time) AS avg_estimated_time
    FROM CTE
    WHERE year IN ('2016', '2017', '2018')
    GROUP BY month_no, month, year
),
Merged AS (
    SELECT
        rt.month_no,
        rt.month,
        rt.year AS real_year,
        et.year AS estimated_year,
        rt.avg_real_time,
        et.avg_estimated_time
    FROM RealTime rt
    FULL OUTER JOIN EstimatedTime et
    ON rt.month_no = et.month_no AND rt.year = et.year
)
SELECT
    month_no,
    month,
    MAX(CASE WHEN real_year = '2016' THEN avg_real_time END) AS Year2016_real_time,
    MAX(CASE WHEN real_year = '2017' THEN avg_real_time END) AS Year2017_real_time,
    MAX(CASE WHEN real_year = '2018' THEN avg_real_time END) AS Year2018_real_time,
    MAX(CASE WHEN estimated_year = '2016' THEN avg_estimated_time END) AS Year2016_estimated_time,
    MAX(CASE WHEN estimated_year = '2017' THEN avg_estimated_time END) AS Year2017_estimated_time,
    MAX(CASE WHEN estimated_year = '2018' THEN avg_estimated_time END) AS Year2018_estimated_time
FROM Merged
GROUP BY month_no, month
ORDER BY month_no;