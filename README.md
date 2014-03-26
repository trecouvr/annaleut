annaleut
========

Archiver of exams

Requirements
------------

* python
* virtualenv (http://www.virtualenv.org/en/latest/)


Setup
-----


Clone the repo
""""""""""""""

  git clone git@github.com:trecouvr/annaleut.git
  cd annaleut


Virtualenv
""""""""""

To setup your development environment, run the following commands

  virtualenv env
  . env/bin/activate
  pip install -r requirements_dev.txt

More info on http://www.virtualenv.org/en/latest/


Local settings
""""""""""""""

Then create a `local_settings.py` file and put inside

  DATABASES['default']['USER'] = <database user>
  DATABASES['default']['PASSWORD'] = <database user>
  DATABASES['default']['HOST'] = <database host>
  DATABASES['default']['NAME'] = <database name>
  DATABASES['default']['ENGINE'] = <database engine> # optional if you want to use something else than MySQL

Be sure to replace the `<..>` placeholders by your values. Default values can be found in `annaleut/settings.py`.


Database
""""""""

To create all the tables, run the followings commands

  ./manage.py syncdb
  ./manage.py migrate

You should now be ready to run !

Run
---

To launch the development server, run these commands

  ./manage.py runserver

The server is now available on http://localhost:8000 :)

