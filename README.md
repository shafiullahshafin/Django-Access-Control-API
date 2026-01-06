# Access Control Log API

A Django REST API for logging door access events in an access control system.

## Features

- RESTful API for managing access logs
- Automatic timestamp recording
- Django signals for system event logging
- SQLite database
- Comprehensive unit tests
- Added filtering to the endpoint
- Containerized the application using Docker

## Requirements

- Python 3.8+
- Django 4.2+
- Django REST Framework 3.14+

## Installation and Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd access-control-api
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations

```bash
python manage.py migrate
```

### 5. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## API Endpoints

### 1. Create Access Log

**POST** `/api/logs/`

**Request Body:**

```json
{
    "card_id": "C1001",
    "door_name": "Main Entrance",
    "access_granted": true
}
```

**Response:** `201 Created`

```json
{
    "id": 1,
    "card_id": "C1001",
    "door_name": "Main Entrance",
    "access_granted": true,
    "timestamp": "2025-01-06T10:35:15.123456Z"
}
```

### 2. List All Access Logs

**GET** `/api/logs/`

**Response:** `200 OK`

```json
[
    {
        "id": 1,
        "card_id": "C1001",
        "door_name": "Main Entrance",
        "access_granted": true,
        "timestamp": "2025-01-06T10:35:15.123456Z"
    }
]
```

### 3. Get Single Access Log

**GET** `/api/logs/<id>/`

**Response:** `200 OK`

```json
{
    "id": 1,
    "card_id": "C1001",
    "door_name": "Main Entrance",
    "access_granted": true,
    "timestamp": "2025-01-06T10:35:15.123456Z"
}
```

### 4. Update Access Log

**PUT** `/api/logs/<id>/`

**Request Body:**

```json
{
    "card_id": "C1001",
    "door_name": "Back Entrance",
    "access_granted": false
}
```

**Response:** `200 OK`

**Note:** The `timestamp` field is read-only and cannot be updated.

### 5. Delete Access Log

**DELETE** `/api/logs/<id>/`

**Response:** `204 No Content`

## System Event Logging

The application automatically logs creation and deletion events to `system_events.log`:

**On Create:**

```pgsql
[2025-01-06 10:35:15] - CREATE: Access log created for card C1001. Status: GRANTED.
```

**On Delete:**

```pgsql
[2025-01-06 10:38:00] - DELETE: Access log (ID: 15) for card C1001 was deleted.
```

## Running Tests

Run all unit tests:

```bash
python manage.py test
```

Run tests with verbose output:

```bash
python manage.py test --verbosity=2
```

Run specific test class:

```bash
python manage.py test access_control.tests.AccessLogAPITest
```

## Project Structure

```text
access-control-api/
├── access_control/          # Django app
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py           # AccessLog model
│   ├── serializers.py      # DRF serializer
│   ├── signals.py          # Django signals for logging
│   ├── tests.py            # Unit tests
│   ├── urls.py             # App URL configuration
│   └── views.py            # API views
├── access_control_project/ # Django project
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── venv/                   # Virtual environment
├── .gitignore
├── db.sqlite3             # SQLite database
├── manage.py
├── README.md
├── requirements.txt
└── system_events.log      # System event log file
```

## Data Model

### AccessLog Model

```text
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key (auto-generated) |
| card_id | CharField | Unique card identifier (e.g., "C1001") |
| door_name | CharField | Name of the door (e.g., "Main Entrance") |
| access_granted | BooleanField | Whether access was granted (True/False) |
| timestamp | DateTimeField | Automatic timestamp (auto_now_add=True) |
```

### License

```text
This project is for technical assessment purposes.
```
