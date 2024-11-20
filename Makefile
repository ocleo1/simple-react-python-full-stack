TARGET :=
DETACH :=
NO_CACHE :=

.PHONY: all

# ====
# api
# ====

api-build:
	docker compose --env-file api/.env -f api/docker-compose.yml build ${NO_CACHE}

api-up:
	docker compose --env-file api/.env -f api/docker-compose.yml up --force-recreate ${DETACH}

api-down:
	docker compose --env-file api/.env -f api/docker-compose.yml down

api-serve: api-build api-up

# ====
# web
# ====

web-build:
	docker compose --env-file web/.env -f web/docker-compose${TARGET}.yml build ${NO_CACHE}

web-up:
	docker compose --env-file web/.env -f web/docker-compose${TARGET}.yml up --force-recreate ${DETACH}

web-down:
	docker compose --env-file web/.env -f web/docker-compose${TARGET}.yml down

web-serve: web-build web-up

# ======
# nginx
# ======

nginx-build:
	docker compose --env-file api/.env --env-file web/.env -f nginx/docker-compose.yml build ${NO_CACHE}

nginx-up:
	docker compose --env-file api/.env --env-file web/.env -f nginx/docker-compose.yml up --force-recreate ${DETACH}

nginx-down:
	docker compose --env-file api/.env --env-file web/.env -f nginx/docker-compose.yml down

# ====
# all
# ====

build: api-build web-build nginx-build

all: api-up nginx-up

down: nginx-down api-down
