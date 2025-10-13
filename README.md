# 🏭 Factory Scheduler
This is a simple app to schedule work orders and part production.


## 🚀 Getting Started
Copy the files to your local machine and build the docker images with the following commands:
```bash
git clone git@github.com:maddencs/factory_scheduling.git
docker-compose build
```

Run database migrations with:
```bash
docker-compose run run_migrations
````

To run the tests inside the docker testing container:

```bash
docker-compose run tests
```

To run the app:
```bash
docker-compose up web db
```
Then access the GraphQL playground at http://localhost:8000/graphql/

Optionally, seed the database with some test data:
```bash
docker-compose run seed_demo_data
```

## 🤖 GraphQL Schema
 [View the full GraphQL Schema](./schema.graphql)

## Stretch Goals(other than auth)

- [ ] Rescheduling when a part is delayed to restore synchronization
- [ ] Pipelined or batch processing per workcenter
- [X] Multi‑order planning and interference avoidance
- [ ] Slack/tolerance parameters for the scheduler (for example ±5%)
- [ ] Visualization or simple Gantt output
- [ ] Async execution with job status and polling/subscriptions
- [ ] Heuristics or optimizations to minimize idle time and balance load

## ⚠️ Possible edge cases and limitations
- Orders with no parts
- No error handling or retries in scheduling
- Potential for double booking a workcenter

## 💡 Design Decisions
- Business logic is decoupled from the API logic
- Tests are small and focused
- Docker allows for consistent development and deployment

## ⚙️ Tech Stack
- FastAPI
- SQLAlchemy
- GraphQL
- PostgreSQL
- pytest
- alembic
- Docker