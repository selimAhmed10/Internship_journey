# API View Project
---
## Overview

This api_view project  provides a complete crud operations system with three different DRF implementation styles also the comparision where to use which moreover the django viewset comparision file also.Here have two models(accounts and transactions) with 3 types of crud operation,default router,custom actions.

- **APIView** - Manual CRUD operations with full control
- **GenericAPIView + Mixins** - Balance between manual and automalically.
- **ModelViewSet** - Auto generated CRUD operations with minimal code

---

## Benefits of APIView

- Full control over every request and response (can modify logic exactly as needed or want, no dependency on built DRF shortcuts)
- Can write custom business logic easily as per developer requirement
- Flexible and easier for complex or unique API behavior (work individual urls to do operations)
- Use - Good for learning how DRF works internally and when need custom logic
- Useful when each endpoint needs different behavior to perform but its need to write every line code

---

## Benefits of GenericAPIView and Mixins

- Less code than APIView because CRUD operations come from built-in mixins (get, put, patch, delete etc)
- No need to write repetitive logic for list, create, retrieve, update and delete
- Here have built in queryset and serializer support makes the code cleaner and easier to maintain and also make the operations
- Good for standard CRUD APIs when some or partial customization is needed
- Useful when APIView feels too manual but its do automatics with minimal code
- Its much more easier than the APIView

---

## Benefits of ModelViewSet

- Fastest and the easiest way to build full operations with minimum code
- Automatically provides list, create, retrieve, update and delete operations
- Works with routers (default and the simple routers) to generate URLs automatically
- Easy to maintain because all provide by the DRF
- Used in productions because it easier to maintain
- Least flexible of the three approaches but most productive and clean
- Best choice when custom logic or requirements are minimal and less

---

## URLs + All Endpoints 
**Base url:**  http://localhost:8000/


## ACCOUNTS ENDPOINTS

### 1. APIView

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/accounts/` | List all accounts |
| POST | `/api/accounts/` | Create new account |
| GET | `/api/accounts/{id}/` | Get account by id |
| PUT | `/api/accounts/{id}/` | Update account by id |
| PATCH | `/api/accounts/{id}/` | Partial update account by id |
| DELETE | `/api/accounts/{id}/` | Delete account by id |

### 2. GenericAPIView

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/generic/accounts/` | List all accounts |
| POST | `/api/generic/accounts/` | Create new account |
| GET | `/api/generic/accounts/{id}/` | Get account by id |
| PUT | `/api/generic/accounts/{id}/` | Update account by id |
| PATCH | `/api/generic/accounts/{id}/` | Partial update account by id |
| DELETE | `/api/generic/accounts/{id}/` | Delete account by id |

### 3. ModelViewSet

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/model/accounts/` | List all accounts |
| POST | `/api/model/accounts/` | Create new account |
| GET | `/api/model/accounts/{id}/` | Get account by id |
| PUT | `/api/model/accounts/{id}/` | Update account by id |
| PATCH | `/api/model/accounts/{id}/` | Partial update account by id |
| DELETE | `/api/model/accounts/{id}/` | Delete account by id |
| POST | `/api/model/accounts/{id}/freeze_account/` | Freeze account by id |

---

## TRANSACTIONS ENDPOINTS

### 1. APIView

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/transactions/` | List all transactions |
| POST | `/api/transactions/` | Create new transaction |
| GET | `/api/transactions/{id}/` | Get transaction by id |
| PUT | `/api/transactions/{id}/` | Update transaction by id |
| PATCH | `/api/transactions/{id}/` | Partial update transaction by id |
| DELETE | `/api/transactions/{id}/` | Delete transaction by id |

### 2. GenericAPIView

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/generic/transactions/` | List all transactions |
| POST | `/api/generic/transactions/` | Create new transaction |
| GET | `/api/generic/transactions/{id}/` | Get transaction by id |
| PUT | `/api/generic/transactions/{id}/` | Update transaction by id |
| PATCH | `/api/generic/transactions/{id}/` | Partial update transaction by id |
| DELETE | `/api/generic/transactions/{id}/` | Delete transaction by id |

### 3. ModelViewSet

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/model/transactions/` | List all transactions |
| POST | `/api/model/transactions/` | Create new transaction |
| GET | `/api/model/transactions/{id}/` | Get transaction by id |
| PUT | `/api/model/transactions/{id}/` | Update transaction by id |
| PATCH | `/api/model/transactions/{id}/` | Partial update transaction by id |
| DELETE | `/api/model/transactions/{id}/` | Delete transaction by id |
| GET | `/api/model/transactions/{id}/status/` | Get transaction status by id |
| POST | `/api/model/transactions/{id}/reverse/` | Reverse transaction by id |

