# Ansible playbook to install and configure an apache server

This playbook should be executed when you have to create an apache server. You will have to create a server with our ubuntu base AMI and make sure you have SSH access to the server. The newly created server should have python up and running.

## Checklist/Pre-requisite before we execute the playbook
There are a few files and variables we need to define before we can execute this script.

### Hosts
Please add the name and ip address of all the servers where you want the playbook to be executed in the `host` file in the root directory. Server group name in  `[]` followed by name and ip address
``` 
[insights-korea]
temp_server01 ansible_host=15.164.120.190
temp_server02 ansible_host=15.164.120.191 
```
### Apache2
This role is used to install and configure apache2 server. Any addition to be made in the `/etc/apache2/apache2.conf` file should be added in `apache-server/roles/apache2/files/block_apacheconf`. Changes that are to be made in the site-enabled conf file should be made in `apache-server/roles/apache2/templates/virtualhost` file.
 
#### Variables for apache server
You will need to populate the following values in the `apache-server/roles/apache2/vars/main.yml`
##### http_port
Port number to forward your **http** traffic eg: `http_port: 80`
##### https_port
Port number to forward your **https** traffic eg: `https_port: 8080`
##### ServerName
Name of the server to be put in the Virtual host eg: `ServerName: editage.co.kr`
##### ServerAlias
Server alias to be put in the VirtualHost file eg: `ServerAlias: editage.co.kr www.editage.co.kr *.editage.co.kr`
##### domain
Name of the domain to be used in the site-enalbed conf filename eg: `domain: editage.co.kr` 
##### home_directory
Root directory of the site where to look for the web contents eg: `home_directory: '/var/www/html'`
##### packages
List of Packages that should be installed. Please do not modified the first item in the list `apache`. You can add any modules you would like to install with the apache server  
eg:
```
packages:
  - apache2
  - libapache2-mod-php7.2
```

The entire `apache-server/roles/apache2/vars/main.yml` file looks like this
``` yaml

--- 
# vars file for apache2
http_port: 80
https_port: 8080
ServerName: editage.co.kr
ServerAlias: editage.co.kr www.editage.co.kr *.editage.co.kr
domain: editage.co.kr
home_directory: '/var/www/html'
packages:
  - apache2
  - libapache2-mod-php7.2
```

### PHP 7.2
This role will install PHP 7.2
#### Variables for PHP file
You will need to populate the following values in the `apache-server/roles/php7.2/vars/main.yml`
#####packages
List of Packages that should be installed. Please do not modified the first item in the list `php7.2`. You can add any modules you would like to install with php

The entire `apache-server/roles/php7.2/vars/main.yml` file looks like this
``` yaml

---
# vars file for php7.2
packages:
  - php7.2
  - php7.2-mysql
  - php7.2-curl
  - php7.2-gd
  - php7.2-json
  - php7.2-mbstring
```

### User creation for deployment
The playbook will also create a user for deployment. We need to add its ssh keys. The keys that are added with this playbook should be added as the deploy keys in the github repo.
To change the keys you should add the keys in the `apache-server/roles/user_roles_keys/files/keys/` folder by creating the following folder structure for each user to be inserted. 
```
.
└── keys
    └── deploy
        ├── id_rsa
        └── id_rsa.pub

```
here deploy is the name of the user to be created.
#### Variables for user creation
##### user
Name of the user to be created

## Execution of the Playbook
Goto the root directory of the playbook and use the following command to execute the playbook
### Apache2 server 
```
ansible-playbook -i hosts apache2-server.yaml
```
### Nginx server
```
ansible-playbook -i hosts nginx-server.yaml
``` 
