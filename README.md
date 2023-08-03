# Learning

In this repository, I plan to share both raw and cleaned up things that I am working on. My aim is to curate this as a training that can be delivered for data science and ml. Each of the directories will be a stand alone and can be used seprately.

## Infrastructure

 Here we have description or how insfrature used for ML and DS are set.

### [Compute Server Backed by S3](Infrastructure/compute-server-storage)

Here we have terraform code to provision EC2 that can connect to an S3 bucket backend

## [Clustering](Clustering)

This folder contains anything clustering. Included as simple files to

- Identify optimal cluster size

## [Code Quality](CodeQuality)

When our code set starts to grow and when we are building highly sensitive applications, we cannot ignore the code quality. There is static code analysis that helps us identify bugs but there are also analysis for security. SonarQube offers sonar scanner which can help identify security vulnerabilities in out code as well as analysis of test cases when they fail.

## [Streaming](streaming)

This folder contains streaming projects. At the moment we have a demo project on how to use lambda to process streaming events and push the results to another service. This is located in [Streaming/demo](Streaming/demo/)

## [Scorecard](AutoScorecard)

This folder contains code to build a scorecard automatically. The scorecard model is capable of generating scores from within a range analogous to probabilities ranging from 0 to 1.
