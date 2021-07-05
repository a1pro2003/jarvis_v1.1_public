#!/usr/bin/env python3

""" Import Python library """
import sys
import platform
import ipaddress
import asyncio

# Global variable
my_list_of_tasks = []
my_tasks = []
nbr_host_found = 0
list_of_hosts_found = []

# The coroutine. That function is called using asyncio
async def ping_coroutine(cmd, ip):
    """ Async procedure
    ping_coroutine is the coroutine used to send a ping
    """


    global nbr_host_found, list_of_hosts_found

    running_coroutine = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    # Suspends the current coroutine allowing other tasks to run
    stdout = await running_coroutine.communicate()

    # Ping OK?
    if "ttl=" in str(stdout).lower():
        # Ping OK

        # 1 host found
        nbr_host_found += 1
        # IP address added to the list of hosts found
        list_of_hosts_found.append(ip)

async def ping_loop():
    """ Async procedure
    ping_loop run the list of coroutines, list by list
    """

    global my_tasks, my_list_of_tasks


    for each_task_list in my_list_of_tasks:
        # Start the coroutines one by one from the current list
        for each_coroutine in asyncio.as_completed(each_task_list):
            await each_coroutine


# networkscan class
class Networkscan:

    """Class Networkscan"""

    def __init__(self, ip_and_prefix):
        """Class init"""


        self.nbr_host_found = 0
        self.list_of_hosts_found = []

        # Default value for the filename
        self.filename = "hosts.yaml"

            # Correct input data?
        try:

            # Use ipaddress library
            self.network = ipaddress.ip_network(ip_and_prefix)

        except:

            # Problem with input data

            # Display error message and exit
            sys.exit("Incorrect network/prefix " + ip_and_prefix)

        # Calculate the number of hosts
        self.nbr_host = self.network.num_addresses

        # Network and mask address to remove? (no need if /31)
        if self.network.num_addresses > 2:
            self.nbr_host -= 2

        # Define the ping command used for one ping (Windows and Linux versions are different)
        self.one_ping_param = "ping -n 1 -l 1 -w 1000 " if platform.system().lower() == "windows" else "ping -c 1 -s 1 -w 1 "

    def write_file(self, file_type=0, filename="hosts.yaml"):
        """ Method to write a file with the list of the detected hosts """

        ret = 0

        # Check if a filename is really given (protection against incorrect name use)
        if (str(filename) == "None") or (str(filename) == ""):
            # No name given
            # Then the default name will be given
            filename = "hosts.yaml"

        # Save the name of the file
        self.filename = filename

        # Nornir file?
        if file_type == 0:
            # Yes Nornir file

            # Convert hosts and yang format into a string
            data = "---\n"
            device_number = 0
            for i in self.list_of_hosts_found:
                # The number used in the host name is increased ("device1", "device2", etc.)
                device_number += 1
                data += "device" + str(device_number) + ":\n    hostname: " \
                    + i + "\n    groups:\n        - device_discovered\n\n"

            try:
                # Write data into a file
                with open(filename, "w") as f:
                    f.write(data)

            except Exception:

                # Error while writting the file
                ret = 1

        # Text file?
        elif file_type == 1:
            # Yes, text file

            # Convert hosts into a single string
            data = ""
            for i in self.list_of_hosts_found:
                data += i + "\n"

            try:
                # Write data into a file
                with open(filename, "w") as f:
                    f.write(data)

            except Exception:

                # Error while writting the file
                ret = 1

        return ret

    def run(self):


        global my_tasks, nbr_host_found, list_of_hosts_found, my_list_of_tasks

        self.nbr_host_found = 0
        self.list_of_hosts_found = []
        my_tasks = []
        nbr_host_found = 0
        list_of_hosts_found = []


        i = 128

        my_list_of_tasks = []

        my_list_of_tasks.append(my_tasks)

        # Check if /32 is not used
        if self.network.num_addresses != 1:

            # /32 not used (so there are more than 2 IP adresses)

            # Create the coroutines tasks
            for host in self.network.hosts():

                # cmd has the command line used by the ping command including the ip address
                # example: cmd = "ping -n 1 -l 1 -w 1000 192.168.0.1"
                cmd = self.one_ping_param + str(host)

                # my_tasks is a list with coroutine tasks. It gets 2 parameters: one with
                #  the ping command and the other one with the ip address of the target
                my_tasks.append(ping_coroutine(cmd, str(host)))

                # Decrease the counter of ping commands inside the list
                i -= 1

                # 128 ping in the current list?
                if i <= 0:
                    # Yes
                    i = 128

                    # Clear the current list
                    my_tasks = []
                    # Add a new empty list to the list of list my_list_of_tasks
                    my_list_of_tasks.append(my_tasks)
        else:

            # Yes, just one 1 IP address is used
            # Without the followning code "self.network.hosts()" will not provide
            # the IP address and no ping would be possible for /32 IP addresses

            # Get the IP address; that is ne network IP address actually
            host = str(self.network.network_address)

            # cmd has the command line used by the ping command including the ip address
            # example: cmd = "ping -n 1 -l 1 -w 1000 192.168.0.1"
            cmd = self.one_ping_param + host

            # my_tasks is a list with coroutine tasks. It gets 2 parameters: one with the ping
            #  command and the other one with the ip address of the target
            my_tasks.append(ping_coroutine(cmd, host))

        #print(str(len(my_list_of_tasks)))

        # if Windows is in use then these commands are needed otherwise
        # "asyncio.create_subprocess_shell" will fail
        if platform.system().lower() == "windows":
            asyncio.set_event_loop_policy(
                asyncio.WindowsProactorEventLoopPolicy())

        # Run the coroutine loop
        asyncio.run(ping_loop())

        # Save list of hosts found and number of hosts
        self.list_of_hosts_found = list_of_hosts_found
        self.nbr_host_found = nbr_host_found

