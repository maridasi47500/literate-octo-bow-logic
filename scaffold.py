# -*- coding: utf-8 -*-

import sys
import os
print(sys.argv[1])


filename=sys.argv[1].lower()
myclass=(filename).capitalize()
modelname=(filename).capitalize()
marouteget="\"/%s\"" % filename
maroutenew="\"/%s_new\"" % filename
maroutecreate="\"/%s_create\"" % filename
marouteget2="\\\"/%s\\\"" % filename
myhtml="my"+filename+"html"
myfavdirectory=filename
index = 2 
createtable=""
columns="("
formhtml="<form  enctype=\"multipart/form-data\" method=\"POST\">"
values="("
mysession="["
myparam=","
items=sys.argv
referencesstr=""
references=""

mylastrowid="""
"""
requestfiles="""
"""
sqltousles="""
"""
sqltousles2="""
"""
while index < (len(items)):

    try:
      print(index, items[index])
      hasfile=""
      referencesstr=""
      checkbox=""
      staff=""
      radiobutton=""
      paramname=items[index]
      if ":staff" in paramname: 
          staff="yes"
      if ":checkbox" in paramname: 
          checkbox="yes"
      if ":radio" in paramname: 
          radiobutton="yes"

      if ":file" in paramname: 
          hasfile="yes"
      if ":references" in paramname: 
          referencesstr="yes"
      paramname=items[index].replace(":staff","").replace(":datetime","").replace(":date","").replace(":time","").replace(":radio","").replace(":checkbox","").replace(":file","").replace(":references","")
      print(items[(index+1)])
    except:
      myparam=""
    index += 1
    myfieldtype="text"
    if radiobutton == "yes":
        myfieldtype="radio"
    if staff == "yes":
        myfieldtype="textarea"
    if checkbox == "yes":
        myfieldtype="checkbox"
    if staff == "yes":
        mylastrowid+="""
        file_pointer = open("./samplescoreexample.ly")
        contents = file_pointer.read()
        contents=contents.replace("KEYSCOREHERE", request.form["key_signature"].replace(" "," \\\\")).replace("TIMESCOREHERE", request.form["time_signature"]).replace("CONTENTSCOREHERE", request.form["{columnname}"])
        file_pointer = open("./static/scores/{tablename}_{columnname}_sample_"+mylastrowid+".ly", "w")
        file_pointer.write(contents)
        file_pointer.close()
        file_pointer = open("./static/scores/{tablename}_{columnname}_sample_"+mylastrowid+".html", "w")
        file_pointer.write("<lilypond staffsize=34>"+contents+"</lilypond>")
        file_pointer.close()
        subprocess.run(["lilypond-book", "static/scores/{tablename}_{columnname}_sample_"+mylastrowid+".html", "-f", "html", "--output", "static/scores/samplescore{tablename}_{columnname}"+mylastrowid]) 

        try:
            f= open("static/scores/samplescore{tablename}_{columnname}"+mylastrowid+"/{tablename}_{columnname}_sample_"+mylastrowid+".html")
            s = f.read()
            soup = BeautifulSoup(s)
""".format(tablename=filename,columnname=paramname)

        mylastrowid+="""
            picvalue=dict({'pic': "static/scores/samplescoremyscore_mymusic"+mylastrowid+"/"+soup.find('img').get("src"), 'id': mylastrowid})
        except:
            picvalue=dict({'pic': "", "id": mylastrowid})
        print(picvalue)
"""
        mylastrowid+="""
        hello_there = query_db("update {tablename} set pic = :pic where id = :id",picvalue, one=True)
""".format(tablename=filename,columnname=paramname)
    if hasfile == "yes":
      myfieldtype="file"
      requestfiles+="""
        uploaded_file = request.files['{paramname}']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join('static/photos', uploaded_file.filename))

        hey["{paramname}"]=uploaded_file.filename
""".format(paramname=paramname)
    if paramname == "password":
        myfieldtype = "password"
    if paramname == "email":
        myfieldtype = "email"
    if paramname == "telephone" or paramname == "phone":
        myfieldtype = "telephone"
        


    if referencesstr == "yes":
        references+=", tousles{paramname}=tousles{paramname}".format(paramname=paramname.replace("_id",""))
        sqltousles+="""
        tousles{paramname}= query_db("select * from {paramname}")
""".format(paramname=paramname.replace("_id",""))
        sqltousles2+="""
    tousles{paramname}= query_db("select * from {paramname}")
""".format(paramname=paramname.replace("_id",""))
        formhtml+="\n<div class=\"field\"><label for=\"somefield{paramname}\">{paramname}</label><select id=\"somefield{paramname}\" name=\"{paramname}\"><option value=\"novalue\">no value</option>".format(myparam=myparam,paramname=paramname,mytype=myfieldtype,tablename=filename)
        formhtml+="\n{% "+"for some{paramname} in tousles{paramname}".format(myparam=myparam,paramname=paramname.replace("_id",""),mytype=myfieldtype)+" %}"
        formhtml+="\n<option value=\"{{ some"+paramname.replace("_id","")+"['id'] }}\">{{ some"+paramname.replace("_id","")+"['name'] }}</option>{% endfor %}"
        formhtml+="\n</select></div>"

    elif radiobutton == "yes":
        formhtml+="\n<div class=\"field\"><label for=\"somefield{paramname}\">{paramname}</label><label for=\"somefield{paramname}1\"><input type=\"{mytype}\" id=\"somefield{paramname}1\" name=\"{paramname}\" value=\"1\"/>yes</label>\n<label for=\"somefield{paramname}2\"><input type=\"{mytype}\" id=\"somefield{paramname}2\" name=\"{paramname}\" value=\"0\"/>no</label></div>".format(myparam=myparam,paramname=paramname,mytype=myfieldtype)
    elif checkbox == "yes":
        formhtml+="\n<div class=\"field\"><input type=\"{mytype}\" id=\"somefield{paramname}\" name=\"{paramname}\" value=\"1\"/><label for=\"somefield{paramname}\">{paramname}</label></div>".format(myparam=myparam,paramname=paramname,mytype=myfieldtype)
    else:
        formhtml+="\n<div class=\"field\"><label for=\"somefield{tablename}{paramname}\">{paramname}</label><input type=\"{mytype}\" id=\"somefield{tablename}{paramname}\" name=\"{paramname}\"/></div>".format(myparam=myparam,paramname=paramname,mytype=myfieldtype,tablename=filename)


    mysession+="'{paramname}'{myparam}".format(myparam=myparam,paramname=paramname)
    columns+="{paramname}{myparam}".format(myparam=myparam,paramname=paramname)
    values+=":{paramname}{myparam}".format(myparam=myparam,paramname=paramname)
    createtable+="""        {paramname} text{myparam}
    """.format(myparam=myparam,paramname=paramname)
