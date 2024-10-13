# US-TX-Family_Law
## Docassemble Package for Family Law forms in Texas, United States
### Author: Thomas J. Daley, J.D.

# Available Interviews

## Inventory & Appraisement

## Notice to Vacate

## Promissory Note for Loan for Legal Fees

## Roommate Early Move Out Incentive Agreement

# Restarting After a Shutdown

Docker is not automatically starting at this point. Here is how to resume the system.

## 1. Open the Lightsail Console

Navigate to the [Lightsail Conole](https://lightsail.aws.amazon.com/ls/webapp/us-east-2/instances/DocAssemble-01/connect?#)

## 2. Connect to the Lightsail Instance

1. Find the instance that relates to docassemble, currently Amazon Linux 2
1. Click on the "Connect" tab
1. Click "Connect using SSH"

## 3. Restart the Docker Damon

```
$ sudo service docker restart
```

## 4. Get the Instance ID of the docassemble container

```
$ docker ps -a
```

You will get a list of containers (probably only 1) that looks like this:

```
CONTAINER ID   IMAGE                COMMAND                  CREATED        STATUS                    PORTS     NAMES
4fe056b5ca06   jhpyle/docassemble   "/usr/bin/supervisor…"   9 months ago   Exited (0) 19 hours ago             condescending_payne
```

## 5. Restart the Container

**DO NOT** start a new container. Doing so will create a totally new docassemble instance which you will have to completely reconfigure.

From the above output, note the **CONTAINER ID**, which in this example is 4fe056b5ca06. Use this container ID to restart the conainer.

```
$ docker start 4fe056b5ca06
```

## 6. Wait for DocAssemble to Restart and Settle Down

You can keep reloading [da.jdbot.us](https://da.jdbot.us). At first it will not respond, but once docassemble settles down, the web site will respond as expected.


# Starting a New Container

If you have to start a new container, may heaven have mercy on your soul because these notes are not great.

## 1. Get Configuration File

If you have a running instance, you can copy the configuration to a text file and use it in you new container. If you do not have a running instance and have no way to recover the last working configuration, there is a configuation.txt file on the developer's laptop. (Tom's Surface)

## 2. Connect to the Server

If you are using Amazon Lightsail, use the instructions above to connect to the server instance.

## 3. Install Docker

Install Docker per [jhpyle's Notes](https://docassemble.org/docs/docker.html#install)

## 4. Install Docassemble

The following docker command will install docassemble and start it in a container:

```
docker run -d -p 80:80 -p 443:443 --restart always --stop-timeout 600 jhpyle/docassemble
```

## Install Packages

1. Install Document Assembly Line following the [publisher's instructions](https://assemblyline.suffolklitlab.org/docs/get_started/installation/)

1. Install UsTxFamilyLaw using this [git repository](https://github.com/tjdaley/docassemble-UsTxFamilyLaw)

## 5. Update the Configuration

Go to the "Configuration" page and paste in the configuration file you obtained in step one.

If you had to resort to an old, possibly out of date configuration file, you might want to just adjust the configuration based on comparing the differences between the configuration that appears on the configuration page and the configuration file you located.