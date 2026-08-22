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
@app.route("/add_one_piece", methods=["GET","POST"])
def add_one_piece():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into piece (name,composer_artist,time_signature,key_signature) values (:name,:composer_artist,:time_signature,:key_signature)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from piece')


        return render_template("pieceform.html", pieces=user, one_user=one_user, the_title="add new piece")


    user = query_db('select * from piece')
    one_user = query_db("select * from piece limit 1", one=True)
    return render_template("pieceform.html", pieces=user, one_user=one_user, the_title="add new piece")

@app.route("/add_one_bow_logic", methods=["GET","POST"])
def add_one_bow_logic():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into bow_logic (position_de_depart,longueur_archet,duree_de_note,pic,time_signature,key_signature,tempo,vitesse_archet,nuances,corde,distance_chevalet,position_manche,description) values (:position_de_depart,:longueur_archet,:duree_de_note,:pic,:time_signature,:key_signature,:tempo,:vitesse_archet,:nuances,:corde,:distance_chevalet,:position_manche,:description)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from bow_logic')


        file_pointer = open("./samplescoreexample.ly")
        contents = file_pointer.read()
        contents=contents.replace("KEYSCOREHERE", request.form["key_signature"].replace(" "," \\")).replace("TIMESCOREHERE", request.form["time_signature"]).replace("CONTENTSCOREHERE", request.form["duree_de_note"])
        file_pointer = open("./static/scores/bow_logic_duree_de_note_sample_"+mylastrowid+".ly", "w")
        file_pointer.write(contents)
        file_pointer.close()
        file_pointer = open("./static/scores/bow_logic_duree_de_note_sample_"+mylastrowid+".html", "w")
        file_pointer.write("<lilypond staffsize=34>"+contents+"</lilypond>")
        file_pointer.close()
        subprocess.run(["lilypond-book", "static/scores/bow_logic_duree_de_note_sample_"+mylastrowid+".html", "-f", "html", "--output", "static/scores/samplescorebow_logic_duree_de_note"+mylastrowid]) 

        try:
            f= open("static/scores/samplescorebow_logic_duree_de_note"+mylastrowid+"/bow_logic_duree_de_note_sample_"+mylastrowid+".html")
            s = f.read()
            soup = BeautifulSoup(s)

            picvalue=dict({'pic': "static/scores/samplescoremyscore_mymusic"+mylastrowid+"/"+soup.find('img').get("src"), 'id': mylastrowid})
        except:
            picvalue=dict({'pic': "", "id": mylastrowid})
        print(picvalue)

        hello_there = query_db("update bow_logic set pic = :pic where id = :id",picvalue, one=True)

        return render_template("bow_logicform.html", bow_logics=user, one_user=one_user, the_title="add new bow_logic")


    user = query_db('select * from bow_logic')
    one_user = query_db("select * from bow_logic limit 1", one=True)
    return render_template("bow_logicform.html", bow_logics=user, one_user=one_user, the_title="add new bow_logic")

