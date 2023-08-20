# finder

**Pre-requisites**

*  pip version 22.3.1
* Python 3.9.6
* npm 9.5.1
* node v18.16.0
  
**Steps to run the server**

* Create a google app from console and get client creds for google apps
* update google creds in `settings.py` like >GOOGLE_OAUTH2_CLIENT_ID, GOOGLE_OAUTH2_CLIENT_SECRET, GOOGLE_OAUTH2_REDIRECT_URI etc.
* make virtual env using `virtualenv finder-personal`
* `source finder-personal/bin/activate`
* now run `pip install -r requirements.txt` in your root of project folder
* `cd frontend`
* `npm i`
* `npm run dev`
* In new terminal run `python manage.py makemigrations`
* `python manage.py migrate`
* `python manage.py runserver`
* Now open your browser and hit `https://localhost:8000`

[Complete Doc can be found here for understanding architecture and stuff.](https://autumn-stitch-a8c.notion.site/Finder-app-51bf09bd59a241528a679e4bf091e6ca)
