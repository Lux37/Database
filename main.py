from flask import Flask, render_template,request,redirect,url_for,make_response
from models import User,db

app = Flask(__name__)
db.create_all()

@app.route("/")
def index():
    email = request.cookies.get("email")

    if email:
        #Get User from DB storage by email
        user = db.query(User).filter_by(email=email).first()
    else:
        user = None

    return render_template("index.html",user=user)

@app.route("/login",methods=["POST"])
def login():
    name = request.form.get("user-name")
    email = request.form.get("user-email")

    #Create new User
    user = User(name=name,email=email)

    #Save User to permanent DB storage
    db.add(user)
    db.commit()

    #Save User email to cookie
    response = make_response(redirect(url_for("index")))
    response.set_cookie("email",email)

    return response

if __name__ == '__main__':
    app.run()