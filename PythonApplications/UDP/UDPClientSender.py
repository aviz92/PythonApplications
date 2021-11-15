"""
##########################
@author: Avi Zaguri
Application Name: UDP Server
version: 1.0
##########################
"""

import time
import socket
import datetime
import re

from Infrastructure.Network_Infrastructure.Socket_Infrastructure import SocketConnectionClass
from Infrastructure.Files_Infrastructure.Folders.Path_folders_Infrastructure import GeneralFolderActionClass

from Infrastructure.Logger_Infrastructure.Projects_Logger import ProjectsLogging


def write_to_file(data_string):
    date_and_time = datetime.datetime.now()
    date = datetime.datetime.now()

    date_and_time = str(date_and_time.strftime("%Y-%m-%d %H:%M:%S"))
    date_and_time = date_and_time.replace(':', '!')
    date = str(date.strftime("%Y-%m-%d"))

    path_folder = 'C:\\connections_to_internet\\' + date
    GeneralFolderActionClass().check_path_exist(path_folder)

    path_file = path_folder + "\\" + date_and_time + ".txt"
    with open(path_file, 'w') as file:
        file.write(data_string)
        file.close()


def analyze_data(data):
    try:
        regex_host_name = ''r"The hostname is: (\S+)"
        match_host_name = re.search(regex_host_name, data)
        if match_host_name:
            match_hostname = match_host_name.group(1)
            logger.info("The host name is: " + format(match_hostname))
        else:
            logger.info("regex_host_name - not match")
    except Exception:
        logger.exception('regex_host_name - not match')
        match_host_name = 'regex_host_name - not match'

    try:
        regex_ip_address = ''r"IPv4 Address. . . . . . . . . . . : (\S+)"
        match_ip_address = re.search(regex_ip_address, data)
        if match_ip_address:
            match_ip_address = match_ip_address.group(1)
            logger.info("The IP address is: " + format(match_ip_address))
        else:
            logger.info("regex_ip_address - not match")
    except Exception:
        logger.exception('regex_ip_address - not match')
        match_ip_address = 'regex_ip_address - not match'

    return match_host_name, match_ip_address


if __name__ == "__main__":
    print('Start UDPClientSender script')

    logger = ProjectsLogging('UDPClientSender').project_logging()
    logger.info('Start UDPClientSender script')

    # server_address = input("Please enter your server ip address: ")
    # server_port = input("Please enter your server port: ")
    server_address = '10.3.35.229'  # Server IP Address
    server_port = 10000

    socket_client = None
    cycle_ = 1

    while True:
        try:
            if socket_client:
                ''' Listen for incoming connections '''
                socket_client.listen(1)

                ''' Wait for a connection '''
                logger.info('waiting for a connection ' + str(cycle_) + ': ')
                connection, client_address = socket_client.accept()

                logger.info('connection from', client_address)

                ''' Receive the data in small chunks and retransmit it '''
                while True:
                    data_client = connection.recv(100000)

                    if data_client:
                        host_name, ip_address = analyze_data(data_client.decode('utf-8'))
                        write_to_file(data_client.decode('utf-8'))
                        connection.sendall(data_client)  # sending data back to the client

                    else:
                        logger.info('closing socket ' + str(cycle_) + ' ' + str(client_address))
                        break

                cycle_ += 1
            else:
                socket_client = SocketConnectionClass().socket_receiver_connection(server_address, server_port)
                continue
        except socket.error:
            logger.exception('')
            logger.debug('Trying to reconnect')
            time.sleep(10)
        except Exception:
            logger.exception('')
            time.sleep(10)
