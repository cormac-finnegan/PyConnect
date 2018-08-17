import boto.ec2
from boto import config
import boto.sns
import boto.s3
import boto.ec2.cloudwatch
import libcloud.security
import boto.ec2.elb

aws_access_key_id = config.get('CREDENTIALS', 'aws_access_key_id') #obtained using boto file
aws_secret_access_key = config.get('CREDENTIALS', 'aws_secret_access_key') #obtained using boto file


class Connection:
    def __init__(self):
        self.region = 'eu-west-1' #Defines the region

    def ec2Connection(self):
        # Create and return an EC2 Connection
        connEC2 = boto.ec2.connect_to_region(self.region, aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key)
        return connEC2

    def S3_connection(self):
        # Create and return an S3 Connection
        connS3 = boto.s3.connect_to_region(self.region, aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key )
        return connS3
    def SNS_connection(self):
        # Create and return an SNS Connection (for creating the alarm)
        sns = boto.sns.connect_to_region(self.region, aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key )
        return sns


    '''Open Stack functionality is hardcoded in, should only need to be changed here. All connections calls are made using this'''
    def open_stack_connection(self, storage): #storage argument is used to differentiate whether a compute or storage driver is returned
        USER = 'cormac.finnegan'
        API_KEY = 'q4HknWgHiazLyaGw'
        AUTH_URL = 'http://128.136.179.2:5000'

        '''IMPORTANT: local directory for the security certificate should be changed to suit'''
        libcloud.security.CA_CERTS_PATH = ['E:/School/ca-bundle.crt']

        if storage:
            from libcloud.storage.types import Provider
            from libcloud.storage.providers import get_driver
            provider = get_driver((Provider.OPENSTACK_SWIFT))
        else:
            from libcloud.compute.types import Provider
            from libcloud.compute.providers import get_driver
            provider = get_driver(Provider.OPENSTACK)

        '''driver connection established here'''
        driver = provider(USER, API_KEY, ex_force_auth_url=AUTH_URL,
                            ex_force_auth_version='2.0_password',
                            ex_tenant_name='cormac.finnegan',
                            ex_force_service_region='RegionOne')
        return driver

    def cloud_watch_connection(self):
        connCW = boto.ec2.cloudwatch.connect_to_region(self.region, aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key)
        return connCW

    def elastic_load_balancing_connection(self):
        elb_conn = boto.ec2.elb.connect_to_region(self.region, aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key )
        print elb_conn
        return elb_conn

