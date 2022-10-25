build-clean: prune-containers prune-images prune-all
dj-setenv:	
	grep -P '^DJ' .dev.env > /tmp/.djvars && sed -i 's/DJ/export DJ/g' /tmp/.djvars
dj-checkenv:
	env | grep '^DJ' | tr '=' '\t' | awk '{print $$1}'


prune-containers:
	sudo docker container prune --force
prune-images:
	sudo docker image rm keycloak-build kong-build nginx-build --force
prune-all:
	sudo docker system prune --force

build-keycloak:
	sudo docker build -f Dockerfile.keycloak . -t keycloak-build --no-cache
build-kong:
	sudo docker build -f Dockerfile.kong . -t kong-build --no-cache
build-nginx:
	sudo docker build -f Dockerfile.nginx . -t nginx-build --no-cache
build-django:
	sudo docker build -f Dockerfile.django . -t django-build --no-cache

run-kong:
	sudo docker run -d --net=host -p 127.0.0.1:8000:8000 -p 127.0.0.1:8001:8001 --env-file .dev.env kong-build
run-keycloak:
	sudo docker run -d -p 127.0.0.1:8042:8042 --env-file .dev.env keycloak-build
run-nginx:
	sudo docker run -d --net=host -p 0.0.0.0:80:80 -p 0.0.0.0:443:443 -p 0.0.0.0:8443:8443 nginx-build
run-django:
	sudo docker run -d  -p 127.0.0.1:8080:8080 --env-file .dev.env django-build

push-keycloak:
	sudo docker build -f Dockerfile.keycloak . -t keycloak-build --no-cache
	sudo docker tag keycloak-build:latest public.ecr.aws/${ECS_REGISTRY_ALIAS}/keycloak-build:latest
	sudo docker push public.ecr.aws/${ECS_REGISTRY_ALIAS}/keycloak-build:latest
push-kong:
	sudo docker build -f Dockerfile.kong . -t kong-build --no-cache
	sudo docker tag kong-build:latest public.ecr.aws/${ECS_REGISTRY_ALIAS}/kong-build:latest
	sudo docker push public.ecr.aws/${ECS_REGISTRY_ALIAS}/kong-build:latest
push-nginx:
	sudo docker build -f Dockerfile.nginx . -t nginx-build --no-cache
	sudo docker tag nginx-build:latest public.ecr.aws/${ECS_REGISTRY_ALIAS}/nginx-build:latest
	sudo docker push public.ecr.aws/${ECS_REGISTRY_ALIAS}/nginx-build:latest
push-django:
	sudo docker build -f Dockerfile.django . -t django-build --no-cache
	sudo docker tag django-build:latest public.ecr.aws/${ECS_REGISTRY_ALIAS}/django-build:latest
	sudo docker push public.ecr.aws/${ECS_REGISTRY_ALIAS}/django-build:latest
login-aws-cli:
	sudo aws ecr-public get-login-password --region ${ECS_REGION} | docker login --username AWS --password-stdin public.ecr.aws/${ECS_REGISTRY_ALIAS}