columns+=")"
values+=")"
mysession+="]"
mystr="""create table if not exists {filename}(
        id integer primary key autoincrement,
"""
mystr+=createtable
mystr+="  , created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP"


mystr+="""                );
"""
selectall= "select * from {filename}"

delete="""delete from {filename} where id = ?",(myid,)"""
selectone="""select * from {filename} where id = ?",(myid,)"""
addone="""@app.route("/add_one_{filename}", methods=["GET","POST"])
def add_one_{filename}():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)""".format(filename=filename, mysession=mysession,columns=columns,values=values,references=references)
addone+=requestfiles.format(filename=filename, mysession=mysession,columns=columns,values=values,references=references)
addone+=sqltousles.format(filename=filename, mysession=mysession,columns=columns,values=values,references=references)

addone+="""
        one_user = query_db("insert into {filename} {columns} values {values}",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from {filename}')
""".format(filename=filename, mysession=mysession,columns=columns,values=values,references=references)
addone+=mylastrowid
if filename == "user":
    addone+="""
        last_user = query_db("select * from {filename} where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        session["current_user_id"]=last_user["id"]
        for x in {mysession}:
            session[x]=hey[x]

""".format(filename=filename, mysession=mysession,columns=columns,values=values)
addone+="""
        return render_template("{filename}form.html", {filename}s=user, one_user=one_user, the_title="add new {filename}"{references})
""".format(filename=filename, mysession=mysession,columns=columns,values=values,references=references)
addone+=sqltousles2
addone+="""
    user = query_db('select * from {filename}')
    one_user = query_db("select * from {filename} limit 1", one=True)
    return render_template("{filename}form.html", {filename}s=user, one_user=one_user, the_title="add new {filename}"{references})

""".format(filename=filename, mysession=mysession,columns=columns,values=values,references=references)
if filename == "user":
    addone+="""
@app.route("/{filename}_sign_out", methods=["GET","POST"])
def {filename}_sign_out():
    if request.method == 'POST':
        session["current_user_id"]=""
        for x in {mysession}:
            session[x]=""
        return redirect("/")


@app.route("/{filename}_log_in", methods=["GET","POST"])
def {filename}_login():
    if request.method == 'POST':
        hey=request.form
        last_user = query_db("select * from {filename} where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        try:
            session["current_user_id"]=last_user["id"]
            for x in {mysession}:
                session[x]=hey[x]
        except:
            return render_template("{filename}login.html")
    return render_template("{filename}login.html")
""".format(filename=filename,mysession=mysession,columns=columns,values=values)
if "lat" in items and "lon" in items:

    lieu="""

@app.route("/searchjobcity", methods=["POST"])
def trouver_lieu_city():
    leslieu=Myplace(request.form["lieu"]).trouver1()

    return dict({"city":leslieu[0], "code":leslieu[1], "region":leslieu[3], "departement":leslieu[2], "pays":leslieu[2], "latitude":leslieu[4], "longitude":leslieu[5]})
"""
else:
    lieu=""

