# Factory Scheduler
This is a simple app to schedule work orders and part production.


## 🚀 Getting Started
Copy the files to your local machine and build the docker images with the following commands:
```bash
git clone git@github.com:maddencs/factory_scheduling.git
docker-compose build --no-cache
```

Run database migrations with:
```bash
docker-compose run run_migrations
````

To run the tests inside the docker testing container:

```bash
docker-compose run --rm tests
```

To run the app:
```bash
docker-compose up web db
```

Access the GraphQL playground at http://localhost:8000/graphql/


## ⚙️ Tech Stack
- FastAPI
- SQLAlchemy
- GraphQL
- PostgreSQL
- pytest
- alembic
- Docker