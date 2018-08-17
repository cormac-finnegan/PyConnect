import Tkinter
import tkFileDialog
from boto.s3.key import Key
import re

from Connection import Connection


class S3Instance:

    global global_connection #a global connection is used so it can be used without having to call the connect method everytime

    def __init__(self):
        self.connect() #init calls the connection method which sets the global_connection

    def list_all_buckets(self, verbose): #this method returns a list of all buckets as an array, but can also be used to list the individual buckets with the Verbosity boolean
        bucket_list = global_connection.get_all_buckets() #uses the global connection to get all the buckets
        if bucket_list: #if the bucket list has buckets
            if (verbose == True): #if verbosity is enabled
                for bucket in bucket_list: #for each bucket in the bucket list array
                    print bucket #print the bucket
        else: #otherwise
            print "\t[ No current Buckets ]" #tell user there are no available buckets
        return bucket_list  #this method always returns the bucket list, thus allowing me to reuse it in other methods,
                            #the verbosity variable is so I have the option to list the buckets in a different way

    def bucket_chooser(self, message): #function handles all uses for choosing a bucket from the bucket array, it returns a single bucket instance. The message argument is passed to allow custom messages
        print "********** [ BUCKETS ] **********"
        bucket_array = self.list_all_buckets(False) #bucket array obtained from list_all_bucket function, 'False' argument used as this function will list the buckets with an index option
        if bucket_array: #if array is not empty
            for buckets in range(len(bucket_array)): #for each bucket spanning the range of the length of the bucket array
                print '\t', str(buckets), ' : ', bucket_array[buckets].name #print the index of the bucket along with the bucket_array[index] name
            print "\n"
            choice = raw_input(message) #the users choice is stored as a raw_input to limit it to be stored as a string
            if(choice != '*'): # [ * ] character is used if the user wants to cancel their solution
                try:
                    choice = int(choice) #the users choice will be attempted to be changed to an integer
                    return bucket_array[choice] # return the chosen bucket from the array
                except (IndexError, ValueError): #If the users choice is not an integer
                    print "\n[ *****Please select a valid number***** ]\n"
                    return self.bucket_chooser(message) #Recursive call
            else: #if the user cancels to proceed with their choice
                print "Cancelling . . ."
                pass
                return None #Returns the equivilent of 'null'


    '''Almost Identical functionality to the bucket chooser, but used for objects from chosen bucket, cannot be called without a bucket argument'''
    def object_chooser(self, message, bucket):
        print "********** [ Files ] **********"
        object_array = [] #creates an empty array to store the objects
        if bucket: #if not empty
            for b in bucket.list(): #for each bucket in the list
                object_array.append(b) #append it to the array (this in necessary as the bucket.list() only returns a list object which throws a spanner into the works for the rest of the code)
        if object_array:
            for buckets in range(len(object_array)):
                print '\t', str(buckets), ' : ', object_array[buckets].name
            print "\n"
            choice = raw_input(message)
            if(choice != '*'):
                try:
                    choice = int(choice)
                    return object_array[choice]
                except (IndexError, ValueError):
                    print "\n[ *****Please select a valid number***** ]\n"
                    return self.bucket_chooser(message)
            else:
                print "Cancelling . . ."
                pass
                return None


    def list_all_objects_in_bucket(self):
        user_choice = self.bucket_chooser("Choose the Bucket you want to see contents of:  [ * to cancel] ") #call the function to choose a bucket with custom message
        if user_choice: #If the user choice is not null
            bucket_choice = global_connection.get_bucket(user_choice) #get the users chosen bucket from the boto connection
            for key in bucket_choice: #for every object in the chosen bucket
                print ' - ', key.name #print the object's name



    def upload_to_a_bucket(self):
        bucket = self.bucket_chooser("Choose the Bucket you want to upload to:  [ * to cancel] ")
        if bucket:
            contents = self.create_file_choosing_window() #Calls function to create a file choosing window (should work cross platform), stores the full filepath as string in contents
            file_name = re.search('([^\/\/]+)$', contents) #A regular expression is used to parse the filename from the full path (C:/foo/bar/image.jpg -> image.jpg)
            file_name = file_name.group(0) #gets the string from the regex group
            if contents: #if contents is not null
                k = Key(bucket) #store the key of the bucket in k
                k.key = file_name #create a new key in k(the bucket) with the filename derived from the regex
                k.set_contents_from_filename(contents) #tell the new key to set its contents to be retrieved from the filepath given for the local machine

    def download_from_bucket(self):
        bucket = self.bucket_chooser("Choose the Bucket you want to download from:  [ * to cancel] ") #call the bucket choosing method to obtain the user's chosen bucket
        key = self.object_chooser("Choose the Object you want to download:  [ * to cancel] ", bucket) #call the object choosing method to obtain the user's chosen file and pass the chosen bucket as an argument
        if key: #if the key is not null
            LOCAL_PATH = str(self.create_dir_choosing_window()) #set the local path to be derived from the returned string value from the directory choosing window
            if LOCAL_PATH:
                key.get_contents_to_filename(LOCAL_PATH +'/'+ key.name)

    def delete_object_from_bucket(self):
        bucket = self.bucket_chooser("Choose the Bucket you want to delete from: [ * to cancel]")
        key = self.object_chooser("Choose the Object you want to delete:  [ * to cancel] ", bucket)
        bucket.delete_key(key)


    '''Uses Tkinter, which is a GUI layer from Python's standard library to easily allow the user to choose a file and returns it's full path'''
    def create_file_choosing_window(self):
        Tkinter.Tk().withdraw() # Closes a root window that is created when the file choosing window is created
        in_path = tkFileDialog.askopenfilename() # from the file dialog window, call the function which allows the user to specify the file they want to upload
        return in_path #returns the full file path

    def create_dir_choosing_window(self):
        Tkinter.Tk().withdraw() # Closes a root window that is created when the file choosing window is created
        in_path = tkFileDialog.askdirectory() # from the file dialog window, call the function which allows the user to specify the directory they want to download the file into
        return in_path #returns the directory chosen

    def connect(self):
        conn0 = Connection() #Create a connection instance
        global global_connection
        global_connection = conn0.S3_connection() #set the global connection variable as the returned S3 connection


