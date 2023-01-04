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
 
#### 2. Setup Django APP http://app.kauth.okzk.com
1. Login at https://app.kauth.okzk.com/admin or whichever subdomain you designated in dns.he.net.
2. Find the admin default credentials in create-admin.sh script.
3. Go to Oauth clients click add.![enter image description here](https://i.imgur.com/yaK9EXu.png)
4. Set the following fields and save:
	- user -> djadmin
	- client id -> kauthapp
	- client secret -> client secret for kauthapp client on Keycloak
	- realm -> master
## TODO
1. Add OAuth as an alternative login method.
2. Use a realm besides master realm on Keycloak.
