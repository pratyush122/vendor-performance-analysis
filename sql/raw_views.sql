CREATE OR REPLACE VIEW raw_begin_inventory AS
SELECT
    InventoryId AS inventory_id,
    TRY_CAST(Store AS INTEGER) AS store_id,
    City AS city,
    TRY_CAST(Brand AS INTEGER) AS brand_id,
    TRIM(Description) AS description,
    TRIM(Size) AS size,
    TRY_CAST(onHand AS DOUBLE) AS on_hand,
    TRY_CAST(Price AS DOUBLE) AS retail_price,
    TRY_CAST(startDate AS DATE) AS snapshot_date
FROM read_csv('{{ begin_inventory_csv }}', header = true, all_varchar = true);

CREATE OR REPLACE VIEW raw_end_inventory AS
SELECT
    InventoryId AS inventory_id,
    TRY_CAST(Store AS INTEGER) AS store_id,
    City AS city,
    TRY_CAST(Brand AS INTEGER) AS brand_id,
    TRIM(Description) AS description,
    TRIM(Size) AS size,
    TRY_CAST(onHand AS DOUBLE) AS on_hand,
    TRY_CAST(Price AS DOUBLE) AS retail_price,
    TRY_CAST(endDate AS DATE) AS snapshot_date
FROM read_csv('{{ end_inventory_csv }}', header = true, all_varchar = true);

CREATE OR REPLACE VIEW raw_purchase_prices AS
SELECT
    TRY_CAST(Brand AS INTEGER) AS brand_id,
    TRIM(Description) AS description,
    TRY_CAST(Price AS DOUBLE) AS retail_price,
    TRIM(Size) AS size,
    TRY_CAST(Volume AS DOUBLE) AS volume_ml,
    TRY_CAST(Classification AS INTEGER) AS classification,
    TRY_CAST(PurchasePrice AS DOUBLE) AS purchase_price_reference,
    TRY_CAST(VendorNumber AS INTEGER) AS vendor_number,
    TRIM(VendorName) AS vendor_name
FROM read_csv('{{ purchase_prices_csv }}', header = true, all_varchar = true);

CREATE OR REPLACE VIEW raw_purchases AS
SELECT
    InventoryId AS inventory_id,
    TRY_CAST(Store AS INTEGER) AS store_id,
    TRY_CAST(Brand AS INTEGER) AS brand_id,
    TRIM(Description) AS description,
    TRIM(Size) AS size,
    TRY_CAST(VendorNumber AS INTEGER) AS vendor_number,
    TRIM(VendorName) AS vendor_name,
    TRY_CAST(PONumber AS BIGINT) AS po_number,
    TRY_CAST(PODate AS DATE) AS po_date,
    TRY_CAST(ReceivingDate AS DATE) AS receiving_date,
    TRY_CAST(InvoiceDate AS DATE) AS invoice_date,
    TRY_CAST(PayDate AS DATE) AS pay_date,
    TRY_CAST(PurchasePrice AS DOUBLE) AS purchase_price,
    TRY_CAST(Quantity AS DOUBLE) AS purchase_quantity,
    TRY_CAST(Dollars AS DOUBLE) AS purchase_dollars,
    TRY_CAST(Classification AS INTEGER) AS classification
FROM read_csv('{{ purchases_csv }}', header = true, all_varchar = true);

CREATE OR REPLACE VIEW raw_sales AS
SELECT
    InventoryId AS inventory_id,
    TRY_CAST(Store AS INTEGER) AS store_id,
    TRY_CAST(Brand AS INTEGER) AS brand_id,
    TRIM(Description) AS description,
    TRIM(Size) AS size,
    TRY_CAST(SalesQuantity AS DOUBLE) AS sales_quantity,
    TRY_CAST(SalesDollars AS DOUBLE) AS sales_dollars,
    TRY_CAST(SalesPrice AS DOUBLE) AS sales_price,
    TRY_CAST(SalesDate AS DATE) AS sales_date,
    TRY_CAST(Volume AS DOUBLE) AS volume_ml,
    TRY_CAST(Classification AS INTEGER) AS classification,
    TRY_CAST(ExciseTax AS DOUBLE) AS excise_tax,
    TRY_CAST(VendorNo AS INTEGER) AS vendor_number,
    TRIM(VendorName) AS vendor_name
FROM read_csv('{{ sales_csv }}', header = true, all_varchar = true);

CREATE OR REPLACE VIEW raw_vendor_invoice AS
SELECT
    TRY_CAST(VendorNumber AS INTEGER) AS vendor_number,
    TRIM(VendorName) AS vendor_name,
    TRY_CAST(InvoiceDate AS DATE) AS invoice_date,
    TRY_CAST(PONumber AS BIGINT) AS po_number,
    TRY_CAST(PODate AS DATE) AS po_date,
    TRY_CAST(PayDate AS DATE) AS pay_date,
    TRY_CAST(Quantity AS DOUBLE) AS quantity,
    TRY_CAST(Dollars AS DOUBLE) AS dollars,
    TRY_CAST(Freight AS DOUBLE) AS freight,
    NULLIF(TRIM(Approval), '') AS approval_status
FROM read_csv('{{ vendor_invoice_csv }}', header = true, all_varchar = true);
