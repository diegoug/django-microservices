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
	# Backend for frontend MS -------------------------------------------------
	cp services/backend_for_frontend_MS/requirements.txt docker/development/build/backend_for_frontend_MS/requirements.txt
	cd docker/development/build/backend_for_frontend_MS/ && docker build -t "diegoug/backend-for-frontend-ms-dev" .
	rm -rf docker/development/build/backend_for_frontend_MS/requirements.txt
	# Backend for frontend OC -------------------------------------------------
	cp services/backend_for_frontend_OC/package.json docker/development/build/backend_for_frontend_OC/package.json
	cd docker/development/build/backend_for_frontend_OC/ && docker build -t "diegoug/backend-for-frontend-oc-dev" .
	rm -rf docker/development/build/backend_for_frontend_OC/package.json
	# User MS -----------------------------------------------------------------
	cp services/user_MS/requirements.txt docker/development/build/user_MS/requirements.txt
	cd docker/development/build/user_MS/ && docker build -t "diegoug/user-ms-dev" .
	rm -rf docker/development/build/user_MS/requirements.txt
	# service A - MS ----------------------------------------------------------
	cp services/service_a_MS/requirements.txt docker/development/build/service_a_MS/requirements.txt
	cd docker/development/build/service_a_MS/ && docker build -t "diegoug/service-a-ms-dev" .
	rm -rf docker/development/build/service_a_MS/requirements.txt
	# service B - MS ----------------------------------------------------------
	cp services/service_b_MS/requirements.txt docker/development/build/service_b_MS/requirements.txt
	cd docker/development/build/service_b_MS/ && docker build -t "diegoug/service-b-ms-dev" .
	rm -rf docker/development/build/service_b_MS/requirements.txt

