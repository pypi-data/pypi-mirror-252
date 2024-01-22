clean_docker:
	@echo "Cleaning images..."
	@docker rm -f $$(docker ps -a -q) || true
	@docker rmi -f $$(docker images -q) || true
	@docker volume prune
	@docker network prune

up:
	@echo "Starting containers..."
	@docker-compose up app

up_debug:
	@echo "Starting containers..."
	@docker-compose up app_debug

ip_db:
	@echo "IP of DB container:"
	@docker inspect escoladobem_db_1 | grep IPAddress

db_restore:
	@echo "Restoring DB..."
	@pg_restore -U minhareceita -d minhareceita -h localhost -Fc minhareceita.backup

db_drop:
	@echo "Dropping DB..."
	@psql -U minhareceita -h localhost -c "DROP DATABASE minhareceita;"


env:
	@echo "Creating .env file..."
	@export $(cat .env | xargs) && envsubst < .env.template > .env

bash:
	@echo "Entering container..."
	@docker exec -ti property_fallen-app-1 bash