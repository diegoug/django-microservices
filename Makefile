# -----------------------------------------------------------------------------
# development -----------------------------------------------------------------
# -----------------------------------------------------------------------------
create-network:
	docker network create django-microservices

start-development:
# detect dinamic os path's
	$(eval $LOCAL_VAR := /var)
	$(eval $LOCAL_SSH := ~)
ifeq ($(UNAME_S),Linux)
	$(eval $LOCAL_SSH := ~)
else ifeq ($(UNAME_S),Darwin)
	$(eval $LOCAL_VAR := ~/Documents/var)
else ifeq ($(OS),Windows_NT)
	$(eval $LOCAL_SSH := C:)
endif
	cd docker/development/ && echo "LOCAL_VAR=$($LOCAL_VAR)" >> .env
	cd docker/development/ && echo "LOCAL_SSH=$($LOCAL_SSH)" >> .env
	# set dynamic env vars
	cd docker/development/ && echo "ENV=localhost" >> .env
	# CMD: start full local platform
	cd docker/development/ && docker-compose up -d
	# remove dynamic env vars
	cd docker/development/ && sed -i.bu '/ENV=localhost/d' .env

stop-development:
	$(eval $LOCAL_VAR := /var)
	$(eval $LOCAL_SSH := ~)
	# set dynamic env vars
	cd docker/development/ && echo "LOCAL_VAR=$($LOCAL_VAR)" >> .env
	cd docker/development/ && echo "LOCAL_SSH=$($LOCAL_SSH)" >> .env
	# CMD: stop local platform
	cd docker/development/ && docker-compose stop
	# remove dynamic env vars
	cd docker/development/ && sed -i.bu $'/LOCAL_VAR='$(LOCAL_VAR)$'/d' .env
	cd docker/development/ && sed -i.bu $'/LOCAL_SSH='$(LOCAL_SSH)$'/d' .env

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