---

## Database Models Documentation

## Account Model

| Field Name | Type | Description |
|------------|------|-------------|
| id | uuid | Primary key and auto-generated |
| account_number | String | Unique account number |
| account_owner | String | Name of account owner |
| account_type | String | Options:saving,current,student |
| balance | Decimal | Current account balance (default: 0) |
| is_frozen | Boolean | Account freeze status (default:False) |
| is_active | Boolean | Account active status (default:True) |
| create_at | DateTime | Creation timestamp (auto-generated) |

```python
from django.db import models
import uuid  #make the unique id number that nobody earlier create 

class Account(models.Model):
    account_type=[
        ('saving','Saving'),
        ('current','Current'),
        ('student','Student')
       
    ]
    
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    account_number=models.CharField(max_length=20,unique=True)
    account_owner=models.CharField(max_length=30)
    account_type=models.CharField(choices=account_type,max_length=50)
    balance=models.DecimalField(max_digits=15,decimal_places=2,default=0)
    is_frozen=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    create_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.account_number}"


```
---

## Transaction Model

| Field Name | Type | Description |
|------------|------|-------------|
| trans_id | UUID | Primary key, auto-generated |
| account | UUID (FK) | Reference to Account model |
| amount | Decimal | Transaction amount |
| transaction_type | String | Options:credit,debit |
| status | String | Options:success,failed,pending (default- pending) |
| created_at | DateTime | Transaction timestamp (auto generated) |

---

### Transaction Model code

```python
from django.db import models
from accounts.models import Account
import uuid

class Transaction(models.Model):
    types=[
        ('credit','Credit'),
        ('debit','Debit'),
        ]
    
    transaction_status=[
        ('success','Success'),
        ('failed','Failed'),
        ('pending','Pending'),
        ]
    
    trans_id=models.UUIDField(primary_key =True,default=uuid.uuid4,editable=False)
    account=models.ForeignKey(Account,on_delete=models.CASCADE,related_name='transactions')
    amount=models.DecimalField(max_digits=12,decimal_places=2)
    transaction_type=models.CharField(max_length=10,choices=types)
    status = models.CharField(max_length=10, choices=transaction_status, default='pending')
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.trans_id}"
```
---

## Account Freeze method

## Method Overview

| Property | Value |
|----------|-------|
| Decorator | `@action(detail=True, methods=['post'])` |
| Endpoint | `/api/model/accounts/{id}/freeze_account/` |
| Method | Post |




## Purpose
Frozen accounts cannot perform deposits,withdrawals or transfers and others operations until unfrozen.



## Method Code

```python

    @action(detail=True,methods=['post'])
    def freeze_account(self, request, pk=None):
        account=self.get_object()

        account.is_frozen=True
        account.save()

        return Response({
            "message":"Account frozen successfully",
            "account_number":account.account_number,
            "is_frozen":account.is_frozen
        })
```


**Json output:**

```json
{
    "message": "Account frozen successfully",
    "account_number": "MOD001",
    "is_frozen": true
}
```
---

## Transaction Status Method(Custom action)

### Method Overview

| Property | Value |
|----------|-------|
| Decorator | `@action(detail=True, methods=['get'])` |
| Endpoint | `/api/model/transactions/{id}/status/` |
| Method | GET |


### Purpose

Retrieves the current status of a transaction including details such as transaction id,status, amount,type,creation date and the connected account number.



### Method Code

```python
  @action(detail=True,methods=['get'])
    def status(self,request,pk=None):
       
        transaction=self.get_object()
        return Response({
            'transaction_id':str(transaction.trans_id),
            'status':transaction.status,
            'amount':transaction.amount,
            'type':transaction.transaction_type,
            'created_at':transaction.created_at,
            'account_number': transaction.account.account_number,
        })
```
**Json output:**

