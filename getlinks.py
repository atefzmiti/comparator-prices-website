from flask import Flask, render_template, request, redirect, url_for, request, flash
import mysql.connector
import os
import validators

app = Flask(__name__)

mydb1 = mysql.connector.connect(host="localhost", user="root", passwd="atefclubiste",
                                database="linkscrawled")
mydb2 = mysql.connector.connect(host="localhost", user="root", passwd="atefclubiste",
                                database="inscription")
mycursor1 = mydb1.cursor()
mycursor2 = mydb2.cursor()

app.secret_key = "hello"
pic_folder = os.path.join("static", "pics")
app.config["UPLOAD_FOLDER"] = pic_folder

@app.route('/contact')
def contact():
    pic1 = os.path.join(app.config["UPLOAD_FOLDER"], "search.png")
    return render_template("contacts.html", front_image=pic1)
@app.route('/')
def search():
    pic1 = os.path.join(app.config["UPLOAD_FOLDER"], "search.png")
    return render_template("frontpage.html", front_image=pic1)


@app.route('/', methods=["GET", "POST"])
def search_url():
    if request.method == "POST":
        text = request.form['search']
        n=0
        lengthtext = len(text.split(" "))
        def myf():
            n=0
            result3=[]
            while n<lengthtext:
                text3 = text.split(" ")[n]
                req = "select * from products_urls where product like '%-{}-%'".format(text3)
                mycursor1.execute(req)
                result1 = mycursor1.fetchall()
                for i in result1:
                    result3.append(i)
                n+=1
            return render_template("result.html", content=result3, r=len(result3), mot=text)
        if lengthtext>1:
            return myf()
        else:
            result3=[]
            text3 = text.split(" ")[n]
            req = "select * from products_urls where product like '%{}%'".format(text3)
            mycursor1.execute(req)
            result1 = mycursor1.fetchall()
            for i in result1:
                result3.append(i)
            return render_template("result.html", content=result3, r=len(result3), mot=text)
    else:
        return redirect(url_for("search"))




@app.route("/all",methods=["GET", "POST"])
def all_urlss():
    req = "select * from products_urls"
    mycursor1.execute(req)
    result1 = mycursor1.fetchall()
    return render_template("all_urls.html", content=result1, r=len(result1))


@app.route("/admin")
def admin():
    return render_template("sign.html")

@app.route('/admin', methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        login = request.form['login']
        password = request.form['mdp1']

        req1 = "SELECT login , password FROM compte WHERE login = '{login}' AND password = '{password}'".format(
            login=login, password=password)
        mycursor2.execute(req1)
        rows = mycursor2.fetchall()
        if len(rows) == 1:
            req = "select * from products_urls"
            mycursor1.execute(req)
            result1 = mycursor1.fetchall()
            return render_template("all_urls.html", content=result1, r=len(result1))
        else:
            flash("login ou mot de passe incorrect")
            return render_template("sign.html")


@app.route("/insert")
def insert():
    return render_template("insert.html")


@app.route("/insert", methods=["GET", "POST"])
def insert_link():
    # if request.method == "POST":
    link = request.form["link"]
    req1 = "insert into products_urls values('{n}')".format(n=link)
    valid_url = validators.url(link)
    if valid_url == True and ("mytek" or "tunisianet") in link:
        mycursor1.execute(req1)
        mydb1.commit()
        return redirect(url_for("all_urlss"))
    else:
        flash("enter a valid url")
        return render_template("insert.html")

@app.route("/delete")
def delete():
    return render_template("deletelink.html")

@app.route("/delete", methods=["GET", "POST"])

def delete_link():
    deletelink = request.form["deletelink"]
    req2 = "delete from products_urls where product = ('{m}')".format(m=deletelink)
    mycursor1.execute(req2)
    mydb1.commit()
    return redirect(url_for("all_urlss"))

if __name__ == '__main__':
    app.run(debug=True)
