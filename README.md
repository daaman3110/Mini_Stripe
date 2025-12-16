# Mini Stripe — A Simplified Payment Processing System

A backend-heavy learning project inspired by Stripe, built using Django REST Framework and PostgreSQL.

## What This Project Is

Mini Stripe simulates how a real payment processor works internally:

- Customers create payment intents
- Payments move through multiple states
- Bank processing is simulated
- Events are emitted via webhooks
- Everything logged in PostgreSQL

## Core Concepts Implemented

### Payment Lifecycle (State Machine)

A payment intent flows through real states:
```
created → processing → succeeded / failed
```

This mimics real payment gateways.

### Webhooks (Event-Based Architecture)

When a payment succeeds or fails:

- An event is generated
- Event data is stored in the database
- This mimics how Stripe sends async events

Example events:
- `payment_intent.succeeded`
- `payment_intent.failed`

### PostgreSQL as System of Record

All important data is stored persistently:

- Customers
- Payment intents
- Webhook event logs
- Request logs

## Tech Stack

- **Backend:** Django + Django REST Framework
- **Database:** PostgreSQL
- **Language:** Python
- **Architecture Style:** API-first, event-driven

## API Endpoints

### Customers
```
POST   /customers/
GET    /customers/
GET    /customers/{id}/
```

### Payment Intents
```
POST   /payment_intents/
GET    /payment_intents/{id}/
POST   /payment_intents/{id}/confirm/
```

## Payment Confirmation Flow

When client calls:
```
POST /payment_intents/{id}/confirm/
```

Backend does:

1. Marks payment as `processing`
2. Simulates bank delay (`sleep`)
3. Randomly succeeds or fails
4. Updates DB
5. Emits webhook event
6. Logs event in PostgreSQL

This models real async payment processing.

## Webhooks (Internal Simulation)

Webhook events are generated internally and stored in DB.

This mirrors real-world behavior where:

- Payments are async
- Clients rely on webhooks for final state

##  How to Run Locally

### 1: Install dependencies
```bash
pip install -r requirements.txt
```

### 2: Ensure PostgreSQL is properly configured

### 3: Run migrations
```bash
python manage.py migrate
```

### 4: Start server
```bash
python manage.py runserver
```

---

**Built to learn payment processing fundamentals and event-driven architecture.**