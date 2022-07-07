CREATE TABLE IF NOT EXISTS "product_types" (
  "id" INTEGER PRIMARY KEY,
  "type" string UNIQUE
);

CREATE TABLE IF NOT EXISTS "products" (
  "id" INTEGER PRIMARY KEY,
  "brand" string,
  "product_type_id" integer,
  "kcal" float8,
  "fat" float8,
  "sugar" float8,
  UNIQUE ("brand", "product_type_id"),
  FOREIGN KEY (product_type_id) REFERENCES product_types(id)
);

CREATE TABLE IF NOT EXISTS "supermarkets" (
  "id" INTEGER PRIMARY KEY,
  "name" string UNIQUE,
  "direction" string,
  "opening_hours" string
);

CREATE TABLE IF NOT EXISTS "product_prices" (
  "product_id" integer,
  "supermarket_id" integer,
  "price" float8,
  UNIQUE ("product_id", "supermarket_id"),
  FOREIGN KEY (product_id) REFERENCES products(id),
  FOREIGN KEY (supermarket_id) REFERENCES supermarkets(id)
);

INSERT OR IGNORE INTO product_types (type) VALUES("Snacks");
INSERT OR IGNORE INTO product_types (type) VALUES("Fresh");
INSERT OR IGNORE INTO product_types (type) VALUES("Coffe");
INSERT OR IGNORE INTO product_types (type) VALUES("Fruit");
INSERT OR IGNORE INTO product_types (type) VALUES("Meat & Fish");
INSERT OR IGNORE INTO product_types (type) VALUES("Bread");