def print_program_parameters_and_usage():
    """ Just display the parameters of the program """

    print("\nUsage: networkscan.py network_to_scan [-h] [-q] [-m] [-w [hosts.yaml]] \
    \n\nOptions : \
    \n    network_to_scan      The network or IP address to scan using fast pings. \
    \n                         Examples: \"192.168.0.0/24\", \"10.0.0.1\", \"172.16.1.128/28\", etc. \
    \n    -h                   Help \
    \n    -m                   Mute mode (nothing is displayed on screen) \
    \n    -q                   Quiet mode (just the list of hosts found is displayed) \
    \n    -w [hosts.yaml]      Write a yaml host file with an optional filename (default name is hosts.yaml)\n \
    ")

# Main function
def main(ip):

    # By default normal mode for displaying information
    #
    # - mode (integer, optional): 0, mute (nothing written on screen during scanning hosts)
    #                             1, quiet (just the list of hosts found is displayed)
    #                             2, normal (write found hosts on screen during scanning hosts)
    #
    mode = 2

    # By default no file to save with the result of the scan
    #
    # - file_to_save (integer, optional): 0, no file to save
    #                                     1, write a file with the ping result
    # - filename_to_save (string, optional): the name of the file with the result of the ping
    #   (default "None" means "hosts.yaml" will be used)
    #
    file_to_save = 0
    filename_to_save = None

    # This variable is used to check if "-w" parameter is used
    after_w = 0

    # Check parameters
 
    # First parameter is the network to scan (always)
    my_network = ip

    # Create the object
    my_scan = Networkscan(my_network)


    my_scan.run()


    # Display additional information? (mode normal and quiet)
    if mode != 0:
        #return my_scan.list_of_hosts_found
        with open('ip.txt', 'w') as f:
        # Display the IP address of all the hosts found
            for i in my_scan.list_of_hosts_found:
                #f.write(i + '\n')
                print(i)

    # Display additional information? (mode normal)
    if mode == 2:
        # Yes

        # Display information
        print("Number of hosts found: " + str(my_scan.nbr_host_found))

    # Write a file with the list of the hosts?
    if file_to_save:
        # Yes

        # Display additional information? (mode normal)
        if mode == 2:
            # Yes

            print("Writting file")

        # Write the file on disk
        res = my_scan.write_file(0, filename_to_save)

        # Display additional information? (mode normal)
        if mode == 2:
            # Yes

            # Error while writting the file?
            if res:
                # Yes
                print("Write error with file " + my_scan.filename)

            else:
                # No error
                print("Data saved into file " + my_scan.filename)


main(input("Ip: "))