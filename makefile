runserver:
	@echo "Starting server..."
	@python manage.py runserver

rundev:
	npm run dev

.PHONY: prod-requirements
prod-requirements:
	poetry export -f requirements.txt --without-hashes -o requirements.txt

.PHONY: collectstatic
collectstatic:
	python manage.py collectstatic --noinput


.PHONY: lint
lint:
	ruff format .
	ruff check . --fix

.PHONY: migration
migration:
	python manage.py makemigrations

.PHONY: migrate
migrate:
	python manage.py migrate