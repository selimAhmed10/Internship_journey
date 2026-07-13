# JWT Permission 

## Project Overview

This is a JwtPermission application built with Django REST Framework.It provides a complete financial transaction system with role based access control(mostly focused on the permission build in and customd),JWT authentication, and secure transaction management.

---

## User Roles

The system has 3  roles with different permissions(django build in and custom) and responsibilities:

### 1.  Admin
- Full System Control

The Admin has complete control over the entire system with access to all features and data for manage everything.

### 2. Agent  
- Customer Transaction Handler

Agents act as intermediaries who handle financial transactions for customers.

### 3. Customer
- Personal Account Management

Customers can manage their own accounts and perform transactions.


## Features & Permission Matrix


##  Admin Features

| # | Feature | Description | Path | Method |
|---|---------|-------------|------|--------|
| 1 | Admin Dashboard | View system overview with total customers, agents, transactions | /api/admin/dashboard/ | GET |
| 2 | View All Transactions | Admin can see every transaction in the system | /api/admin/transactions/ | GET |
| 3 | List All Users | Admin can view all registered users | /api/auth/admin/users/ | GET |
| 4 | Create User | Admin can create new users (Customer/Agent) | /api/auth/admin/users/ | POST |
| 5 | View User Details | Admin can view specific user details | /api/auth/admin/users/{id}/ | GET |
| 6 | Update User | Admin can update any user's details | /api/auth/admin/users/{id}/ | PUT |
| 7 | Delete User | Admin can delete any user | /api/auth/admin/users/{id}/ | DELETE |
| 8 | Transaction Detail | Admin can view any transaction details | /api/transactions/{id}/ | GET |



##  Agent Features

| # | Feature | Description | Path | Method |
|---|---------|-------------|------|--------|
| 1 | Agent Dashboard | View personal information (name, role, phone, balance) | /api/agent/dashboard/ | GET |
| 2 | View Own Transactions | Agent can see only their handled transactions | /api/agent/transactions/ | GET |
| 3 | Cash In | Agent can add money to customer's wallet | /api/agent/cash-in/ | POST |
| 4 | Transaction Detail | Agent can view details of handled transactions | /api/transactions/{id}/ | GET |



##  Customer Features

| # | Feature | Description | Path | Method |
|---|---------|-------------|------|--------|
| 1 | Customer Dashboard | View personal information (name, role, phone, balance) | /api/customer/dashboard/ | GET |
| 2 | View Own Transactions | Customer can see only their own transactions | /api/customer/transactions/ | GET |
| 3 | Send Money | Customer can send money to other customers | /api/customer/send-money/ | POST |
| 4 | Cash Out | Customer can withdraw money through agent | /api/customer/cash-out/ | POST |
| 5 | Transaction Detail | Customer can view details of own transactions | /api/transactions/{id}/ | GET |



##  Authentication Features

| # | Feature | Description | Path | Method |
|---|---------|-------------|------|--------|
| 1 | User Registration | Register new user (Customer/Agent/Admin) | /api/auth/register/ | POST |
| 2 | User Login | Login with username & password to get tokens | /api/auth/login/ | POST |
| 3 | Refresh Token | Get new access token using refresh token | /api/auth/refresh/ | POST |
| 4 | User Logout | Logout and blacklist refresh token | /api/auth/logout/ | POST |



##  Permission Matrix

| Endpoint | Method | Admin | Agent | Customer | Non User |
|----------|--------|-------|-------|----------|----------|
| **Authentication** |
| /api/auth/register/ | POST | ✅ | ✅ | ✅ | ✅ |
| /api/auth/login/ | POST | ✅ | ✅ | ✅ | ✅ |
| /api/auth/refresh/ | POST | ✅ | ✅ | ✅ | ❌ |
| /api/auth/logout/ | POST | ✅ | ✅ | ✅ | ❌ |
| **Admin** |
| /api/admin/dashboard/ | GET | ✅ | ❌ | ❌ | ❌ |
| /api/admin/transactions/ | GET | ✅ | ❌ | ❌ | ❌ |
| /api/auth/admin/users/ | GET | ✅ | ❌ | ❌ | ❌ |
| /api/auth/admin/users/ | POST | ✅ | ❌ | ❌ | ❌ |
| /api/auth/admin/users/{id}/ | GET | ✅ | ❌ | ❌ | ❌ |
| /api/auth/admin/users/{id}/ | PUT | ✅ | ❌ | ❌ | ❌ |
| /api/auth/admin/users/{id}/ | DELETE | ✅ | ❌ | ❌ | ❌ |
| **Agent** |
| /api/agent/dashboard/ | GET | ❌ | ✅ | ❌ | ❌ |
| /api/agent/transactions/ | GET | ❌ | ✅ | ❌ | ❌ |
| /api/agent/cash-in/ | POST | ❌ | ✅ | ❌ | ❌ |
| **Customer** |
| /api/customer/dashboard/ | GET | ❌ | ❌ | ✅ | ❌ |
| /api/customer/transactions/ | GET | ❌ | ❌ | ✅ | ❌ |
| /api/customer/send-money/ | POST | ❌ | ❌ | ✅ | ❌ |
| /api/customer/cash-out/ | POST | ❌ | ❌ | ✅ | ❌ |
| **Transaction** |
| /api/transactions/{id}/ | GET | ✅ | ✅ | ✅ | ❌ |



## Permission List


| # | Permission | Type | Description |
|---|------------|------|-------------|
| 1 | AllowAny | Built-in | Allows access to anyone, even unauthenticated users |
| 2 | IsAuthenticated | Built-in | Allows access only to authenticated users |
| 3 | IsAuthenticatedOrReadOnly | Built-in | Allows read-only for unauthenticated, full access for authenticated |
| 4 | IsAdmin | Custom | Allows access only to Admin users |
| 5 | IsAgent | Custom | Allows access only to Agent users |
| 6 | IsCustomer | Custom | Allows access only to Customer users |
| 8 | IsActiveAccount | Custom | Allows access only to active accounts |
| 9 | IsTransactionOwner | Custom | Allows access only to own transactions |

