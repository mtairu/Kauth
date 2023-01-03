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
