#!/bin/bash
export GITHUBUSERNAME="maridasi47500"
mkdir -p "/home/$USER/$1/templates" 
mkdir -p "/home/$USER/$1/static/js"
mkdir -p "/home/$USER/$1/static/css"
mkdir -p "/home/$USER/$1/static/scores"
mkdir -p "/home/$USER/$1/static/photos"
touch "/home/$USER/$1/templates/base.html" 
touch "/home/$USER/$1/templates/hey.html" 
echo "&1 $1 $2 $3 $4 $5"
pwd
echo "git clone git@github.com:$GITHUBUSERNAME/$1.git"
$(cd ~ && git clone "git@github.com:$GITHUBUSERNAME/$1.git")
echo "__pycache__/\ndatabase.db" > "/home/$USER/$1/.gitignore" 
echo "`cat <<EOF
__pycache__/
database.db
static/photos/
static/scores/
EOF`" > "/home/$USER/$1/.gitignore" 



echo "====CREE COMMENCER.SH ====\n"
echo "`cat <<EOF
mkdir -p ~/path/to/venv
python3 -m venv ~/path/to/venv
source ~/path/to/venv/bin/activate
flask run
EOF`" > "/home/$USER/$1/commencer.sh" 
echo "====CHECK COMMENCER.SH ====\n"
echo "/home/$USER/$1/commencer.sh" 
cat "/home/$USER/$1/commencer.sh" 

echo "====CREE BASE HTML ====\n"
echo "`cat <<EOF
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">

	<title>{% block montitre %}{% endblock %}$2{{ the_title }}</title>

	<!-- note the special href for files in the Flask "static" folder -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB" crossorigin="anonymous">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
	<link rel="stylesheet" href="/static/css/main.css">

</head>
<body>

<div id="container">

  <!-- Jinja directives: page contents will go between them -->
  {% block liens %}
  {% endblock %}
  {% block content %}
  {% endblock %}

</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js" integrity="sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI" crossorigin="anonymous"></script>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
  {% block jsmap %}
  {% endblock %}

</body>
</html>
EOF`" > "/home/$USER/$1/templates/base.html" 
echo "====CHECK BASE  ====\n"
echo "/home/$USER/$1/templates/base.html" 
cat "/home/$USER/$1/templates/base.html" 


echo "====CREE HEY HTML ====\n"
echo "`cat <<EOF
{% extends 'base.html' %}

{% block montitre %}
$2
{% endblock %}
{% block content %}
<h1># $1</h1>
{% for x in users | reverse %}
 <li>{{ x["first_name"]  }}</li>

{% endfor %} 
$3
{% endblock %}
{% block liens %}
<a href="/">welcome</a>
{% endblock %}
EOF`" > "/home/$USER/$1/templates/hey.html" 
echo "====CHECK HEY  ====\n"
cat "/home/$USER/$1/templates/hey.html" 
echo "`cat <<EOF
body {
background:black;
color:white;
}
a, a:visited, a:hover, a:link {
color:white;
}
EOF`" > "/home/$USER/$1/static/css/main.css" 
echo "`cat <<EOF
import sqlite3
from flask import g

DATABASE = './database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def query_db(query, args=(), one=False):
    mydb = get_db()
    cur = mydb.execute(query, args)
    insert=""
    if "insert into" in query or ("update " in query and "set" in query):

        mydb.commit()
        insert="yes"

    rv = cur.fetchall()
    try:
        myid=cur.lastrowid
    except:
        myid=""
    cur.close()
    
    if insert == "yes":
        return {"myid": myid}
    else:
        return (rv[0] if rv else None) if one else rv







EOF`" > "/home/$USER/$1/yourappdb.py"
echo "`cat <<EOF
from flask import Flask, render_template, request, session, redirect
from myplace import Myplace
from bs4 import BeautifulSoup
import subprocess
import os
from yourappdb import query_db, get_db
from flask import g

app = Flask(__name__)
app.secret_key="any string"
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
init_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def hello_world():
    user = query_db('select * from contacts')
    the_username = "anonyme"
    one_user = query_db('select * from contacts where first_name = ?',
                [the_username], one=True)
    return render_template("hey.html", users=user, one_user=one_user, the_title="my title")
EOF`" > "/home/$USER/$1/app.py"
echo "`cat <<EOF
CREATE TABLE  IF NOT EXISTS contacts (
	contact_id INTEGER PRIMARY KEY,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	email TEXT NOT NULL UNIQUE,
	phone TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS groups (
   group_id INTEGER PRIMARY KEY,
   name TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS contact_groups(
   contact_id INTEGER,
   group_id INTEGER,
   PRIMARY KEY (contact_id, group_id),
   FOREIGN KEY (contact_id) 
      REFERENCES contacts (contact_id) 
         ON DELETE CASCADE 
         ON UPDATE NO ACTION,
   FOREIGN KEY (group_id) 
      REFERENCES groups (group_id) 
         ON DELETE CASCADE 
         ON UPDATE NO ACTION
);
INSERT OR IGNORE INTO contacts (contact_id, first_name, last_name, email, phone)
VALUES( '1', 'anonyme', 'noname', 'anonymous@email.fr', '+2653546434');
INSERT OR IGNORE INTO contacts (contact_id, first_name, last_name, email, phone)
VALUES( '2', 'anne onim', 'onim', 'anne.onim@email.com', '+86877779898');
EOF`" > "/home/$USER/$1/schema.sql"
pwd
cp ~/list-repo/samplescoreexample.ly "/home/$USER/$1"
cp ~/list-repo/awesomemap.js "/home/$USER/$1"
cp ~/list-repo/myplace.py "/home/$USER/$1"
cp ~/list-repo/fichier.py "/home/$USER/$1"
cp ~/list-repo/scaffold.py "/home/$USER/$1"
cp ~/list-repo/hellopython.sh "/home/$USER/$1"
cp ~/list-repo/demofile.sh "/home/$USER/$1"
#alias proj="(cd /home/$USER/$1 && pwd)"
#alias proj1="(cd /home/$USER/$1 && sh demofile.sh)"
#alias proj2="(cd /home/$USER/$1 && git add .)"
#alias proj3="(cd /home/$USER/$1 && git commit -am 'wow dljfghsfj')"
#alias proj4="(cd /home/$USER/$1 && git push origin main)"
#proj
#proj1
#proj2
#proj3
#proj4
(cd /home/$USER/$1 && pwd)
(cd /home/$USER/$1 && sh demofile.sh)
(cd /home/$USER/$1 && git add .)
(cd /home/$USER/$1 && git commit -am 'wow dljfghsfj')


(cd /home/$USER/$1 && rm awesomemap.js)
(cd /home/$USER/$1 && rm hellopython.sh)
(cd /home/$USER/$1 && rm demofile.sh)
(cd /home/$USER/$1 && git push origin main)
