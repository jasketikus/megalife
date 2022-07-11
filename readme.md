## Megalife
Megalife is a small pet-project, which uses Python, Django framework and sqlite3 database.
It allows you to create web-site with:
* List of posts with pagination
* Model of categories
* Forms
  * Registraion and authorization;
  * Feedback form;
  * Form of adding post for registered users;
  * Proposed posts needs a publishing;
  * All forms have captcha. 
* Admin-panel where you can create and change categories 
and posts.
___
### Installation
1. Python Interpreter - __Python 3.10__
2. Virtualenv Environment - ___megalife\venv___
3. Install __requirements.txt__
4. Create ___.env___ file in main folder with secret data:
example
>SECRET_KEY=1234567890
> 
>DEBUG=True
> 
>ALLOWED_HOSTS=127.0.0.1
5. Run next operations in project terminal:
>cd pobalakaemo
> 
>python manage.py makemigrations
> 
>python manage.py migrate
> 
> python manage.py runserver
6. Create superuser 
>python manage.py createsuperuser
7. 127.0.0.1:8000/odmen to open adminpanel.