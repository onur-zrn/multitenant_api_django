"""
# Multi-Tenant Django REST API

A Django REST Framework application with PostgreSQL schema-based multi-tenancy.

## Features

- **Schema-based Multi-tenancy**: Each center gets its own PostgreSQL schema
- **User Management**: Global user system with center associations
- **Sample Management**: Tenant-specific sample and result management
- **REST API**: Full CRUD operations with filtering and pagination
- **Docker Support**: Complete containerization with Docker Compose

## Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd multitenant_api
```
Important Note: If you want to run the program locally, the host setting in .env and multitenant_project/settings.py should be changed to localhost, and the database settings should be configured.
### 2. Environment Setup

Create `.env` file:
```
DEBUG=True
SECRET_KEY=your-very-secret-key-here
DATABASE_NAME=multitenant_db
DATABASE_USER=postgres
DATABASE_PASSWORD=root
DATABASE_HOST=db
DATABASE_PORT=5432
```

### 3. Docker Setup

```bash
# Start services
docker-compose up -d

# Wait for database to be ready, then run migrations
docker-compose exec web python manage.py migrate_schemas --shared
docker-compose exec web python manage.py migrate_schemas

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

### 4. Create Your First Tenant

```bash
# Using management command
docker-compose exec web python manage.py setup_tenant --name "Medical Center A" --schema "medical_a"

# Or via API (see API documentation below)
```

## API Documentation

### Public Schema APIs (Available at any domain)

#### 1. User Management

**Create User**
```bash
POST /api/users/
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure_password",
    "password_confirm": "secure_password",
    "first_name": "John",
    "last_name": "Doe",
    "center": 1,
    "is_center_admin": false
}
```

**Login**

```bash  
POST /api/users/login/
{
    "email": "john@example.com",
    "password": "secure_password"
}
```

**Get Profile**
```bash
GET /api/users/profile/
CSRF token ve session id gerekli.
```

**List Center Users**
```bash
GET /api/users/center_users/
```

#### 2. Center Management

**Create Center**
```bash
POST /api/centers/
{
    "schema_name": "Medical Center",
    "name": "Medical Center B",
    "description": "A medical center for testing"
}
```

**List Centers**
```bash
GET /api/centers/
```

**Get Center Details**
```bash
GET /api/centers/{id}/
```

**Update Center**
```bash
PUT /api/centers/{id}/
{
    "name": "Updated Medical Center",
    "description": "Updated description"
    "schema_name": "Updated Medical Center"
}
```

**Migrate Schema**
```bash
POST /api/centers/{id}/migrate_schema/
```

### Tenant Schema APIs (Available at tenant domains like medical_a.localhost:8000)

#### 3. Sample Management

**Create Sample**
```bash
POST http://samples.localhost:8000/api/samples/
{
    "name": "Blood Sample #001",
    "description": "Patient blood sample",
    "sample_type": "blood",
    "collection_date": "2025-08-10T10:00:00Z",
    "status": "collected",
    "metadata": {
        "patient_id": "P001",
        "collector": "Dr. Smith"
    }
}
Authorization is required username and password
```

**List Samples with Filters**
```bash
GET http://samples.localhost:8000/api/samples/
GET http://samples.localhost:8000/api/samples/?status=completed
GET http://samples.localhost:8000/api/samples/?sample_type=blood
GET http://samples.localhost:8000/api/samples/?start_date=2025-08-01&end_date=2025-08-10
```

**Update Sample Status**
```bash
PATCH /api/samples/{id}/update_status/
{
    "status": "processing"
}
```

**Add Sample Result**
```bash
POST http://samples.localhost:8000/api/samples/{id}/add_result/
{
    "test_name": "Hemoglobin",
    "result_value": "14.2",
    "unit": "g/dL",
    "reference_range": "12.0-15.5",
    "is_abnormal": false,
    "notes": "Normal range"
    "sample": 1
}
```

**Get Sample Statistics**
```bash
GET /api/samples/statistics/
```

#### 4. Sample Results

**List Results**
```bash
GET  http://samples.localhost:8000/api/sample-results/
GET  http://samples.localhost:8000/api/sample-results/?sample=1
GET  http://samples.localhost:8000/api/sample-results/?is_abnormal=true
```

## Domain Configuration

The system uses domain-based tenant routing. Configure your hosts file or DNS:

```
# /etc/hosts (Linux/Mac) or C:\Windows\System32\drivers\etc\hosts (Windows)
127.0.0.1 medical_a.localhost
127.0.0.1 medical_b.localhost
127.0.0.1 localhost
```

## Database Schema Structure

- **Public Schema**: Contains shared data (Centers, Domains, Users)
- **Tenant Schemas**: Each center gets its own schema with isolated data (Samples, SampleResults)

## Key Features

### 1. Automatic Schema Creation
When you create a new Center via API, the system automatically:
- Creates a PostgreSQL schema
- Runs migrations for the tenant
- Creates a domain mapping

### 2. User-Center Association
- Users exist in the public schema
- Users can be associated with centers
- Center admins have additional permissions

### 3. Data Isolation
- Each center's data is completely isolated
- Samples and results are tenant-specific
- Cross-tenant data access is prevented

### 4. RESTful APIs
- Full CRUD operations
- Filtering and pagination
- Proper HTTP status codes
- JSON responses

## Development

### Run Tests
```bash
docker-compose exec web python manage.py test
```

### Access Tenant Schema Directly
```bash
docker-compose exec web python manage.py shell
from django_tenants.utils import schema_context
from tenants.models import Center

center = Center.objects.get(schema_name='medical_a')
with schema_context(center.schema_name):
    from core.models import Sample
    samples = Sample.objects.all()
    print(f"Found {samples.count()} samples")
```

### Create Additional Management Commands
```bash
# Create new tenant
docker-compose exec web python manage.py setup_tenant --name "Lab Center" --schema "lab_center"

# List all tenants
docker-compose exec web python manage.py list_tenants
```

## Production Considerations

1. **Security**: Update SECRET_KEY, use environment variables
2. **Database**: Use managed PostgreSQL service
3. **Domains**: Configure proper DNS and SSL certificates
4. **Monitoring**: Add logging and monitoring solutions
5. **Backup**: Implement schema-aware backup strategy

## Troubleshooting

### Common Issues

1. **Schema not found**: Run `migrate_schemas` command
2. **Permission denied**: Check user permissions and center associations
3. **Domain routing**: Verify domain configuration in hosts file

### Useful Commands

```bash
# Check current schema
docker-compose exec web python manage.py shell -c "from django.db import connection; print(connection.schema_name)"

# List all schemas
docker-compose exec db psql -U postgres -d multitenant_db -c "SELECT schema_name FROM information_schema.schemata;"

# Reset database (development only)
docker-compose down -v
docker-compose up -d
```
"""   