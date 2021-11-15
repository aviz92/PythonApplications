"""
##########################
@author: Avi Zaguri
Application Name: UDP Client
version: 1.0
##########################
"""

import time
import socket
import subprocess

from Infrastructure.Network_Infrastructure.Socket_Infrastructure import SocketConnectionClass
from Infrastructure.Logger_Infrastructure.Projects_Logger import ProjectsLogging


def send_details(cycle):
    try:
        socket_client = SocketConnectionClass().socket_sender_connection(server_address, server_port)
        if socket_client:
            host_name = str(socket.gethostname())
            # host_name = HostName.encode('utf-8')

            ipconfig = subprocess.check_output("ipconfig").decode('utf-8')
            # ipconfig = ipconfig.encode('utf-8')

            message = "The hostname is: " + host_name + "\n" + ipconfig
            logger.info('Message ' + str(cycle) + ' is: \n' + str(message))

            socket_client.sendall(message.encode('utf-8'))

            ''' Look for the response '''
            amount_received = 0
            amount_expected = len(message)
            logger.info('Message ' + str(cycle) + ' was sent')

            while amount_received < amount_expected:
                data = socket_client.recv(100000)
                amount_received += len(data)
                logger.info('Get received message expected')
            return cycle
        else:
            return cycle-1
    except socket.error:
        logger.exception('')
        logger.info('Trying to reconnect')
        return
    except Exception:
        logger.exception('')
        logger.info('Trying to reconnect')
        return


if __name__ == "__main__":
    print('Start UDPClientReceive script')

    logger = ProjectsLogging('UDPClientReceive').project_logging()
    logger.info('Start UDPClientReceive script')

    # server_address = input("Please enter your server ip address: ")
    # server_port = input("Please enter your server port: ")
    server_address = '10.3.35.229'  # Server IP Address
    server_port = 10000

    cycle_ = 1
    while True:
        send_details(cycle_)
        time.sleep(2)
        cycle_ += 1
