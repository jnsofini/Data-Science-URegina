# Set up AWS Programmatic Access

In this guide, we will walk you through the process of setting up an AWS user called _terraform-user_ with programmatic access to your AWS account. The _terraform-user_ will be granted administrative privileges. Let's dive into the steps:

## Creating an Account and User

1. Start by [creating an AWS account](https://www.google.com/aclk?sa=l&ai=DChcSEwiXiJX_oqCAAxVxCX0KHSx7DLIYABAAGgJwdg&sig=AOD64_3OKsX2TmS5PEKxZBUkuYTnqPOaZw&q&adurl&ved=2ahUKEwju343_oqCAAxXiMDQIHXOFBr8Q0Qx6BAgGEAE) and log in to the root account.

2. Once logged in, navigate to the IAM console, select "Users," and click on "Add user". ![user](images/account-creation-start.png)

3. Provide the required information for the user and select "Next" to proceed to the permission settings.

4. Choose the option "Attach policy directly" and select the administration policy, then click "Next". ![policy](images/account-creation-policy.png)

5. Review the information and click "Create user" to finalize the creation of the user account. ![create-user](images/account-creation-create.png)

6. Click on the newly created user and go to "Security Credentials". ![credential](images/account-creation-acces-keys-start.png)

7. Select the access key type for programmatic access, and confirm your selection at the bottom. Click "Next," optionally add tags, and then click "Create". ![credential-type](images/account-creation-acces-keys-type.png)

8. The credentials will appear as shown below. ![credentials](images/account-creation-credentials.png)

## Setting Up a Profile

To set up credentials for programmatic access, you need to install the AWS CLI by following the [instructions for your operating system](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html). Confirm the installation by running `aws --version` in the terminal.

With the AWS CLI installed, you can create a profile tied to the permissions in the account you created. Profiles can be named or default. The default profile is automatically loaded by the AWS CLI when running code. It can be optionally specified, whereas the named profile must be specified.

To create a default profile, run the following command in the terminal:

```sh
admin@ubuntu:~$ aws configure
admin@ubuntu:~$ aws configure
```

Output looks like

```sh
AWS Access Key ID [****************KAPE]: AKIAV7GQDWMJHBDNKAPE
AWS Secret Access Key [****************12S0]: MKO8WlfajpYcfoeqMg+1AspjsPj5iNF2T127T 
Default region name [us-east-2]: us-east-2
Default output format [json]: json
admin@ubuntu:~$
```

To configure a named profile (e.g., _terraform-user_), use the following command:

```sh
admin@ubuntu:~$ aws configure --profile terraform-user
admin@ubuntu:~$ aws configure --profile terraform-user
```

Output looks like

```sh
AWS Access Key ID [****************KAPE]: AKIAV7GQDWMJHBDNKAPE
AWS Secret Access Key [****************12S0]: MKO8WlfajpYcfoeqMg+1AspjsPj5iNF2T127T
Default region name [us-east-2]: us-east-2
Default output format [json]: json
admin@ubuntu:~$
```

Check your profiles

```sh
aws configure list-profiles
default
dev
```

Now you are all set to use your AWS account programmatically with the specified credentials and profiles. Happy AWS coding!