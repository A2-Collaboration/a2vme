#!/usr/bin/env python 

import socket, select, subprocess

def process(data):
    cmd = ""
    msg = ""
    array = data.split()
    
    if array[0] == "read":
        cmd = "vmeext "+array[1]+" 0 r"
        #msg = execute(cmd)
    elif array[0] == "write":
        if len(array) == 3:
            hx = hex(int(array[2]))
            cmd = "vmeext "+array[1]+" "+hx+" w"
            #msg = execute(cmd)
        else:
            msg = "No selection"
            cmd = msg*1 #for testing only
    else:
        msg = "Command not found"
    return cmd #should be msg
    
        
def execute(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    return output



if __name__ == "__main__":
      
    CONNECTION_LIST = []    # list of socket clients
    RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
    PORT = 8888
         
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this has no effect, why ?
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)
 
    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)
 
    print "Server started on port " + str(PORT)
 
    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
 
        for sock in read_sockets:
             
            #New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print "Client (%s, %s) connected" % addr
                 
            #Some incoming message from a client
            else:
                # Data recieved from client, process it
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        print "Received:" + data
                        
                        msg = process(data)
                        
                        print "Sent:"+msg
                        sock.send(msg)
                 
                # client disconnected, so remove from socket list
                except:
                    print "Client (%s, %s) disconnected" % addr
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
         
    server_socket.close()
    

