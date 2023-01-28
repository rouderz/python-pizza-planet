seed: docker-run
	export database="postgresql://pizza:pizzaplanet@localhost:5432/pizzaplanet" && \
	python ./manage.py seed run --root app/seeds

run-project: docker-run
	export database="postgresql://pizza:pizzaplanet@localhost:5432/pizzaplanet" && \
	export FLASK_ENV=development && \
	python manage.py run 

run-project-windows: docker-run
	set database="postgresql://pizza:pizzaplanet@localhost:5432/pizzaplanet" && \
	set FLASK_ENV=development && \
	python manage.py run 

coverage:
	coverage run --source=app -m pytest -v app/test && coverage report -m

docker-run:
	docker-compose up -d

docker-stop:
	docker-compose down
