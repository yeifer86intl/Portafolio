-- TODO: This query will return a table with the revenue by month and year. It
-- will have different columns: month_no, with the month numbers going from 01
-- to 12; month, with the 3 first letters of each month (e.g. Jan, Feb);
-- Year2016, with the revenue per month of 2016 (0.00 if it doesn't exist);
-- Year2017, with the revenue per month of 2017 (0.00 if it doesn't exist) and
-- Year2018, with the revenue per month of 2018 (0.00 if it doesn't exist).
SELECT
    strftime('%m', datetime(julianday(o.order_purchase_timestamp))) AS month_no,
    CASE strftime('%m', datetime(julianday(o.order_purchase_timestamp)))
        WHEN '01' THEN 'Jan'
        WHEN '02' THEN 'Feb'
        WHEN '03' THEN 'Mar'
        WHEN '04' THEN 'Apr'
        WHEN '05' THEN 'May'
        WHEN '06' THEN 'Jun'
        WHEN '07' THEN 'Jul'
        WHEN '08' THEN 'Aug'
        WHEN '09' THEN 'Sep'
        WHEN '10' THEN 'Oct'
        WHEN '11' THEN 'Nov'
        WHEN '12' THEN 'Dec'
    END AS month,
    SUM(CASE WHEN strftime('%Y', datetime(julianday(o.order_purchase_timestamp))) = '2016' THEN op.payment_value ELSE 0 END) AS Year2016,
    SUM(CASE WHEN strftime('%Y', datetime(julianday(o.order_purchase_timestamp))) = '2017' THEN op.payment_value ELSE 0 END) AS Year2017,
    SUM(CASE WHEN strftime('%Y', datetime(julianday(o.order_purchase_timestamp))) = '2018' THEN op.payment_value ELSE 0 END) AS Year2018
FROM
    olist_orders o
JOIN
    olist_order_payments op ON o.order_id = op.order_id
WHERE
    strftime('%Y', datetime(julianday(o.order_purchase_timestamp))) IN ('2016', '2017', '2018')
GROUP BY
    month_no, month
ORDER BY
    month_no;