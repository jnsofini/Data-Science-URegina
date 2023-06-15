"""
Code to generate figure for a configuration of EC2 which can access an S3 bucket to read/write objects.
"""

from diagrams import Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.security import (
    IdentityAndAccessManagementIamPermissions as IAMPermissions,
    IdentityAndAccessManagementIamRole as IAMRole 
    )
from diagrams.aws.devtools import CommandLineInterface as CLI 
from diagrams.aws.storage import SimpleStorageServiceS3BucketWithObjects as s3wo
from  diagrams.aws.management import SystemsManagerParameterStore as ParameterStore 

with Diagram("Server With S3 Backend",  outformat=["pdf", "png"]):
    policy = IAMPermissions("IAM policy file with permissions")
    role = IAMRole("IAM role")
    server = EC2("AWS EC2 Instance")
    cli = CLI("AWS Command Line Interfeace")
    s3 = s3wo("Amazon S3")
    params = ParameterStore("Parameter Store")

    policy >> role >> server >> cli >> s3 
    server << Edge(color="brown", style="dashed", arrowhead="both") << params
    params << Edge(color="brown", style="dashed", arrowhead="both") << server
    cli >> server
    s3 >> cli
 