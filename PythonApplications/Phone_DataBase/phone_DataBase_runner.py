"""
##########################
@author: Avi Zaguri
Application Name: Phone DataBase Creator
version: 1.0
##########################
"""

import threading

from PythonApplications.Phone_DataBase.frontend import PhoneDatabaseClass
from Infrastructure.Login.Login_Infrastructure import LogInApplicationClass
from Infrastructure.Logger_Infrastructure.Projects_Logger import ProjectsLogging


# username_guest_ = ['Administrator', 'gust']
# password_guest_ = ['Administrator', 'gust']
# server_ip_ = r'10.3.10.5:3268'
# domain_name_ = r'@airspan.com'

username_guest_ = ['Administrator', 'gust']
password_guest_ = ['Administrator', 'gust']

server_ip_ = input("Please enter server ip:")
server_port_ = input("Please enter server port:")
server_ip_ = f'{server_ip_}:{server_port_}'

domain_name_ = input("Please enter domain name:")

icon_path_ = r'data\EZLife.ico'
img_path_ = r'data\EZLife_open.png'

if __name__ == "__main__":
    print('Start Phone DataBase Creator script')

    logger = ProjectsLogging('PhoneDataBaseCreator').project_logging()
    logger.info('Start Phone DataBase Creator')

    try:
        access_flag = threading.Event()

        user_domain, password_domain, guest_mode, admin_mode = LogInApplicationClass().login_fronted(
            access_flag=access_flag, domain_name=domain_name_, server_ip=server_ip_, username_guest=username_guest_,
            password_guest=password_guest_, icon_path=icon_path_, img_path=img_path_)

        if access_flag.isSet():
            logger.info("0 = uncheck  \\\\  1 = check")
            logger.info("The guest mode is: " + str(guest_mode))
            logger.info("The admin mode is: " + str(admin_mode))
            PhoneDatabaseClass().phone_database_creator(user_domain, admin_mode)
            print()
        else:
            logger.info("Exit from the application")
            pass
    except Exception:
        logger.exception('')
