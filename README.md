## Must Have
1.  [https://dns.he.net](https://dns.he.net) account(or similar)
2.  [https://freedns.afraid.org](https://freedns.afraid.org) account(or similar)
3.  Wild card SSL certificates (https://punchsalad.com) for any domain selected in (2)
4.  Remote PostgreSQL database (like RDS)
5.  Google OAuth credentials

> With valid accounts in dns.he.net and freedns.afraid.org, you can
> generate a wildcard ssl certificate, and assign subdomains to each
> service getting setup.

## Getting a domain name.
#### Freedns.Afraid.org
1. Log into freedns.afraid.org
2. Click on registry
3. Click on your preferred domain
4. Using the drop down set TYPE to NS
5. Enter your preferred subdomain name in the subdomain field
6. Enter “ns1.he.net” in the destination field.
7. Fill in the captcha and click save
#### Dns.He.Net
1. Log into dns.he.net
2. Click on add a new domain
3. Enter the FQDN you just reserved on freedns.afraid.org
4. Click add domain
5. If you get a zone validation failed error. Try again after a while - the DNS records may take a while to propagate. You can use whatsmydns.net to monitor propagation.
6. Create the following subdomains - oidc, api, and app
    * Click New A
    *  Enter a subdomain name, server IP address, and set TTL to 5 mins
    * Click submit.
#### Wildcard SSL Certificate
1.  Go to [https://punchsalad.com/ssl-certificate-generator/](https://punchsalad.com/ssl-certificate-generator/)
2.  Enter the domain name from dns.he.net starting with an asterisk *.subdomain.domain.tld
3.  Enter an email address
4.  Select DNS
5.  Accept the TOS
6.  Click create
7.  Download the certificates, and upload them to the server - place them in the /certs in /Kauth.
8.  Rename the certificates - ca-bundle to bundle.crt, and private-key to priv.key
#### AWS RDS
1. Create databases for Kong, Keycloak and Django
## Configuration
1.  Update the .dev.env file with the correct database credentials for keycloak, kong, and django
2.  Update the .dev.env and the nginx.conf file with the respective hostnames created in dns.he.net
3.  Export the following environment variables
    * export DJ_DB_PASS=
    * export DJ_DB_HOST=
    * export ECS_REGISTRY_ALIAS=
    * export ECS_REGION=
    * export KONG_PG_HOST=
    * export KONG_PG_USER=
    * export KONG_PG_PASSWORD=
#### Setup Server (UBUNTU 22.04 lts)
-   Install Docker
    * sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
- Install Make
   * sudo apt install make
- Install AWSCLI
   * sudo apt install awscli
#### Prepare docker images
- Nginx
  1. make build-nginx
  2. make run-nginx
- Django
  1. make build-django
  2. make run-django
 - Keycloak
   1. make build-keycloak
   2. make run-keycloak
  - Kong
    1. make build-kong
    2. make migrate-kong
    3. make run-kong

#### Check docker containers
```sudo docker container ls```

![enter image description here](https://i.imgur.com/kiWICtu.png)

## Services
This project integrates three services, which should be accessible via subdomains created at https://dns.he.net. This repo is configured using https://kauth.okzk.com.
1. Keycloak OAuth - https://oidc.kauth.okzk.com
2. Django DRF - https://app.kauth.okzk.com
3. Kong API Gateway - https://api.kauth.okzk.com

![enter image description here](https://i.imgur.com/yDA6SMR.png)

#### 1. Setup Keycloak http://oidc.kauth.okzk.com
1. Login at https://oidc.kauth.okzk.com. Find the credentials in the .dev.env file.
2. Go to Clients > Create Client
3. Enter kauthapp in the client id field and save
4. Go to Clients > kauthapp > Service Account Roles
5. Click Assign Role
6. Click Filter by Origin dropdown, select master-realm.![enter image description here](https://imgur.com/DlWZQWS.png)
7. Search for manage-users. 
![enter image description here](https://imgur.com/qXlWzv8.png)
8. Select manage-users, then click Assign.
9. Go to Clients > kauthapp > Settings > Capability Config 
10. Turn on Client authentication, select Standard flow, Service accounts roles then Save. ![enter image description here](https://imgur.com/P8URLv9.png)
11. Go to Clients > kauthapp > Credentials > Client secret
12. Copy the Client secret.
13. Go to Clients > kauthapp > Advanced > Advanced Settings
14. Set Access Token Lifespan to 1 days (24hrs). ![enter image description here](https://imgur.com/lYKn5I6.png)
 
#### 2. Setup Django APP http://app.kauth.okzk.com
1. Login at https://app.kauth.okzk.com/admin or whichever subdomain you designated in dns.he.net.
2. Find the admin default credentials in create-admin.sh script.
3. Go to Oauth clients click add.![enter image description here](https://i.imgur.com/yaK9EXu.png)
4. Set the following fields and save:
     - user -> djadmin
     - client id -> kauthapp
     - client secret -> client secret for kauthapp client on Keycloak
     - realm -> master

## API DOCUMENTATION
#### Authentication
1. Get a user account from https://app.kauth.okzk.com
2. Copy the api key from the users profile page ![enter image description here](https://imgur.com/zKwuWgW.png)
3. Send the apikey in the header to retrieve an accesstoken
    - Using curl      
    ```curl -H "apikey:m0j5ygb94v2IrNFLjB0vHxul5C3IpnYI" https://api.kauth.okzk.com/oauth/tokens/```
    - Using httpie 
```http api.kauth.okzk.com/api/v1/oauth/tokens/ apikey:m0j5ygb94v2IrNFLjB0vHxul5C3IpnYI```
4. The API will send the access token in a response
     ```{
    "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ4cHEyN3Jib1hqdE1XTUo0S1VHQmFWbElYbFhURjJLVkVvcktJQlpGOGI4In0.eyJleHAiOjE2NzI4OTc3OTcsImlhdCI6MTY3Mjg2MTc5NywianRpIjoiZGU5YWU2NjYtMWI1Zi00MDBlLWE1YzctYjdkNTE1YzI4Y2E4IiwiaXNzIjoiaHR0cHM6Ly9vaWRjLmthdXRoLm9remsuY29tL3JlYWxtcy9tYXN0ZXIiLCJhdWQiOlsibWFzdGVyLXJlYWxtIiwiYWNjb3VudCJdLCJzdWIiOiI0NmEzYzg3OC00Yjc1LTQ1OGUtYmUwMC1iM2E5OWUxN2E3NmQiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJrYXV0aGFwcCIsImFjciI6IjEiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy1tYXN0ZXIiLCJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsibWFzdGVyLXJlYWxtIjp7InJvbGVzIjpbIm1hbmFnZS11c2VycyJdfSwiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJwcm9maWxlIGVtYWlsIiwiY2xpZW50SWQiOiJrYXV0aGFwcCIsImNsaWVudEhvc3QiOiIxNzIuMTcuMC4yIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJzZXJ2aWNlLWFjY291bnQta2F1dGhhcHAiLCJjbGllbnRBZGRyZXNzIjoiMTcyLjE3LjAuMiJ9.j6MJB14VEYbuwOOMqh_3ZNz7H42u_0HnFiuT8_Oq-IPO0EvJFN_KIHCyvetM8MLVANTp3HXqIdtm6oA2nBeEClOubrCYBrnrx_X6ABfxTCfFMnneuIEvJNZwQeYEZ6yt1KZXF_A2wrIFMyjl2iey8MK6s_5lGaQJAJRpNDZCplthY_DJbrTwkJf5wfdn9aTXpnyi1brGhm5Jf74HSND_F2uPNWYPlh1ahbGABeP1TsmmJHV8Sk23tQvG2Upxdue8A7sknF5_DdRe5Ndwv-tpMRTVaJMQ5L0fZD1oLj0d1b74hhv0txtibZo1RWqsu4_FUElXFqcLmRTE8FA-BIYg-g",
    "expires_in": 36000,
    "not-before-policy": 0,
    "refresh_expires_in": 0,
    "scope": "profile email",
    "token_type": "Bearer"
}```

#### Endpoints
USERDATA 

**retrieve | status code 200**
```
GET /api/v1/users/userdata
Authorization: Bearer access_token

http api.kauth.okzk.com/api/v1/users/userdata/

[{"content": "Compilers are important", "id": 1}]
```
**create | status code 201**
```
POST /api/v1/users/userdata
Authorization: Bearer access_token

echo -n '{"content": "Another compiler post"}' | http api.kauth.okzk.com/api/v1/users/userdata
```
**delete  | status code 204**
```
DELETE /api/v1/users/userdata
Authorization: Bearer access_token

http DELETE api.kauth.okzk.com/api/v1/users/userdata/ id=1
```

USERDATAPOINTS

**retrieve | status code 200**
```
GET /api/v1/users/userdatapoints
Authorization: Bearer access_token

http GET api.kauth.okzk.com/api/v1/users/userdatapoints/

[{"content": "Datapoints for compilers", "id": 3}]
```
**create | status code 201**
```
POST /api/v1/users/userdatapoints
Authorization: Bearer access_token

echo -n '{"content": "Datapoints for compilers"}' | http POST api.kauth.okzk.com/api/v1/users/userdata/userdatapoints
```
**delete  | status code 204**
```
DELETE /api/v1/users/userdatapoints
Authorization: Bearer access_token

http DELETE api.kauth.okzk.com/api/v1/users/userdatapoints/ id=3
```

## TODO
1. Add OAuth as an alternative login method.
2. Use a realm besides master realm on Keycloak.
