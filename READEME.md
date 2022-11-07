Project
Create a virtual environment to install dependencies in and activate it:

$ pip install virtualenv
$ virtualenv venv
$ venv/bin/activate or venv\\Scripts\\activate 
Then install the dependencies:

(venv)$ pip install -r requirements.txt
Note the (venv) in front of the prompt. This indicates that this terminal session operates in a virtual environment.

Once pip has finished downloading the dependencies:

(venv)$ cd project_name
(venv)$ uvicorn main:app --reload
