from __future__ import annotations

SCHEMA_CONTEXT = r'''
PostgreSQL classicmodels schema:

productlines("productLine", "textDescription", "htmlDescription", "image")
products("productCode", "productName", "productLine", "productScale", "productVendor", "productDescription", "quantityInStock", "buyPrice", "MSRP")
offices("officeCode", "city", "phone", "addressLine1", "addressLine2", "state", "country", "postalCode", "territory")
employees("employeeNumber", "lastName", "firstName", "extension", "email", "officeCode", "reportsTo", "jobTitle")
customers("customerNumber", "customerName", "contactLastName", "contactFirstName", "phone", "addressLine1", "addressLine2", "city", "state", "postalCode", "country", "salesRepEmployeeNumber", "creditLimit")
payments("customerNumber", "checkNumber", "paymentDate", "amount")
orders("orderNumber", "orderDate", "requiredDate", "shippedDate", "status", "comments", "customerNumber")
orderdetails("orderNumber", "productCode", "quantityOrdered", "priceEach", "orderLineNumber")

Relationships:
products."productLine" -> productlines."productLine"
employees."officeCode" -> offices."officeCode"
employees."reportsTo" -> employees."employeeNumber"
customers."salesRepEmployeeNumber" -> employees."employeeNumber"
payments."customerNumber" -> customers."customerNumber"
orders."customerNumber" -> customers."customerNumber"
orderdetails."orderNumber" -> orders."orderNumber"
orderdetails."productCode" -> products."productCode"
'''

DECOMPOSITION_PROMPT = '''
You are decomposing a natural language database question into structured JSON.
Return ONLY valid JSON with these keys:
Intent, Tables, Columns, Filters, Joins.

Question:
{question}

Database schema:
{schema}
'''

SQL_GENERATION_PROMPT = '''
You are writing PostgreSQL for the classicmodels database.
Use only a safe SELECT query.
Use quoted identifiers for camelCase columns such as "customerName" and "orderNumber".
Return ONLY the SQL query, no markdown.

Structured decomposition:
{decomposition}

Database schema:
{schema}
'''

SQL_FIX_PROMPT = '''
The following PostgreSQL SELECT query failed.
Fix the SQL using the database error message.
Return ONLY the corrected SELECT SQL query, no markdown.
Do not use DELETE, DROP, UPDATE, INSERT, ALTER, or TRUNCATE.

Original question:
{question}

Failed SQL:
{sql}

Database error:
{error}

Database schema:
{schema}
'''
