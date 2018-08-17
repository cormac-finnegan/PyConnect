from Connection import Connection

class elb_instance():
    global global_connection
    def __init__(self):
        self.connect()
        self.zones = ['eu-west-1a']
        self.ports = [(80, 8080, 'http'), (443, 8443, 'tcp')]


    def list_all_load_balancers(self, verbose):
        load_balancers = global_connection.get_all_load_balancers()
        for elb in load_balancers:
            if verbose:
                print 'Load Balancer Name:', elb.name
        return load_balancers

    def elb_chooser(self, message): #function handles all uses for choosing an elb from the elb array, it returns a single bucket instance. The message argument is passed to allow custom messages
        print "********** [ Load Balancers ] **********"
        elb_array = self.list_all_load_balancers(False) #elb array obtained from (list_all_elb) function, 'False' argument used as this function will list the buckets with an index option
        if elb_array: #if array is not empty
            for elb in range(len(elb_array)): #for each elb instance spanning the range of the length of the elb array
                print '\t', str(elb), ' : ', elb_array[elb].name #print the index of the elb instance along with the elb_array[index] name
            print "\n"
            choice = raw_input(message) #the users choice is stored as a raw_input to limit it to be stored as a string
            if(choice != '*'): # [ * ] character is used if the user wants to cancel their solution
                try:
                    choice = int(choice) #the users choice will be attempted to be changed to an integer
                    return elb_array[choice] # return the chosen bucket from the array
                except (IndexError, ValueError): #If the users choice is not an integer
                    print "\n[ *****Please select a valid number***** ]\n"
                    return self.elb_chooser(message) #Recursive call
            else: #if the user cancels to proceed with their choice
                print "Cancelling . . ."
                pass
                return None #Returns the equivilent of 'null'


    def create_new_load_balancer(self):
        lb = global_connection.create_load_balancer(self.get_user_given_name(), self.zones, self.ports)
        return lb

    def delete_existing_load_balancer(self):
        chosen_elb = self.elb_chooser("Choose the index of the Load Balancer you want to delete")
        if chosen_elb:
            chosen_elb.delete()
        else:
            print "[ No active Load Balancers ]"


    def get_user_given_name(self):
        return raw_input("Type the name of your new load balancer: ")


    def connect(self):
        conn0 = Connection()
        global global_connection
        global_connection = conn0.elastic_load_balancing_connection()

