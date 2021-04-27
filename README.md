# EECE430Project
## Django Online Consultation Web Application 
## Steps to Run the Project 
**Step 1 - Database Preparation**
``` 
Download MySQL workbench based on the following steps https://m.youtube.com/watch?v=sCcncJNLbaw 
While installing you will be asked to provide a username and password for your MySQL local instance, make sure to remember them 
Create a new database by copying the code in the query.txt file uploaded to your MySQL workbench 
Execute the code in a SQL query 

``` 
**Step 2 - Django Environment Preparation (If you don't already have a django Virtual Environment)** 
``` 
The following steps are provided by Professor Ali Moukalled
Steps to install Django2.0.1 with Python3.6.4 on windows 64bits
C:\>pip3 install virtualenvwrapper-win
C:\>mkvirtualenv my_env		//you can replace my_env with any name

This will create an environment to run Django. You can run the following DOS commands on the environment:
1.	workon: lists available virtual environment , because you can run many mkvirtualenv
2.	workon env_name:  to activate specific environment
3.	deactivate: to exit the virtual environment
4.	rmvirtualenv env_name: to remove specific environment

C:\>workon my_env
(my_env) C:\>pip3 install django			//to install Django in the virtual env.
(my_env) C:\>django-admin startproject proj_name       //chose any name for your project
(my_env) C:\>cd proj_name
(my_env) C:\proj_name>dir				//check the folders and files in proj_name
…
(my_env)  C:\proj_name>python manage.py migrate	//setting up SQLite database

SETUP is done … let’s see if it works
(my_env) C:\proj_name>python manage.py runserver 0.0.0.0:8000 
Few lines will be displayed and a message showing you how to quit
Leave this DOS session running (minimize the screen if you like) and,
Open any browser and type the following URL: 
Your_computer_ip_address:8000
Example 127.0.0.1:8000
Or localhost:8000 (localhost instead of ip_address)
A welcome from django server will show.

``` 
**Step 3 - Running the project** 
``` 
Make sure you are working on my_env & correct path
First, Install the required python libraries as follows: 
pip install mysql-connector-python-rf 
pip install mysql-connector 
pip install mysql 
pip install mysqlclient 
- make sure to install all required packages (check the important libraries in views.py)
- make sure the password for the database is correct in views.py and in settings.py (according to the previously set password in installing MySQL workbench) 
```  
```
On the terminal/cmd run the following commands: 
python manage.py makemigrations 
python manage.py migrate 
python manage.py runserver 
``` 
The output of the last command should provide you with a link similar to the following:  http://127.0.0.1:8000/home (make sure to add /home to the link if it's not there)

Click on the link provided, it will direct you to the django application 

*Navigate through the web application and enjoy its features ツ* 


