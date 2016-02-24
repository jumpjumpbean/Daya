sudo docker run -d --name mongo-base mongo

sudo docker build -t="python/gunicorn-flask" .

sudo docker run -d --name gunicorn-flask --link mongo-base:mongo-base python/gunicorn-flask

docker run -d --name nginx -p 80:80 -v ./nginx.conf:/etc/nginx/nginx.conf:ro --link gunicorn-flask:gunicorn-flask nginx
