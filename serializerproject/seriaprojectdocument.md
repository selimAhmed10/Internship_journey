# Choosing the right serializer Type and test

Django rest framework provides multiple serializer types and each type is designed for a specific level of control,data structure and use case of each.Choosing the correct serializer depends on whether the data is model based, requires custom logic,handles bulk operations or needs nested representation. So sometimes need to use multiple use as per my want.

---

## 1. Basic Serializer

* Basic Serializer is used to handle input and other external API data without a direct database connection
* It has no model dependency, and no automated or predefined fields, so all fields must be defined manually
* Create and update logic must be written manually based on custom requirements
* No predefined rules or built-in model automation like ModelSerializer, so it gives full control over data handling
* Supports custom logic, custom structure, field-level validation, and object-level validation
* Used when more control over data processing is required
* Mainly used when data does not need to be stored in the database
* Common use cases include login, authentication, and external API validation

**Key Characteristics:**
- No model dependency
- Full manual control
- Custom create/update logic required
- Supports field level,object validation
- 

**When to Use:**
- No database storage is required
- Data is only validated or processed or test
- Custom logic is needed like when for  login, authentication,external api validation.
- Complex validation scenarios

**Example:** `BasicUserSerializer`

**Best for:** Full control,non model operations,custom validation logic etc

---

## 2. ModelSerializer

* ModelSerializer is closely connected with Django models and automatically maps model fields so there is no need to define fields manually
* It is directly connected to the Django model and handles read,write, and all crud operations,storing data in the database
* It reduces boilerplate code by generating fields automatically from the model
* It can automatically handle all CRUD operations without needing manual implementation
* It supports the Meta class where we define model, fields, read_only_fields, and extra_kwargs
* It is mainly used for CRUD operations because of its built-in model integration and automation


**Key Characteristics:**
- Model-based
- Auto field generation
- Built in crud operations
- Meta class configuration as per my want
- Supports custom validation as per my want field level and the object level

**When to Use:**
- Working with Django models(ORM)
- Performing crud operations


---

## 3. ListSerializer

* ListSerializer is used for creating a bulk amount of data at a time
* It automatically runs in the background when using serializer with `many=True`
* It helps in validating and processing multiple objects together instead of handling them one by one


**Key Characteristics:**
- Bulk create/update support
- Works with `many=True` in the model

**When to Use:**
- Handling bulk data creation and getting 
- Validating multiple objects together
- Processing lists of records in a single request
- Batch operations



---

## 4. HyperlinkedModelSerializer

* HyperlinkedModelSerializer uses URLs instead of primary keys for object representation
* It generates a unique URL for each object eg.user, account, etc.
* The view name must match the URL pattern defined in `urls.py` to correctly generate links
* `lookup_field="uuid"` is used to specify that UUID should be used in the url instead of the default id
* It is useful for restapi that follow HATEOAS principles, where resources are accessed through links
*Useful for rest apis that follow HATEOAS principles-hypermedia as the engine of apppilication state , in the link store not only the data also store the additonal informatio


**Key Characteristics:**
- URL based representation
- HATEOAS compliant
- Uses view_name and lookup_field
- Auto generates hyperlinks

**When to Use:**
- Building restful apis with navigation links
- Following HATEOAS architecture
- Exposing resources through URLs instead of IDs
- Resource navigation
- Hypermedia apis
---

## 5. Nested Serializer

* Nested Serializer is used when related model data needs to be included inside another serializer
* Instead of returning only foreign keys,it returns complete related object ata time by one api call 
* it create  and update of related objects in a single request using nested way
* It is useful for handling complex relationships like User to  Account to Transaction that is use in my code
* It requires custom create and update logic to properly handle nested writes

**Key Characteristics:**

* Includes related objects
* Complete nested representation
* Custom create and update logic need
* Handles complex relationships
* Single api call for multiple objects create and update 

**When to Use:**

* Working with related models
* Returning detailed relational data
* Creating and updating multiple related objects together at a time 
* Complex data relationships
* need to create or update by one api call 
---

## 6. Read-Only Serializer

* Read-Only Serializer is used when data only needs to be viewed and not modified
* All fields are marked as read-only preventing any update or create operations
* It is ideal for reports,logs and analytics for for write
* It ensures data integrity for sensitive or system  generated information
* It is commonly used for public or restricted view only endpoints

**Key Characteristics:**
* View only serializer
* All fields read only
* No write operations allowed
* Ensures data integrity
* Secure for sensitive data

**When to Use:**

* Generating reports and analytics
* Viewing logs and audit trails
* Public api endpoints (view only)
* Sensitive or system data exposure
---

## 7. Custom Field Serializer

* Custom Field Serializer is used to create specialized fields with custom behavior
* It allows transformation of data between storage format and display format using to representation and internalvalue change
* Examples include MoneyField (USD to BDT conversion) and MaskedAccountField (hides sensitive digits)
* It improves reusability by applying the same logic across multiple serializers
* It helps implement security and formatting rules consistently

**Key Characteristics:**
* Custom field behavior
* Data transformation support
* Reusable field logic
* Security and masking support

**When to Use:**

* Custom data transformation required
* Masking sensitive information
* Reusable field logic across multiple apis 
* Standardized display thats are need in custom logic

---

## 8. SerializerMethodField
* SerializerMethodField is used to add computed fields that do not exist in the model( new field that not have)
* These fields are calculated dynamically at runtime using custom logic
* It can use relationships and model data to derive new values

**Key Characteristics:**
* Computed fields at runtime
* Custom logic based values and structure 
* No database storage required
* Supports aggregation and calculations

