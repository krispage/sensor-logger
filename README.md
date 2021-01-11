## Docker build
docker build . -t flask_template:latest

## Docker run
sudo docker run -p 8000:5000 flask_template:latest

## Add user
### Running locally
flask cmd create_user admin blabla
### Docker
docker exec -i \<CONTAINER ID> /bin/sh -c "export FLASK_APP=/etc/flask/src/flask_app/main; flask cmd create_user myuser mypass"
### Docker compose
docker-compose --env-file compose.env up 
