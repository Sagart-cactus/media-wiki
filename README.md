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

```npm install -g aws-cdk```

For more details visit : https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html

Check if the CDK has been installed properly

```cdk --version```

## Step 2: Git Clone
Clone the repository

```git clone git@github.com:Sagart-cactus/media-wiki.git```

## Step 3: Get a hang of CDK and Deploy
goto the CDK directory. Assuming you are still in the directory from where you have executed `Step 2` 

```cd media-wiki\cdk\```

We create a seperate .venv environment so that we do not break or include something global.

```source .venv/bin/activate```

Install all the dependencies

```python -m pip install -r requirements.txt```

You are now all set to go ahead with CDK. Lets first do a list of stacks that are going to be created

`cdk ls`

If this gives you output go ahead and deploy our stack

`cdk deploy --all`

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

We will first create the mysql server, we will need to execute the below command. You will need to modify the credentials of the db

`mysql_root_password`
`mysql_user_password`