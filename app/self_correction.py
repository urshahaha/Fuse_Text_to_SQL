from __future__ import annotations

import re

# Common column names in the seeded schema. Used for simple quote correction.
KNOWN_COLUMNS = [
    "productLine", "textDescription", "htmlDescription", "image", "productCode",
    "productName", "productScale", "productVendor", "productDescription",
    "quantityInStock", "buyPrice", "MSRP", "officeCode", "city", "phone",
    "addressLine1", "addressLine2", "state", "country", "postalCode", "territory",
    "employeeNumber", "lastName", "firstName", "extension", "email", "reportsTo",
    "jobTitle", "customerNumber", "customerName", "contactLastName",
    "contactFirstName", "salesRepEmployeeNumber", "creditLimit", "checkNumber",
    "paymentDate", "amount", "orderNumber", "orderDate", "requiredDate",
    "shippedDate", "status", "comments", "quantityOrdered", "priceEach",
    "orderLineNumber",
]


def try_fix_sql(sql: str, error_message: str) -> str:
    """Very small self-correction function for Task 3/4.

    It fixes common beginner mistakes caused by PostgreSQL's case-sensitive quoted
    columns, for example productName -> "productName".
    """
    fixed = sql
    for col in sorted(KNOWN_COLUMNS, key=len, reverse=True):
        # Do not double quote an already quoted column.
        fixed = re.sub(rf'(?<!")\b{re.escape(col)}\b(?!")', f'"{col}"', fixed)
    return fixed
