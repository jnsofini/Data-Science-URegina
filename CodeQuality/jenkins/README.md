# Project Description

## Jenkins

In the jenkins folder we have a _docker-compose_ file for the services. Run

```sh
docker compose up -d
```

Jenkins is running on port 7000 as specified in the comose file. On the browser open localhost:8080. It will ask for initial password in a login that looks like ![this](jenkins/images/jenkin-welcome-page.png). The passwors is stored securedly in _/var/jenkins_home/secrets/initialAdminPassword_. We can get it from the mount local dir or container as follows

```sh
docker exec jenkins-lts cat /var/jenkins_home/secrets/initialAdminPassword
cat data/secrets/initialAdminPassword
```

Copy the credentials and login to see suggested plugins as ![follows](jenkins/images/jenkins-plugins.png). We can skip this step. If you chose to install, you will have a screen below ![screen](jenkins/images/jenkins-suggested-plugins.png). Create first admins account. Here I use username: admin password:password.

We can create a job normally. To see details on Jenkins jobs, see [Link](Todo).

Finally you get to Jenkins ![dashboard](jenkins/images/jenkins-dashboards.png)

## Creating Job

Create new job in jenkins by clicking new and creating a freestyle project called __sonarqube-flask_ as ![shown](jenkins/images/jenkins-project-freestyle.png).
