## Requirements
 1. Domain/Subdomain with SSL Certificates
     - freedns.fraid.org 
     - dns.he.net
     - https://punchsalad.com (wildcard ssl certificates)
 2. Docker
 3. PostgreSQL
 4. Google OAuth credentials
	 - https://console.cloud.google.com/apis/credentials
 5. AWS Account for
     - AWS CLI https://aws.amazon.com/cli/

|  Requirement| Function |
|--|--|
| Subdomains with SSL | Three subdomains are used in this setup; oidc, app and api. Communication with or between these three domains over SSL is a security requirement |
|Docker|To build and push images to AWS ECS|
|Google & Facebook OAuth||
|Postgres|Kong, Django, Keycloak require database access.|
|AWS|Container registry & AWS Fargate|

-  This repo contains 4 Dockerfiles, which will be used to build docker images. The images will be pushed to ECS registry.
- `/tasks`	directory holds task definitions will can be used to start tasks or serve as a starting point for configuring new task on Fargate.
- The Makefile can be used to run commands that:
	-  build & push containers to AWS container registry.
		- `make push-keycloak` will build and push the keycloak image to the registry.
		- `make build-keycloak` will only build the image
		- `make run-keycloak` will start a container using the keycloak image.
