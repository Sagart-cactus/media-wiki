# Install Mediawiki using AWS CDK and Ansible

## Prerequisite
This code written assumes that the system executing it has the following things installed.

- `node` and `npm`
- `python3`
- aws cli v2

This code is account and region agnostic, It will get created in the default region of the AWS profile which is used to execute it. Due to a force of habbit and a very late realization there is a hardcoded `mu` for `ap-south-1` in the name of the stacks and entities, but what is in the name right? 😉

There are many things that I would have done more elegantly but due to time constraints. I have created a basic structre. 

## Step 1: Install CDK
install the CDK globally via `npm`. This is a command line tool and I suggest you set it up globally.

```
npm install -g aws-cdk
```

For more details visit : https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html

Check if the CDK has been installed properly

```
cdk --version
```
We will need CDK 1.121 for this stack

## Step 2: Git Clone
Clone the repository

```
git clone git@github.com:Sagart-cactus/media-wiki.git
```

## Step 3: Get a hang of CDK and Deploy
goto the CDK directory. Assuming you are still in the directory from where you have executed `Step 2` 

```
cd media-wiki\cdk\
```

We create a seperate .venv environment so that we do not break or include something global.

```
python3 -m venv .venv 
source .venv/bin/activate
```
Make sure that you have virtual env installed on your system, you can do so by  `sudo apt install python3.8-venv`

Install all the dependencies

```
python -m pip install -r requirements.txt
```

You are now all set to go ahead with CDK. Lets first do a list of stacks that are going to be created

```
cdk ls
```

If this gives you output go ahead and deploy our stack

```
cdk deploy --all
```
You would be asked whether you want to deploy changes related to security like opening up ports etc. You will have to press `y` to proceed. If you trust me with your account and do not like pressing `y` every now and then use `--require-approval never` flag.

## Install the App on the servers created.
The above steps have just created blank server with just ansible installed in them. We will execute a few ansible playbooks to install the media-wiki server.

## Executing Ansible Playbooks without the hassles of Keys SSM way
We will use SSM run command to execute playbooks on the respective App and DB servers. This is a great way to execute playbooks as we have
- Better security
    - There is no need to open incoming ports to remotely execute the directives. This eliminates the need for using SSH
    - You can use IAM to restrict and control access to the platform
    - All command execution is audited via AWS Cloudtrail
- Performance and reliability
    - Asynchronous execution of commands
    - Commands are delivered and executed even when the system comes back from being offline
    - Execute at scale by taking advantage of velocity control
    - Control deployment rate if errors increase during deployment

## Using an Intermediate S3 Bucket
We can acutally execute the ansible roles directly from the Github repo itself. But for this example we will use an intermediate S3 Bucket as github option often faces rate limiting for public Repos and It will be an additional hassle for you to configure the github access tokens.

Push all the ansible books to an S3 bucket created by the CDK stack above
```
cd media-wiki/ansible/create-web-server
aws s3 cp . s3://ansible-deployment-prod/create-web-server/ --recursive
```

## Creating MySQL server first
We will first create the mysql server, we will need to execute the below command But before that, you will need to modify the credentials of the db (if you want a more secure password) by changing the values of `mysql_root_password=supersecure@123` and `mysql_user_password=sagart@123` in the below command.

```
aws ssm send-command --document-name "AWS-ApplyAnsiblePlaybooks" --document-version "1" --targets '[{"Key":"tag:app_type","Values":["app_server"]}]' --parameters '{"SourceType":["S3"],"SourceInfo":["{\n\"path\":\"https://s3.amazonaws.com/ansible-deployment-prod/create-web-server/\"\n}"],"InstallDependencies":["True"],"PlaybookFile":["mysql.yaml"],"ExtraVariables":["SSM=True\nmysql_root_password=supersecure@123\nmysql_user_password=sagart@123"],"Check":["False"],"Verbose":["-v"],"TimeoutSeconds":["3600"]}' --timeout-seconds 600 --max-concurrency "50" --max-errors "0" --output-s3-bucket-name "ansible-deployment-prod" --output-s3-key-prefix "execution-output"
```
The above command will take some time. You will need to check the status of the command on `https://{{your-region}}console.aws.amazon.com/systems-manager/run-command/executing-commands?region={{your-region}}`

The above command will
- install `mysql` server
- set the root password to the specified password
- create a user `example_user` with the specified password (you can change the name in the ansible script if you want before you upload it to the S3 server)
- create a database named `example_db`
- Assign access to `example_user` to `example_db`

## Creating the Media-wiki App server
For creating the Media-wiki server we will execute another ansible playbook with the same method. This time we will need the following details
- Private IP of the MySQL server (The localhost itself for now)
- Password of `example_user` set in the above mysql ansible playbook
- Name of the Wiki Host (This is set to public IP of the instance for Now)
- Password for the admin user that will be created.

```
export SERVER_IP=$(aws ec2 describe-instances --query "Reservations[].Instances[][PublicIpAddress]" --filter "Name=tag:app_type,Values=app_server" "Name=instance-state-name,Values=running" --output text)
```

The above step will get the public IP of the ec2 instance and store it in the `SERVER_IP` env variable.

Then we execute this.
```
aws ssm send-command --document-name "AWS-ApplyAnsiblePlaybooks" --document-version "1" --targets '[{"Key":"tag:app_type","Values":["app_server"]}]' --parameters '{"SourceType":["S3"],"SourceInfo":["{\n\"path\":\"https://s3.amazonaws.com/ansible-deployment-prod/create-web-server/\"\n}"],"InstallDependencies":["True"],"PlaybookFile":["apache2-server.yaml"],"ExtraVariables":["SSM=True\nmysql_password=sagart@123\nmysql_host=localhost\nwiki_host=http://'$(echo $SERVER_IP)'\nadmin_pass=supersecure@123"],"Check":["False"],"Verbose":["-v"],"TimeoutSeconds":["3600"]}' --timeout-seconds 600 --max-concurrency "50" --max-errors "0" --output-s3-bucket-name "ansible-deployment-prod" --output-s3-key-prefix "execution-output"
```

The above command will take some time. You will need to check the status of the command on `https://{{your-region}}console.aws.amazon.com/systems-manager/run-command/executing-commands?region={{your-region}}`

## Visting out Test Mediawiki

Once the above playbook are executed, Enter this command and visit the link given in the output.
```
echo "http://$SERVER_IP/mediawiki-1.36.1/"
```

## Things I would have done differently in this system
There are many things I would have done this differently

### Code from the Github
The install guide given as the reference has only a tar file that contains the mediawiki app along with its dependencies. I have no experience in maintaining and creating MediaWiki but I would like to use github code as the source and build the dependency on the server using composer. This would also help in the **CI and CD of the changes** in the code.

### Separate MySQL and App server
The reference doc specifies that mysql and application to be installed in the same server. Using this config we cannot horizontally scale this system. An ideal solution would be an ALB and 2-3 app servers in Autoscaling behind the ALB and a separate MySQL server. In order to make this happen we will have to use some extensions/configurations like 
- https://www.mediawiki.org/wiki/Redis - To maintain the sessions and cache
- https://www.mediawiki.org/wiki/Extension:AWS - To store the media files to S3

### Better way to manage credentials
I would have used secure SSM parameter store or secrets manager to store the password and credentials for the Stack/Database.

### Alarms and Monitoring
I would have added atleast CPU and Disk Monitoring on the servers for better visibility.
