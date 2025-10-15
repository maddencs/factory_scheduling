# 🏭 Factory Scheduler
This is a simple app to schedule work orders and part production.


## 🚀 Getting Started
### Terraform Instructions
1. Install Terraform
2. Run the following commands
```bash
    terraform init  # Initialize terraform
    terraform plan  # Optional to review terraform plant
    terraform apply  # apply the plan and spin up the services. Accept with "yes" when prompted
```
Access the app at http://localhost:8000/graphql

### Docker Instructions
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
- FastAPI - Lightweight API framework for REST and async API's
- SQLAlchemy - Database ORM
- GraphQL - API query language(using `strawberry`)
- PostgreSQL - Relational database for persistence layer
- pytest - Python testing framework
- alembic - For database migrations
- Docker - Containerization for consistent deployment/development environments
- Terraform - Infrastructure as Code(IaC) for provisioning infrastructure