with open("app.py", "a") as myfile:
    #myfile.write(addone.format(filename=filename,columns=columns,values=values)+lieu)
    myfile.write(addone+lieu)
with open("schema.sql", "a") as myfile:
    myfile.write(mystr.format(filename=filename))
with open("templates/base.html", "a") as myfile:
    myfile.write("<a href=\"/add_one_{filename}\"> add one {filename}</a>".format(filename=filename))

if "lat" in items and "lon" in items:
    maphtmlcode="""
<div id="monadresse">
</div>
<div id="autresoffres">
</div>

     <div class="field">

                                         <label for="monlieu1">lieu</label>


         <input type="text" name="lieu" id="monlieu1" placeholder="nom du lieu"/>


                 </div>

                <button id="loadmycity" type="button">chercher l'adresse</button>

<div id="chercherunjob" style="display:none;">
la carte est bien là ou est l'offre d'emploi?
</div>

                                                        <input type="hidden" value="" id="maregion1" name="region" />
                                                        <input type="hidden" value="" id="monpays1" name="pays" />


        <input type="hidden" value="" id="moncode1" name="code" />


        <input type="hidden" value="" id="maville1" name="ville" />


        <input type="hidden" value="" id="monrayon1" name="rayon" />

                                                         <input type="hidden" onchange="" name="job" value="informatique" id="monjob1" placeholder="nom du job"/>

"""
    maphtmlcode+=("<div id=\"imap\"><div id=\"map\" style=\"height:200px;width:100%;\" onclick=\"onMapClick(event);\"><!-- Ici s'affichera la carte --></div>")
    othermapjs=("{% block jsmap %}"+"<script src=\"https://code.jquery.com/jquery-4.0.0.js\" integrity=\"sha256-9fsHeVnKBvqh3FB2HYu7g2xseAZ5MlN6Kz/qnkASV8U=\" crossorigin=\"anonymous\"></script><script src=\"/static/js/{filename}mymap.js\" type=\"text/javascript\"></script>".format(filename=filename)+"{% endblock %}")
else:
    maphtmlcode=""
    othermapjs=""

with open("templates/"+filename+"form.html", "w") as myfile:
    myfile.write("{% extends 'base.html' %}{% block content %}"+formhtml+"<div class=\"actions\"><input type=\"submit\"/></div></form>" + "{% for x in "+filename+"s %}{{"+ "x[\""+items[2].replace(":staff","").replace(":datetime","").replace(":date","").replace(":time","").replace(":radio","").replace(":checkbox","").replace(":file","").replace(":references","")+"\"] }}{% endfor %}"+maphtmlcode+"{% endblock %}{% block liens %}<a href=\"/\">bienvenue</a>"+"<a href=\"/add_one_{filename}\"> add one {filename}</a>".format(filename=filename)+"{% endblock %}"+othermapjs)



if filename == "user":
    with open("templates/"+filename+"login.html", "w") as myfile:
        myfile.write("{% extends 'base.html' %}{% block content %}<h1>signin</h1><form method=\"POST\"><div>\n<label>username</label><input name=\"username\"/><div>\n<label>username</label><input name=\"password\" type=\"password\"/></div><div class=\"actions\"><input type=\"submit\"/></div></form>" + "{% for x in "+filename+"s %}{{"+ "x[\""+items[2].replace(":staff","").replace(":datetime","").replace(":date","").replace(":time","").replace(":radio","").replace(":checkbox","").replace(":file","").replace(":references","")+"\"] }}{% endfor %}"+"{% endblock %}{% block liens %}<a href=\"/\">bienvenue</a>"+"<a href=\"/add_one_{filename}\"> s'inscrire (add one {filename})</a>".format(filename=filename)+"{% endblock %}")
if "lat" in items and "lon" in items:
 
    mymap=open("./awesomemap.js","r")
    f=mymap.read().replace("{tablename}", filename)
    with open("static/js/"+filename+"mymap.js", "w") as myfile:
        myfile.write(f)