```json
{
    "transaction_id": "2743d1e4-84bb-4012-adb9-7c78dbff8f7a",
    "status": "reversed",
    "amount": 20600.0,
    "type": "credit",
    "created_at": "2026-06-06T12:02:06.952406Z",
    "account_number": "SAV1006"
}
```
---

## Transaction Reverse Method (Custom Action)

### Method Overview

| Property | Value |
|----------|-------|
| Decorator | `@action(detail=True, methods=['post'])` |
| Endpoint | `/api/model/transactions/{id}/reverse/` |
| Method | POST |



## Purpose

Reverses a successful transaction by applying the opposite transaction type, updating the original transaction status to "reversed", and creating a new reversal transaction record.



## Method Code

```python
     
    @action(detail=True,methods=['post'])
    def reverse(self,request,pk=None):
        transaction=self.get_object()

    # create reversed transaction
        reversed_transaction=Transaction.objects.create(
            account=transaction.account,
            amount=transaction.amount,
            transaction_type='credit' if transaction.transaction_type== 'debit' else 'debit',
            status='reversed'
            )

        # update the  original transaction
        transaction.status ='reversed'
        transaction.save()

        return Response({
            "message":"reversed successfully",
            "original":str(transaction.trans_id),
            "reversed":str(reversed_transaction.trans_id)
        })
```
**Json output:**

```json
{
    "message": "reversed successfully",
    "original": "2743d1e4-84bb-4012-adb9-7c78dbff8f7a",
    "reversed": "f5fefb1e-03f7-4e34-bca8-3e5b986e56b3"
}
```
---

## Account model CRUD

### Get all the account -
```json

    {
        "id": "f3cc9cc8-e2d1-46c7-aef6-b0073c5c63bc",
        "account_number": "SAV1006",
        "account_owner": "Selim",
        "account_type": "saving",
        "balance": "50000.00",
        "is_frozen": false,
        "is_active": true,
        "create_at": "2026-06-06T09:39:43.541893Z"
    },
    {
        "id": "e212cf2a-06ce-49a5-946e-c635d0e6b00b",
        "account_number": "SAV1007",
        "account_owner": "Jaber",
        "account_type": "saving",
        "balance": "1000000.00",
        "is_frozen": false,
        "is_active": true,
        "create_at": "2026-06-06T09:50:10.187775Z"
    },
    {
        "id": "0b4e5ee4-87e3-497b-9500-df8aad744288",
        "account_number": "SAV1008",
        "account_owner": "tohin",
        "account_type": "saving",
        "balance": "1000003.00",
        "is_frozen": false,
        "is_active": true,
        "create_at": "2026-06-06T09:50:47.383021Z"
    }
```
---

### Create account -

**Input json**
```json
{
  {
    "account_number": "SAV10051",
    "account_owner": "Rahim Khan",
    "account_type": "saving",
    "balance": 50000
}
}
```
**Output json response**
```json
{
    "id": "f7e2ebe3-00a5-4326-b456-f1ff10be59d5",
    "account_number": "SAV10051",
    "account_owner": "Rahim Khan",
    "account_type": "saving",
    "balance": "50000.00",
    "is_frozen": false,
    "is_active": true,
    "create_at": "2026-06-06T18:44:25.112312Z"
}
```
---
### Get one account by id(f7e2ebe3-00a5-4326-b456-f1ff10be59d5) -
```json
  {
    "id": "f7e2ebe3-00a5-4326-b456-f1ff10be59d5",
    "account_number": "SAV10051",
    "account_owner": "Rahim Khan",
    "account_type": "saving",
    "balance": "50000.00",
    "is_frozen": false,
    "is_active": true,
    "create_at": "2026-06-06T18:44:25.112312Z"
}
```
---
### Update account by id(f7e2ebe3-00a5-4326-b456-f1ff10be59d5) -

