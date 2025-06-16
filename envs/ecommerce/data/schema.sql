-- 1. Supplier
CREATE TABLE Supplier (
  supplier_id   VARCHAR(8)   PRIMARY KEY,
  name          VARCHAR(100) NOT NULL,
  contact_email VARCHAR(100),
  address       VARCHAR(200),
  city          VARCHAR(50),
  state         VARCHAR(20),
  zip_code      VARCHAR(10),
  country       VARCHAR(50)
);

-- 2. Product
CREATE TABLE Product (
  product_id    VARCHAR(8)   PRIMARY KEY,
  name          VARCHAR(100) NOT NULL,
  description   TEXT,
  supplier_id   VARCHAR(8)   REFERENCES Supplier(supplier_id),
  unit_price    DECIMAL(9,2) NOT NULL
);

-- 3. User (Customer)
CREATE TABLE "User" (
  user_id       VARCHAR(8)   PRIMARY KEY,
  first_name    VARCHAR(50),
  last_name     VARCHAR(50),
  email         VARCHAR(100) UNIQUE,
  address       VARCHAR(200),
  city          VARCHAR(50),
  state         VARCHAR(20),
  zip_code      VARCHAR(10),
  country       VARCHAR(50)
);

-- 4. Purchase Order
CREATE TABLE PurchaseOrder (
  purchase_order_id VARCHAR(8) PRIMARY KEY,
  supplier_id       VARCHAR(8) REFERENCES Supplier(supplier_id),
  order_date        DATE      NOT NULL
);

-- 5. Purchase Order Item
CREATE TABLE PurchaseOrderItem (
  po_item_id        VARCHAR(10) PRIMARY KEY,
  purchase_order_id VARCHAR(8)  REFERENCES PurchaseOrder(purchase_order_id),
  product_id        VARCHAR(8)  REFERENCES Product(product_id),
  quantity          INTEGER     NOT NULL,
  unit_cost         DECIMAL(9,2) NOT NULL
);

-- 6. Sales Order
CREATE TABLE SalesOrder (
  sales_order_id VARCHAR(8) PRIMARY KEY,
  user_id        VARCHAR(8) REFERENCES "User"(user_id),
  order_date     DATE      NOT NULL,
  status         VARCHAR(20)
);

-- 7. Sales Order Item
CREATE TABLE SalesOrderItem (
  so_item_id      VARCHAR(10) PRIMARY KEY,
  sales_order_id  VARCHAR(8)  REFERENCES SalesOrder(sales_order_id),
  product_id      VARCHAR(8)  REFERENCES Product(product_id),
  quantity        INTEGER     NOT NULL
);