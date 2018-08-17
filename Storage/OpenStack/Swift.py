from Connection import Connection
from libcloud.storage.types import Provider
from libcloud.storage.providers import get_driver

class SwiftInstance:
    def __init__(self):
        get_driver(Provider.OPENSTACK_SWIFT)


    def list_all_containers(self, verbose):
        driver = self.connect()
        container_list = driver.list_containers()
        if verbose:
            for container in container_list:
                print '\t', container.name
        return container_list


    def container_chooser(self):
        container_array = self.list_all_containers(False)
        print "********** [ Instances ] **********"
        for containers in range(len(container_array)):
            containername = 'No Name'
            if container_array[containers].name:
                containername = container_array[containers].name
            print '\t', str(containers), ' : ', containername
        print "\n"
        choice = raw_input("Choose the Container:  [ * to cancel] ")
        if(choice != '*'):
            try:
                choice = int(choice)
                return container_array[choice]
            except (IndexError, ValueError):
                print "\n[ *****Please select a valid number***** ]\n"
                return self.container_chooser()
        else:
            print "Cancelling . . ."
            pass
            return None

    def list_objects_in_container(self):
        container = self.container_chooser()
        object_list = self.connect().list_container_objects(container)
        for objects in object_list:
            print objects.name

    def connect(self):
        conn0 = Connection()
        return conn0.open_stack_connection(True)

#test = SwiftInstance()
#test.list_objects_in_container()