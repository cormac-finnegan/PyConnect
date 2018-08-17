import boto
import datetime
from Connection import Connection
from Compute.AWS.EC2 import EC2Instance
from boto.ec2.cloudwatch import MetricAlarm

class CloudWatchInstance:

    global global_connection #a global connection is used so it can be used without having to call the connect method everytime

    def __init__(self):
        self.connect_to_cw() #init calls the connection method which sets the global_connection

    def enable_cw(self): #function enables ec2instances to be monitored using cloudwatch
        ec2inst = EC2Instance()
        conn0 = ec2inst.connect()
        conn0.monitor_instances(self.get_EC2_instance().id) #invokes the ec2Instance picker from the EC2Instance and specifies the id from the returned EC2Instance returned to be monitored

    def list_metrics(self): #lists the standard metrics for a particular instance
        instance = self.get_EC2_instance() #get a user chosen instance from the EC2 Class
        metrics = global_connection.list_metrics() #list the available metrics
        my_metrics=[] # Create a new empty array to store the metrics aplicable to the chosen instance
        if (instance != '*'):
            for metric in metrics: #for each given metric in the metric list
                if 'InstanceId' in metric.dimensions: #find the 'InstanceId' label in the metric list
                    if instance.id in metric.dimensions['InstanceId']: #if the id of the user's chosen instance matches the instance id in the 'InstanceId' metrics
                        my_metrics.append(metric) #append it to my_metric array as it applies to the user's chosen instance

        for my_metric in my_metrics: #for each of the metrics in the applicable metric array
            statistic = global_connection.get_metric_statistics( #list the statistics of the metric
                                        300, #The period between checks, in seconds, of the returned datapoints. Period must be a multiple of 60
                                        datetime.datetime.utcnow() - datetime.timedelta(seconds=600), #the current time obtained using python's datetime subtracting by the same time, but 10 mins earlier
                                        datetime.datetime.utcnow(), #the current time
                                        my_metric.name, #the particualr metric in the metric_array loop
                                        'AWS/EC2', #specifies it is an EC2 instance
                                        'Average', #specifies the statistic I am looking for which is the average CPU Utilization
                                        dimensions={'InstanceId': instance.id} #specifies the instance ID is the user chosen instance ID
                                    )
            print my_metric.name, ': ', statistic #display the metric name and the statistic

    def less_than_40_alarm(self):
        instance_id = self.get_EC2_instance().id
        alarm_name = "CPU less than 40%"
        email_address = "example@test.com"
        metric_name = "CPUUtilization"
        comparison = "<"
        threshold = 40
        period = 300
        eval_periods = 1
        statistics = "Average"

        # Create a connection to the required services
        conn = Connection()
        sns = conn.SNS_connection()
        cw = conn.cloud_watch_connection()

        # Create the SNS Topic
        topic_name = 'Less_than_40_Percent'
        response = sns.create_topic(topic_name)
        topic_arn = response['TopicResponse']['TopicResult']['TopicArn']

        # Subscribe the email addresses to SNS Topic
        print 'Subscribing %s to Topic %s' % (email_address, topic_arn)
        sns.subscribe(topic_arn, "email", self.prompt_for_email())

        # Now find the Metric we want to be notified about
        metric = cw.list_metrics(dimensions={'InstanceId':instance_id}, metric_name=metric_name)[0]
        print 'Found: %s' % metric

        # Now create Alarm for the metric
        print 'Creating alarm'
        alarm = metric.create_alarm(name=alarm_name, comparison=comparison, threshold=threshold, period=period, evaluation_periods=eval_periods,
                                    statistic=statistics, alarm_actions=[topic_arn], ok_actions=[topic_arn])


    def prompt_for_email(self):
        return raw_input("Please Enter your Email Address: ") #ask the user for their email


    def connect_to_cw(self):
        conn0 = Connection()
        global global_connection
        global_connection = conn0.cloud_watch_connection()

    def get_EC2_instance(self):
        ec2inst = EC2Instance()
        return ec2inst.instance_chooser()

#test = CloudWatchInstance()
#test.enable_cw()
#test.easy_alarm()
