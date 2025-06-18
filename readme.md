# ExpMantenibilidad2

A Django-based microservices project for demonstrating bulkhead, read, and write database patterns in a medical data context.

I developed this as part of the course "ISIS2503- Arquitectura y diseño de software" (Software architecture and design) at Universidad de los Andes.

A video (in Spanish) showcasing the project can be watched through this link: https://youtu.be/RImE-6kuCwk

## Project Structure

- `bulkhead/`: Bulkhead service for routing and service availability control.
- `database/`: Read and write database microservices.
- `ExpMantenibilidad2/`: Django project configuration.
- `populate_db.py`: Script to populate databases with sample medical data.
- `deployment.yaml`: Example GCP VM and firewall deployment configuration.
- `requirements.txt`: Python dependencies.

## Setup

### Prerequisites

- Python 3.8+
- pip
- (Optional) Google Cloud SDK for deployment

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/danteboe/ExpMantenibilidad2.git
    cd ExpMantenibilidad2
    ```

2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Set environment variables as needed:
    - `SERVER_TYPE`: `bulkhead`, `write`, or `read`
    - `DJANGO_SECRET_KEY`: Your Django secret key
    - `DEBUG`: `True` or `False`
    - `WRITE_DB_IP` and `READ_DB_IP` (for bulkhead server)

4. Run migrations:
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Populate the database:
    ```sh
    python populate_db.py
    ```

6. Start the server:
    ```sh
    python manage.py runserver 0.0.0.0:8000
    ```

## Services

### Bulkhead Service

- **Endpoint:** `/bulkhead/`
- **Routes requests** to the appropriate read/write database service.
- **Service control:**  
    - `/bulkhead/toggle/` (POST): Toggle GET/POST service availability.
    - `/bulkhead/status/` (GET): Check current GET/POST service status.

### Database Service

- **Endpoint:** `/database/`
- **Write:** `/database/write/` (POST)  
    - Only available on write servers.
    - Request body: `{ "title": "...", "content": "..." }`
- **Read:** `/database/read/` (GET)  
    - Only available on read servers.
    - Query params: `id`, `page`, `page_size`
- **Health:** `/database/health/` (GET)

## Deployment

See [deployment.yaml](deployment.yaml) for an example of deploying three VMs (bulkhead, write, read) on Google Cloud Platform.

## Models

- [`database.models.WriteData`](database/models.py): Write-side data model.
- [`database.models.ReadData`](database/models.py): Read-side data model.
- [`bulkhead.models.ServiceStatus`](bulkhead/models.py): Service availability status.

## Populating Data

Run [`populate_db.py`](populate_db.py) to generate sample medical records or initialize service status, depending on `SERVER_TYPE`.

## Testing

Run Django tests with:
```sh
python manage.py test
```