**When to Use:**
* Adding computed values and custom as per my wants 
* Calculating totals, counts or summaries etc
* Formatting or derived data
* Dynamic response fields

---


## All Api endpoint-
**Base Url:** http://127.0.0.1:8000/api/


---

## 1. Basic Serializer - User Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/user/` | Create a new user |
| GET | `/api/user/{uuid}/` | Retrieve a specific user by UUID |
| PUT | `/api/user/{uuid}/` | Update a specific user by UUID |

### Validation Error Response

```json
{
    "email": [
        "The email already have"
    ],
    "phone": [
        "Ensure this field has no more than 14 characters."
    ],
    "nid": [
        "Ensure this field has no more than 15 characters."
    ]
}
```
---
## 2.Model Serializer -Account Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/account/` | List all accounts |
| POST | `/api/account/` | Create a new account |
| GET | `/api/account/{uuid}/` | Retrieve a specific account by UUID |
| PUT | `/api/account/{uuid}/` | Update a specific account by UUID |
| PATCH | `/api/account/{uuid}/` | Partially update a specific account |
| DELETE | `/api/account/{uuid}/` | Delete a specific account |


### Get all account

```json
[
    {
        "uuid": "727e51f7-f7a0-4199-913e-ca9ff706992d",
        "account_number": "12345678801234567890",
        "account_type": "Savings",
        "balance": "10000.00",
        "is_active": true,
        "created_at": "2026-06-18T16:08:19.872968Z",
        "user": "1b9a4e31-44ed-4ffe-89d6-05e50270fb30"
    },
    {
        "uuid": "c568f13a-06bb-4058-a0b9-390d68e4a946",
        "account_number": "12345678901234567890",
        "account_type": "Business",
        "balance": "25000.00",
        "is_active": true,
        "created_at": "2026-06-18T16:01:11.779562Z",
        "user": "8a390631-3341-4380-b6c8-ba313a64b064"
    }
]
```
### Validation Error Response

```json
{
    "account_number": [
        "Account number must be 20 character"
    ],
    "account_type": [
        "\"Student\" is not a valid choice."
    ],
    "balance": [
        "the balance cant negative"
    ],
    "user": [
        "This field is required."
    ]
}
```
---




## Computed Fields Endpoint

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `api/computed/account/{uuid}/` | Get computed fields |



### Response

```json
{
    "uuid": "727e51f7-f7a0-4199-913e-ca9ff706992d",
    "available_balance": 10000.0,
    "trasaction_count": 1,
    "last_active": "2026-06-18T16:08:19.879013Z",
    "account_number": "12345678801234567890",
    "account_type": "Savings",
    "balance": "10000.00",
    "is_active": true,
    "created_at": "2026-06-18T16:08:19.872968Z",
    "user": "1b9a4e31-44ed-4ffe-89d6-05e50270fb30"
}
```
---





## Moneyfield and masked field

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `api/custom/account/` | Get custom fields |



### Response

```json
[
    {
        "uuid": "727e51f7-f7a0-4199-913e-ca9ff706992d",
        "balance": "1200000.00 Taka ",
        "account_number": "****************7890",
        "account_type": "Savings",
        "is_active": true,
        "created_at": "2026-06-18T16:08:19.872968Z",
        "user": "1b9a4e31-44ed-4ffe-89d6-05e50270fb30"
    },
    {
        "uuid": "c568f13a-06bb-4058-a0b9-390d68e4a946",
        "balance": "3000000.00 Taka ",
        "account_number": "****************7890",
        "account_type": "Business",
        "is_active": true,
        "created_at": "2026-06-18T16:01:11.779562Z",
        "user": "8a390631-3341-4380-b6c8-ba313a64b064"
    }
]
```
---






## Nasted Trasaction created( with user and accoint)

| Method | Endpoint | Description |
|--------|----------|-------------|
| Post | `nested/write/transaction/` | write nasted trasaction |



### Input 

```json
{
    "amount": 5000,
    "transaction_type": "Deposit",
    "transaction_status": "Successful",
    "note": "Salary Deposit",

    "account": {
        "account_number": "12345678801234567890",
        "account_type": "Savings",
        "balance": 10000,
        "is_active": true,

        "user": {
            "name": "Selim Ahmed akash",
            "email": "selimmmm@gmail.com",
            "phone": "01710945678",
            "nid": "1234567800123"
        }
    }
}
```
### Output

```json
{
    "amount": "5000.00",
    "transaction_type": "Deposit",
    "transaction_status": "Successful",
    "note": "Salary Deposit",
    "account": {
        "account_number": "12345678801234567890",
        "account_type": "Savings",
        "balance": "10000.00",
        "is_active": true,
        "user": {
            "name": "Selim Ahmed akash",
            "email": "selimmmm@gmail.com",
            "phone": "01710945678",
            "nid": "1234567800123"
        }
    }
}
```
---



## Nasted Trasaction patch( with user and accoint)

| Method | Endpoint | Description |
|--------|----------|-------------|
| Put | `nested/write/transaction/{uuid}` | patch nasted trasaction |



### Input 

```json
{
    "amount": "5000.00",
    "note": "Updated account balance",
    "account": {
        "balance": "15000.00"
    }
}
```
### Output

```json
{
    "amount": "5000.00",
    "transaction_type": "Deposit",
    "transaction_status": "Successful",
    "note": "Updated account balance",
    "account": {
        "account_number": "12345678901234567890",
        "account_type": "Savings",
        "balance": "15000.00",
        "is_active": true,
        "user": {
            "name": "Selim Ahmed",
            "email": "selimmm@gmail.com",
            "phone": "01712945678",
            "nid": "1234567890123"
        }
    }
}
```
---
