from Connection import Connection
from libcloud.compute.types import NodeState

class list_running:
    def list_nodes(self):
        driver = self.connect() #get the Nova driver from the connection class
        nodes = driver.list_nodes() #list all nodes runinng
        for node in nodes: #for every node
            print 'Node Name: ', node.name, 'Node ID: ', node.id, 'Node State: ', NodeState.tostring(node.state)


    def connect(self):
        conn0 = Connection()
        return conn0.open_stack_connection(False) #returns the driver obtained from the connection class (False signifies that I am looking for the Compute driver to be returned)
