#### Django Blog Template

This project is a template to easily build and deploy a personnal blog. It allows also to easily deploy it on the [Heroku](http://heroku.com) platform. 

### Installation

Clone This Project (Make Sure You Have Git Installed):
```
https://github.com/gaulthiergain/django_blog.git
```

Create (and install) a virtual environment:
```
pip install pipenv
pipenv shell
```

Install Dependencies:
```
pip install -r requirements.txt
```

Set Database (Make Sure you are in directory same as manage.py):
```
python manage.py makemigrations
python manage.py migrate
```

Create SuperUser:
```
python manage.py createsuperuser
```

Run server and go to (http://localhost:8000):
```
python manage.py runserver
```

### Deployment

Go to [Heroku](http://heroku.com) and create an account.

Install the [Heroku command lines](https://devcenter.heroku.com/categories/command-line).

After that, write the following commands:

```
heroku login
git push heroku master
heroku run python manage.py makemigrations
heroku run python manage.py migrate
heroku ps:scale web=1
heroku logs --tail
```
