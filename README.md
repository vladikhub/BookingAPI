git config user.name "Влад Смольков"
git config user.email "smavl.andrey@gmail.com"
docker network create myNetwork
docker build -t booking_image . 
docker run --name booking_db -p 6432:5432 -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=booking --network=myNetwork --volume pg-booking-data:/var/lib/postgresql/data -d postgres:17
docker run --name booking_cache -p 7379:6379 --network=myNetwork -d redis:7.4
docker run --name booking_backend -p 8888:8000 --network=myNetwork booking_image
docker run --name booking_celery_worker --network=myNetwork booking_image celery --app=src.tasks.celery_app:celery_instance worker -l INFO
docker run --name booking_celery_beat --network=myNetwork booking_image celery --app=src.tasks.celery_app:celery_instance worker -l INFO -B
docker run --name booking_nginx --volume ./nginx.conf:/etc/nginx/nginx.conf --network=myNetwork --rm -p 80:80 nginx