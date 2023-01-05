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

- This repo contains:
	- 4 Dockerfiles, to build docker images for Kong, Django, Keycloak and Nginx.
	- A Makefile can be used to run commands that build, run & push docker containers to AWS container registry.
	- `/tasks` that directory holds aws task definitions.
	- `/certs` that directory holds letsencrypt ssl certs for Nginx.

## Usage
- *Update .dev.env with valid values. Current values in .dev.env should not be used in production*
- *Images can run on Docker or AWS Fargate.*

### To run on Docker
1. Clone the repository
2. Build the docker images by running:
	- make build-kong
	- make build-nginx
	- make build-keycloak
	- make build-django
3. Run on Docker using:
	- make run-kong
	- make run-nginx
	- make run-keycloak
	- make run-django

### To run on AWS
*Install AWS-CLI before you proceed*
1. Clone the repository.
2. Add the following to your enviroment.
	- export ECS_REGISTRY_ALIAS=your-aws-registry-alias
	- export ECS_ALIAS=your-aws-ecs-region
3. Login to AWS-CLI; run, make login-aws-cli.
4. Push the images to AWS Container Registry
	- make push-kong
	- make push-nginx
	- make push-keycloak
	- make push-django
5. Run images using task-definations
