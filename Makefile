# -----------------------------------------------------------------------------
# development -----------------------------------------------------------------
# -----------------------------------------------------------------------------
create-network:
	docker network create django-rest

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
	# django rest framework MS ------------------------------------------------
	cp services/django_rest_framework_MS/requirements.txt docker/development/build/django_rest_framework_MS/
	cd docker/development/build/django_rest_framework_MS/ && docker build -t "diegoug/django-rest-framework-ms-dev" .
	rm -rf docker/development/build/django_rest_framework_MS/requirements.txt
