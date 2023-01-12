# Task Manager

Django project for IT companies for managing worker's tasks


# Check it out

...


## Installation

Python3 must be already installed

```shell
git clone https://github.com/YanPurdenko/task-manager
git checkout -b develop
python3 -m venv venv
sourse venv/bin/activate
pip install -r requirements.txt

Set another DB in settings.py like this:
DATABASES = {
     "default": {
         "ENGINE": "django.db.backends.sqlite3",
         "NAME": BASE_DIR / "db.sqlite3",
     }
 }

python manage.py migrate
python3 manage.py shell
from app.models import Position
positions = ["Developer", "Project manager", "Designer", "Devops", "QA"]
for position in positions:
  Position.objects.create(name=position)
python manage.py runserver

And finnaly sign up
```


## Features
- Authorization functionality for Workers/Users
- Change and reset password functionality
- Workers profile interface
- Updating profile functionality like changing avatar or edit some profile information
- Powerful admin panel for advanced managing
- And also create, update, delete, complete task functionality


## Demo

![Website Interface](demo.png)
