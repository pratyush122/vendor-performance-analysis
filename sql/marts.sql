CREATE OR REPLACE TABLE stg_purchase_price_reference AS
WITH ranked_prices AS (
    SELECT
        brand_id,
        vendor_number,
        vendor_name,
        description,
        size,
        volume_ml,
        retail_price,
        purchase_price_reference,
        ROW_NUMBER() OVER (
            PARTITION BY brand_id, vendor_number
            ORDER BY purchase_price_reference DESC NULLS LAST, retail_price DESC NULLS LAST
        ) AS row_num
    FROM raw_purchase_prices
)
SELECT
    brand_id,
    vendor_number,
    vendor_name,
    description,
    size,
    volume_ml,
    retail_price,
    purchase_price_reference
FROM ranked_prices
WHERE row_num = 1;

CREATE OR REPLACE TABLE stg_vendor_freight_summary AS
SELECT
    vendor_number,
    MAX(vendor_name) AS vendor_name,
    COUNT(DISTINCT po_number) AS invoice_count,
    SUM(COALESCE(quantity, 0)) AS invoice_quantity,
    SUM(COALESCE(dollars, 0)) AS invoice_dollars,
    SUM(COALESCE(freight, 0)) AS freight_cost,
    SUM(COALESCE(freight, 0)) / NULLIF(SUM(COALESCE(quantity, 0)), 0) AS freight_per_unit
FROM raw_vendor_invoice
GROUP BY vendor_number;

CREATE OR REPLACE TABLE stg_purchase_summary AS
SELECT
    p.vendor_number,
    MAX(p.vendor_name) AS vendor_name,
    p.brand_id,
    MAX(p.description) AS description,
    MAX(p.size) AS size,
    COALESCE(
        MAX(ref.volume_ml),
        TRY_CAST(NULLIF(REGEXP_REPLACE(MAX(p.size), '[^0-9.]', '', 'g'), '') AS DOUBLE)
    ) AS volume_ml,
    MAX(ref.retail_price) AS retail_price,
    MAX(ref.purchase_price_reference) AS purchase_price_reference,
    SUM(p.purchase_quantity) AS total_purchase_quantity,
    SUM(p.purchase_dollars) AS total_purchase_dollars,
    SUM(p.purchase_dollars) / NULLIF(SUM(p.purchase_quantity), 0) AS weighted_purchase_price,
    COUNT(*) AS purchase_rows,
    COUNT(DISTINCT p.po_number) AS purchase_orders,
    MIN(p.po_date) AS first_purchase_date,
    MAX(p.po_date) AS last_purchase_date
FROM raw_purchases AS p
LEFT JOIN stg_purchase_price_reference AS ref
    ON p.brand_id = ref.brand_id
   AND p.vendor_number = ref.vendor_number
WHERE COALESCE(p.purchase_price, 0) > 0
  AND COALESCE(p.purchase_quantity, 0) > 0
GROUP BY p.vendor_number, p.brand_id;

CREATE OR REPLACE TABLE stg_sales_summary AS
SELECT
    vendor_number,
    MAX(vendor_name) AS vendor_name,
    brand_id,
    MAX(description) AS description,
    MAX(size) AS size,
    MAX(volume_ml) AS volume_ml,
    SUM(sales_quantity) AS total_sales_quantity,
    SUM(sales_dollars) AS total_sales_dollars,
    AVG(sales_price) AS avg_sales_price,
    SUM(excise_tax) AS total_excise_tax,
    COUNT(*) AS sales_rows,
    MIN(sales_date) AS first_sales_date,
    MAX(sales_date) AS last_sales_date
FROM raw_sales
WHERE COALESCE(sales_quantity, 0) > 0
  AND COALESCE(sales_dollars, 0) >= 0
GROUP BY vendor_number, brand_id;

CREATE OR REPLACE TABLE stg_inventory_summary AS
WITH begin_inventory AS (
    SELECT
        brand_id,
        SUM(COALESCE(on_hand, 0)) AS begin_on_hand_units
    FROM raw_begin_inventory
    GROUP BY brand_id
),
end_inventory AS (
    SELECT
        brand_id,
        SUM(COALESCE(on_hand, 0)) AS end_on_hand_units
    FROM raw_end_inventory
    GROUP BY brand_id
)
SELECT
    COALESCE(b.brand_id, e.brand_id) AS brand_id,
    COALESCE(b.begin_on_hand_units, 0) AS begin_on_hand_units,
    COALESCE(e.end_on_hand_units, 0) AS end_on_hand_units,
    COALESCE(e.end_on_hand_units, 0) - COALESCE(b.begin_on_hand_units, 0) AS inventory_change_units
FROM begin_inventory AS b
FULL OUTER JOIN end_inventory AS e
    ON b.brand_id = e.brand_id;

