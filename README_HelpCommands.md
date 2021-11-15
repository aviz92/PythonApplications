# Help Commands

------------------------------------------------------------------------------------------------------------------------

General:
========

Create requirements.txt:
----------------------------
- pip freeze > requirements.txt


Install requirements.txt:
----------------------------
- pip install -r requirements.txt


Uninstall requirements.txt:
----------------------------
- pip uninstall -r requirements.txt -y


Upgrade pip:
------------
- pip install pip --upgrade


Create wheel:
-------------
install .whl:
- pip install wheel

create .whl: 
- python setup.py sdist bdist_wheel (the file will be under dist - 2 file)

load .whl: 
- pip install http:path_to_file_name/wheel_file_name.whl

remove .whl:
- pip uninstall Automation_Infrastructure


------------------------------------------------------------------------------------------------------------------------

Django:
=======

Run Server:
-----------
from console:
- python manage.py runserver

from pycharm (edit configuration):
- runserver ip_address:port
- runserver host_name:port


Create super user:
------------------
- python manage.py createsuperuser --email user@example.com --username user


Create makemigrations:
----------------------
- python manage.py makemigrations
- python manage.py migrate


Create project:
---------------
- django-admin startproject my_project_name


Create application:
-------------------
- django-admin startapp my_app_name


Schema:
-------
Schema configurations:
- INSTALLED_APPS = (
    ...
    'django_extensions',
    ...
)

Create Schema:
- python manage.py graph_models -a -o Myapp_Models.png
- python manage.py graph_models -a -o Project_Schema.png


------------------------------------------------------------------------------------------------------------------------

LDAP:
=====

How to install LDAP:
--------------------
- install openldap-2.4.54
- pip install django-auth-ldap
- pip install python_ldap-3.3.1-cp38-cp38-win_amd64.whl


LDAP from terminal:
-----------------
ldapobj = ldap.initialize("ldap://IPAddress:PORT")
ldapobj.simple_bind_s(user, password)

ldapobj.search_s("OU=Israel,OU=UsersName,DC=DCName,DC=com", ldap.SCOPE_SUBTREE, "(objectClass=user)")


------------------------------------------------------------------------------------------------------------------------
