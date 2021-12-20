# -----------------------------------------------------------------------------
# development -----------------------------------------------------------------
# -----------------------------------------------------------------------------
create-network:
	docker network create django-microservices

start-development:
	cd docker/development/ && docker-compose up -d

stop-development:
	cd docker/development/ && docker-compose stop

build-development:
	# Backend for frontend ms -------------------------------------------------
	cp services/backend_for_frontend_ms/requirements.txt docker/development/build/backend_for_frontend_ms/requirements.txt
	cd docker/development/build/backend_for_frontend_ms/ && docker build -t "diegoug/backend_for_frontend_ms_dev" .
	rm -rf docker/development/build/backend_for_frontend_ms/requirements.txt
	# orchestrator ms ---------------------------------------------------------
	cp services/orchestrator_ms/requirements.txt docker/development/build/orchestrator_ms/requirements.txt
	cd docker/development/build/orchestrator_ms/ && docker build -t "diegoug/orchestrator_ms_dev" .
	rm -rf docker/development/build/orchestrator_ms/requirements.txt
	# author ms ----------------------------------------------------------
	cp services/author_ms/requirements.txt docker/development/build/author_ms/requirements.txt
	cd docker/development/build/author_ms/ && docker build -t "diegoug/author_ms_dev" .
	rm -rf docker/development/build/author_ms/requirements.txt
	# book ms ----------------------------------------------------------
	cp services/book_ms/requirements.txt docker/development/build/book_ms/requirements.txt
	cd docker/development/build/book_ms/ && docker build -t "diegoug/book_ms_dev" .
	rm -rf docker/development/build/book_ms/requirements.txt
	# user ms -----------------------------------------------------------------
	cp services/user_ms/requirements.txt docker/development/build/user_ms/requirements.txt
	cd docker/development/build/user_ms/ && docker build -t "diegoug/user_ms_dev" .
	rm -rf docker/development/build/user_ms/requirements.txt