CREATE OR REPLACE TABLE mart_vendor_performance AS
WITH vendor_purchase_totals AS (
    SELECT
        vendor_number,
        SUM(total_purchase_dollars) AS vendor_total_purchase_dollars
    FROM stg_purchase_summary
    GROUP BY vendor_number
)
SELECT
    p.vendor_number,
    p.vendor_name,
    p.brand_id,
    p.description,
    p.size,
    p.volume_ml,
    p.retail_price,
    p.purchase_price_reference,
    p.weighted_purchase_price AS purchase_price,
    p.weighted_purchase_price AS unit_purchase_cost,
    p.total_purchase_quantity,
    p.total_purchase_dollars,
    COALESCE(s.total_sales_quantity, 0) AS total_sales_quantity,
    COALESCE(s.total_sales_dollars, 0) AS total_sales_dollars,
    COALESCE(s.avg_sales_price, 0) AS avg_sales_price,
    COALESCE(s.total_excise_tax, 0) AS total_excise_tax,
    COALESCE(f.freight_cost, 0) AS vendor_freight_cost_total,
    COALESCE(f.freight_cost, 0) * p.total_purchase_dollars / NULLIF(v.vendor_total_purchase_dollars, 0) AS freight_cost,
    (
        COALESCE(f.freight_cost, 0) * p.total_purchase_dollars / NULLIF(v.vendor_total_purchase_dollars, 0)
    ) / NULLIF(p.total_purchase_quantity, 0) AS freight_per_unit,
    COALESCE(i.begin_on_hand_units, 0) AS begin_on_hand_units,
    COALESCE(i.end_on_hand_units, 0) AS end_on_hand_units,
    COALESCE(i.inventory_change_units, 0) AS inventory_change_units,
    p.purchase_rows,
    p.purchase_orders,
    COALESCE(s.sales_rows, 0) AS sales_rows,
    p.first_purchase_date,
    p.last_purchase_date,
    s.first_sales_date,
    s.last_sales_date,
    COALESCE(s.total_sales_dollars, 0) - p.total_purchase_dollars AS gross_profit,
    COALESCE(s.total_sales_dollars, 0)
        - p.total_purchase_dollars
        - (COALESCE(f.freight_cost, 0) * p.total_purchase_dollars / NULLIF(v.vendor_total_purchase_dollars, 0)) AS gross_profit_after_freight,
    (COALESCE(s.total_sales_dollars, 0) - p.total_purchase_dollars) / NULLIF(COALESCE(s.total_sales_dollars, 0), 0) * 100 AS profit_margin,
    (
        COALESCE(s.total_sales_dollars, 0)
        - p.total_purchase_dollars
        - (COALESCE(f.freight_cost, 0) * p.total_purchase_dollars / NULLIF(v.vendor_total_purchase_dollars, 0))
    ) / NULLIF(COALESCE(s.total_sales_dollars, 0), 0) * 100 AS net_profit_margin,
    COALESCE(s.total_sales_quantity, 0) / NULLIF(p.total_purchase_quantity, 0) AS stock_turnover,
    COALESCE(s.total_sales_dollars, 0) / NULLIF(p.total_purchase_dollars, 0) AS sales_to_purchase_ratio,
    GREATEST(p.total_purchase_quantity - COALESCE(s.total_sales_quantity, 0), 0) AS unsold_units,
    GREATEST(p.total_purchase_quantity - COALESCE(s.total_sales_quantity, 0), 0) * p.weighted_purchase_price AS unsold_inventory_value,
    COALESCE(s.total_sales_dollars, 0) / NULLIF(COALESCE(s.total_sales_quantity, 0), 0) AS unit_sales_price,
    (COALESCE(s.total_sales_dollars, 0) / NULLIF(COALESCE(s.total_sales_quantity, 0), 0)) - p.weighted_purchase_price AS unit_margin,
    CASE
        WHEN COALESCE(s.total_sales_quantity, 0) = 0 THEN 'No sales'
        WHEN COALESCE(s.total_sales_dollars, 0) - p.total_purchase_dollars < 0 THEN 'Loss making'
        WHEN COALESCE(s.total_sales_quantity, 0) / NULLIF(p.total_purchase_quantity, 0) < 1 THEN 'Slow moving'
        ELSE 'Healthy'
    END AS performance_flag
FROM stg_purchase_summary AS p
LEFT JOIN stg_sales_summary AS s
    ON p.vendor_number = s.vendor_number
   AND p.brand_id = s.brand_id
LEFT JOIN stg_vendor_freight_summary AS f
    ON p.vendor_number = f.vendor_number
LEFT JOIN vendor_purchase_totals AS v
    ON p.vendor_number = v.vendor_number
LEFT JOIN stg_inventory_summary AS i
    ON p.brand_id = i.brand_id;
