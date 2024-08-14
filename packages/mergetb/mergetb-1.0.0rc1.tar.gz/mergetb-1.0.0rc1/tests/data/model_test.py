from mergexp import *

# Create a network topology object. This network will automatically
# add IP addresses to all node interfaces and configure static routes
# between all experiment nodes. 
net = Network('hello-world', addressing==ipv4, routing==static)

# Create three nodes.
a,b,c = [net.node(name) for name in ['a', 'b', 'c']]

# Create a link connecting the three nodes.
link = net.connect([a,b,c])

# Make this file a runnable experiment based on our three node topology.
experiment(net)