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
1. Clone the repository
2. Build the docker images by running:
	- make build-kong
	- make build-nginx
	- make build-keycloak
	- make build-django
