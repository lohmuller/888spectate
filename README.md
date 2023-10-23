# 888Spectate

**Project Description:** This project implements a robust REST API for managing sports, events, and selections. The API facilitates the creation, searching, and updating of sports, events, and selections with advanced filtering capabilities. Notably, this API employs RAW SQL for operations, adhering to the documentation's specific request for database interactions. The project is built on Django, utilizing `djangorestframework` for API development, incorporating unit testing, and employing Docker for seamless containerization.

## Required Software

- **Docker:** Ensure you have Docker installed to manage the containerized application environment.
- **Docker Compose:** Docker Compose simplifies the process of running multi-container applications. Make sure you have Docker Compose installed alongside Docker.

## Getting Started

1. **Clone the Repository:**
   ```bash
   git clone git@github.com:lohmuller/888spectate.git
   cd 888spectate
   ```

2. **Start Mysql:**
   ```bash
   docker-compose up mysql -d 
   ```

2. **Building and running Migrations:**
   Please wait while until the database is getting ready
   ```bash
   docker-compose run --build web python manage.py migrate
   ```

3. **Starting the web:**
   This will not attach the output console to check for error logs while running
   ```bash
   docker-compose run web
   ```


4. **Access the API:**
   The API documentation, powered by Swagger, is accessible at `http://localhost:80/`. Utilize tools like `curl`, Postman, or similar API clients to interact with the endpoints.

## Testing the Project

To run unit tests, execute the following command inside the project folder:

```bash
docker-compose run test
```

This command triggers unit tests using `pytest`.

## API Endpoints

The API provides a range of endpoints for managing sports, events, and selections, including creation, retrieval, and updating functionalities. The endpoints include:

- **`GET /sports/`**: Retrieve a list of sports.
- **`GET /events/`**: Retrieve a list of events.
- **`GET /selection/`**: Retrieve a list of selections.
- **`POST /sports/`**: Create a new sport.
- **`POST /events/`**: Create a new event.
- **`POST /selection/`**: Create a new selection.
- **`PUT /sports/<id>/`**: Update details of a specific sport.
- **`PUT /events/<id>/`**: Update details of a specific event.
- **`PUT /selection/<id>/`**: Update details of a specific selection.

## Notes

- The project utilizes RAW SQL for operations due to specific documentation requirements, ensuring optimized database interactions.
- Comprehensive unit tests are integrated to ensure the correctness of API endpoints.
- Docker containerization simplifies deployment and management processes.
