# 🏭 Factory Scheduler
This is a simple app to schedule work orders and part production.


## 🚀 Getting Started
Initial setup
```bash
git clone git@github.com:maddencs/factory_scheduling.git # Clone the repo
cd factory_scheduling # Navigate to the project directory
docker-compose build # Build the docker images
docker-compose run run_migrations # Run database migrations

# (Optional) Seed database with demo data
docker-compose run seed_demo_data
````

Run the tests inside the docker testing container:

```bash
docker-compose run tests
```

To run the app:
```bash
docker-compose up web db
```
Access the GraphQL playground at http://localhost:8000/graphql/

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