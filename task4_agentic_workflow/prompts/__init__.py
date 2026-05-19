from __future__ import annotations

SCHEMA_CONTEXT = r'''
Classicmodels PostgreSQL schema:
productlines("productLine", "textDescription", "htmlDescription", "image")
products("productCode", "productName", "productLine", "productScale", "productVendor", "productDescription", "quantityInStock", "buyPrice", "MSRP")
offices("officeCode", "city", "phone", "addressLine1", "addressLine2", "state", "country", "postalCode", "territory")
employees("employeeNumber", "lastName", "firstName", "extension", "email", "officeCode", "reportsTo", "jobTitle")
customers("customerNumber", "customerName", "contactLastName", "contactFirstName", "phone", "addressLine1", "addressLine2", "city", "state", "postalCode", "country", "salesRepEmployeeNumber", "creditLimit")
payments("customerNumber", "checkNumber", "paymentDate", "amount")
orders("orderNumber", "orderDate", "requiredDate", "shippedDate", "status", "comments", "customerNumber")
orderdetails("orderNumber", "productCode", "quantityOrdered", "priceEach", "orderLineNumber")

Common joins:
orders."customerNumber" = customers."customerNumber"
payments."customerNumber" = customers."customerNumber"
orderdetails."orderNumber" = orders."orderNumber"
orderdetails."productCode" = products."productCode"
products."productLine" = productlines."productLine"
employees."officeCode" = offices."officeCode"
customers."salesRepEmployeeNumber" = employees."employeeNumber"
'''

PLANNER_PROMPT = '''
Create a concise plan for answering this database question.
Return JSON with: intent, tables, columns, filters, joins, strategy.

Question: {question}
Schema: {schema}
'''

SQL_GENERATOR_PROMPT = '''
Write a PostgreSQL SELECT query from this plan.
Use quoted identifiers for camelCase columns.
Return only SQL, no markdown.

Plan: {plan}
Schema: {schema}
Previous error if any: {error}
'''

SUMMARY_PROMPT = '''
Summarize the SQL result in a short natural language answer.

Question: {question}
SQL: {sql}
Result: {result}
'''
