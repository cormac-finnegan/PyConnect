from boto import config

from Connection import Connection


class EC2Instance:
    global global_connection
    def __init__(self):
        self.ami_array = ['ami-31328842', 'ami-8b8c57f8', 'ami-f4278487', 'ami-f4278487', 'ami-f95ef58a', 'ami-c6972fb5'] #array which holds the ami names  corresponding to the ami_string _array
        self.ami_string_array = ['Amazon Linux AMI', 'Red Hat Enterprise', 'SUSE Linux Enterprise Server', 'Ubuntu Server', 'Microsoft Windows Server'] #Names corresponding to the ami strings
        self.connect() #set the global_connection here


    def list_instances(self, verbose):
        instances = self.get_all_instances()
        for i in instances:
            tags = i.tags
            instancename = 'No Name'
            if 'Name' in tags:
                instancename = tags['Name']
            if verbose:
                print 'Instance Name:', instancename, '\tInstance Id:', i.id, '\tAMI ID:', i.image_id, '\tState:', i.state, '\tLaunch Time:', i.launch_time, '\tInstance Type:', i.instance_type
        return instances

    def instance_chooser(self):
        instance_array = self.list_instances(False)
        print "********** [ Running AWS EC2 instances ] **********"
        for instances in range(len(instance_array)):
            instancename = 'No Name'
            if 'Name' in instance_array[instances].tags:
                instancename = instance_array[instances].tags['Name']
            print '\t', str(instances), ' : ', instancename, ' Instance Id:', instance_array[instances].id, ' State:', instance_array[instances].state
        print "\n"
        choice = raw_input("Choose the Instance:  [ * to cancel] ")
        if(choice != '*'):
            try:
                choice = int(choice)
                return instance_array[choice]
            except (IndexError, ValueError):
                print "\n[ *****Please select a valid number***** ]\n"
                return self.instance_chooser()
        else:
            print "Cancelling . . ."
            pass
            return None


    def list_EBS_volumes(self, verbose):
        volumes = global_connection.get_all_volumes()
        for v in volumes:
            if verbose:
                print 'Volume Name:', v.id, '\tState:', v.attachment_state
        return volumes

    def volume_chooser(self):
        volume_array = self.list_EBS_volumes(False)
        print "********** [ Volumes ] **********"
        for volumes in range(len(volume_array)):
            print '\t', str(volumes), ' : ',' Volume Id:', volume_array[volumes].id, ' State:', volume_array[volumes].status
        print "\n"
        choice = raw_input("Choose the Volume:  [ * to cancel] ")
        if(choice != '*'):
            try:
                choice = int(choice)
                return volume_array[choice]
            except (IndexError, ValueError):
                print "\n[ *****Please select a valid number***** ]\n"
                return self.instance_chooser()
        else:
            print "Cancelling . . ."
            pass
            return None


    def ami_chooser(self):
        array_names = self.ami_string_array
        ami_array = self.ami_array
        for i in range(len(array_names)):
            print ': ', str(i),' :', array_names[i]
        array_choice = raw_input("Please select the index of the instance you would like to create [ * to cancel]")
        if(array_choice != "*"):
            try:
                choice = int(array_choice)
                return ami_array[choice]
            except (IndexError, ValueError):
                print "\n[ *****Please select a valid number***** ]\n"
                return self.ami_chooser()
        else:
                print "Cancelling . . ."
                pass
                return None

    def attach_existing_volume(self):
        attach_state = global_connection.attach_volume (self.volume_chooser().id, self.instance_chooser().id, "/dev/sdf")
        print 'Attach Volume Result: ', attach_state

    def detach_volume(self):
        global_connection.detach_volume (self.volume_chooser().id, self.instance_chooser().id, "/dev/sdf")


    def get_instance_info(self):
        user_choice = self.instance_chooser()
        info = user_choice.__dict__
        for tags in info:
            print tags, ' : ', info[tags]

    def stop_instance(self):
        user_choice = self.instance_chooser()
        global_connection.stop_instances(user_choice.id)

    def start_stopped_instance(self):
        user_choice = self.instance_chooser()
        if(user_choice.state == "stopped"):
            global_connection.start_instances(user_choice.id)
        if(user_choice.state == "running"):
            print "Instance is already running"

    def stop_all(self):
        inst = self.get_all_instances()
        for i in inst:
            if i.state == 'running':
                i.stop()

    def start_new_instance(self):
        ami_choice = self.ami_chooser()
        global_connection.run_instances(ami_choice, key_name=config.get('CREDENTIALS', 'key_name'), instance_type="t2.micro")

    def get_all_reservations(self):
        return global_connection.get_all_reservations()

    def get_all_instances(self):
        reservations = self.get_all_reservations()
        instances = []
        for r in reservations:
            instance = r.instances
            for i in instance:
                instances.append(i)
        return instances



    def connect(self):
        conn0 = Connection()
        global global_connection
        global_connection = conn0.ec2Connection()
        return global_connection
