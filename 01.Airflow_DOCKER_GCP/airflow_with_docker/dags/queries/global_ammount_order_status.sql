-- TODO: This query will return a table with two columns; order_status, and
-- Ammount. The first one will have the different order status classes and the
-- second one the total ammount of each.
SELECT 
    o.order_status,
    SUM(oi.price) AS Ammount
FROM 
    olist_orders o
JOIN 
    olist_order_items oi ON o.order_id = oi.order_id
GROUP BY 
    o.order_status;