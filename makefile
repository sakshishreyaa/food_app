app:
	sudo docker-compose build
	sudo docker-compose up -d
	sudo docker-compose logs 
terminate:
	sudo docker-compose down

test:
	sudo docker-compose build
	sudo docker-compose up -d
	sudo docker exec food_app_food_app_1 ls
	sudo docker exec food_app_food_app_1 pytest food_app --disable-warnings || true
	sudo docker-compose logs food_app_food_app_1
	sudo docker-compose stop
	sudo docker-compose down

database:
	flask db init
	flask db migrate
	flask db revision -m "revision_name"
	flask db upgrade
	
# kill -9 $(ps -A | grep python | awk '{print $1}')


