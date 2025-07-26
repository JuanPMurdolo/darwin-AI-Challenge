# Darwin AI Challenge - Makefile

.PHONY: help build up down logs test clean dev prod health

# Default target
help:
	@echo "Darwin AI Challenge - Available commands:"
	@echo "  build     - Build all Docker images"
	@echo "  up        - Start all services"
	@echo "  down      - Stop all services"
	@echo "  logs      - Show logs for all services"
	@echo "  test      - Run tests"
	@echo "  clean     - Clean up containers and volumes"
	@echo "  dev       - Start in development mode"
	@echo "  prod      - Start in production mode"
	@echo "  health    - Check service health"

# Build all images
build:
	docker compose build

# Start all services
up:
	docker compose up -d

# Stop all services
down:
	docker compose down

# Show logs
logs:
	docker compose logs -f

# Run tests
test:
	chmod +x bot-service/test_docker.sh
	./bot-service/test_docker.sh

# Clean up
clean:
	docker compose down -v
	docker system prune -f

# Development mode
dev:
	docker compose -f docker-compose.yaml -f docker-compose.dev.yaml up

# Production mode
prod:
	docker compose up -d

# Check health of all services
health:
	@echo "🏥 Checking service health..."
	@echo ""
	@echo "Bot Service:"
	@curl -s http://localhost:8001/health/live | jq . || echo "❌ Bot service not responding"
	@echo ""
	@echo "Celery Flower:"
	@curl -s http://localhost:5556 > /dev/null && echo "✅ Flower UI available" || echo "❌ Flower not available"
	@echo ""
	@echo "Database:"
	@docker exec expenses-db pg_isready -U expenses_user -d expenses_db && echo "✅ Database ready" || echo "❌ Database not ready"
	@echo ""
	@echo "Redis:"
	@docker exec expenses-redis redis-cli ping && echo "✅ Redis ready" || echo "❌ Redis not ready"

# Monitor Celery
monitor:
	@echo "📊 Celery Flower available at: http://localhost:5556"
	@open http://localhost:5556 || echo "Open http://localhost:5556 in your browser"

# Database operations
db-shell:
	docker exec -it expenses-db psql -U expenses_user -d expenses_db

# View logs for specific service
logs-bot:
	docker compose logs -f bot-service

logs-celery:
	docker compose logs -f celery-worker

logs-db:
	docker compose logs -f postgres