**Input json**
```json
{
    "account_number": "SAV100tt51",
    "account_owner": "selim ahmed",
    "account_type": "saving",
    "balance": 50000
}
```
**Output json response**
```json
{
    "id": "f7e2ebe3-00a5-4326-b456-f1ff10be59d5",
    "account_number": "SAV100tt51",
    "account_owner": "selim ahmed",
    "account_type": "saving",
    "balance": "50000.00",
    "is_frozen": false,
    "is_active": true,
    "create_at": "2026-06-06T18:44:25.112312Z"
}
```
---


### pathch account by id(f7e2ebe3-00a5-4326-b456-f1ff10be59d5) -

**Input json**
```json
{
    "account_owner": "selim ahmed akash",
    "balance": 50000
}
```
**Output json response**
```json
{
    "id": "f7e2ebe3-00a5-4326-b456-f1ff10be59d5",
    "account_number": "SAV100tt51",
    "account_owner": "selim ahmed akash",
    "account_type": "saving",
    "balance": "50000.00",
    "is_frozen": false,
    "is_active": true,
    "create_at": "2026-06-06T18:44:25.112312Z"
}
```
---
### Delete one account by id(f7e2ebe3-00a5-4326-b456-f1ff10be59d5) -
```json
{
    "message": "successfully deleted"
}
```
---


## Transaction model CRUD

### Get all the transactions -
```json

    
    {
        "trans_id": "99139a4e-325d-4780-8cd0-547bc8728d3c",
        "amount": "10555550.00",
        "transaction_type": "credit",
        "status": "pending",
        "created_at": "2026-06-06T10:26:08.262195Z",
        "account": "3730262b-38dd-40fc-a790-c645107e81c5"
    },
    {
        "trans_id": "478de010-e785-4dc5-ac80-88f35a635d4c",
        "amount": "1555550.00",
        "transaction_type": "credit",
        "status": "reversed",
        "created_at": "2026-06-06T10:26:15.617740Z",
        "account": "3730262b-38dd-40fc-a790-c645107e81c5"
    },
```
---

### Create transaction -

**Input json**
```json
{
    "account": "{b3e1cd5d-93cf-47f4-ad00-4f60134ab663}",
    "amount": 10040,
    "transaction_type": "credit"
}
```
**Output json response**
```json
{
    "trans_id": "c56a1dd0-72ac-430d-85c8-59cddc08baaa",
    "amount": "10040.00",
    "transaction_type": "credit",
    "status": "pending",
    "created_at": "2026-06-06T18:57:02.946280Z",
    "account": "b3e1cd5d-93cf-47f4-ad00-4f60134ab663"
}
```


---
### Update transaction by id(f7e2ebe3-00a5-4326-b456-f1ff10be59d5) -

**Input json**
```json
{
    "account": "{b3e1cd5d-93cf-47f4-ad00-4f60134ab663}",
    "amount": 100400000,
    "transaction_type": "credit"
}
```
**Output json response**
```json
{
    "trans_id": "c56a1dd0-72ac-430d-85c8-59cddc08baaa",
    "amount": "100400000.00",
    "transaction_type": "credit",
    "status": "pending",
    "created_at": "2026-06-06T18:57:02.946280Z",
    "account": "b3e1cd5d-93cf-47f4-ad00-4f60134ab663"
}
```
---

### Get one transaction by id(c56a1dd0-72ac-430d-85c8-59cddc08baaa) -
```json
{
    "trans_id": "c56a1dd0-72ac-430d-85c8-59cddc08baaa",
    "amount": "100400000.00",
    "transaction_type": "credit",
    "status": "pending",
    "created_at": "2026-06-06T18:57:02.946280Z",
    "account": "b3e1cd5d-93cf-47f4-ad00-4f60134ab663"
}
```
---
### pathch account by id(c56a1dd0-72ac-430d-85c8-59cddc08baaa) -

**Input json**
```json
{
    "amount": 8880000
}
```
**Output json response**
```json
{
    "trans_id": "c56a1dd0-72ac-430d-85c8-59cddc08baaa",
    "amount": "8880000.00",
    "transaction_type": "credit",
    "status": "pending",
    "created_at": "2026-06-06T18:57:02.946280Z",
    "account": "b3e1cd5d-93cf-47f4-ad00-4f60134ab663"
}
```
---
### Delete one account by id(c56a1dd0-72ac-430d-85c8-59cddc08baaa) -
```json
{
    "message": "successfully deleted"
}
```
---

