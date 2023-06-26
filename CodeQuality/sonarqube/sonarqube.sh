#!/bin/bash
docker run --rm --net=host -v ${PWD}:/SonarQube-flask sonarsource/sonar-scanner-cli sonar-scanner -D sonar.projectBaseDir=/SonarQube-flask