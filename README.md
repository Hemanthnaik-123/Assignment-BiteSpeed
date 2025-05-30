# Bitespeed Backend Task – Identity Reconciliation

This is my submission for the backend assignment given by Bitespeed. The goal is to create an API that helps identify a customer even if they used different emails or phone numbers in different orders.

## Problem

Customers might use different emails/phone numbers for different orders. We need to link these records and return a single identity with all the connected details.

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite (can be replaced with other DBs)

## How It Works

I created a `/identify` POST endpoint. You send a request with either email, phone number, or both, and it returns the primary contact with all linked secondary contacts.

### Example request:

```json
{
  "email": "mcfly@hillvalley.edu",
  "phoneNumber": "123456"
}
```

### Example response:

```json
{
  "contact": {
    "primaryContatctId": 1,
    "emails": ["lorraine@hillvalley.edu", "mcfly@hillvalley.edu"],
    "phoneNumbers": ["123456"],
    "secondaryContactIds": [23]
  }
}
```

## How to Run

1. Install requirements:

```bash
pip install -r requirements
```

2. Run the server:

```bash
uvicorn main:app --reload
```

3. Test the API at `http://localhost:8000/docs`

## Files

- `main.py` – API logic
- `models.py` – Contact model
- `crud.py` – DB operations
- `database.py` – DB setup
- `schemas.py` – Request/response models
- `requirements` – Dependencies list

## Notes

- New contact is created if not found.
- If existing data matches partially, a secondary contact is added.
- All records are linked through the `linkedId` field.

---


