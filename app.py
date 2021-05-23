#import which are required in this project
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

#initialzing the sql server credentials
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="username",
    password="password",
    hostname="host name",
    databasename="databasename",
)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


#initialzing the dictonary for the mapping of the district id and district name
dict = {'Araria': 74, 'Arwal': 78, 'Aurangabad': 77, 'Banka': 83, 'Begusarai': 98, 'Bhagalpur': 82, 'Bhojpur': 99, 'Buxar': 100, 'Darbhanga': 94, 'East Champaran': 105, 'Gaya': 79, 'Gopalganj': 104, 'Jamui': 107, 'Jehanabad': 91, 'Kaimur': 80, 'Katihar': 75, 'Khagaria': 101, 'Kishanganj': 76, 'Lakhisarai': 84, 'Madhepura': 70, 'Madhubani': 95, 'Munger': 85, 'Muzaffarpur': 86, 'Nalanda': 90, 'Nawada': 92, 'Patna': 97, 'Purnia': 73, 'Rohtas': 81, 'Saharsa': 71, 'Samastipur': 96, 'Saran': 102, 'Sheikhpura': 93, 'Sheohar': 87, 'Sitamarhi': 88, 'Siwan': 103, 'Supaul': 72, 'Vaishali': 89, 'West Champaran': 106}



#create a class of the table person
class Person(db.Model):

    __tablename__ = "person"
    d_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(10000))

    def __init__(self, d_id, email):
        self.id = id
        self.email = email



#rendering  the register form
@app.route("/")
def index():
    return render_template("form.html")



#commiting the email and district id to the database and show message
@app.route("/register", methods= ['POST', 'GET'])
def result():
    if request.method == "POST":
        d_name = request.form.get("d_name")
        email = request.form.get("Email")
        d_id = dict[d_name]
        li = Person.query.filter_by(d_id =d_id).first_or_404()
        if li.email == None:
            li.email = email
            db.session.commit()
        else:
            li.email = li.email +", "+email
            db.session.commit()
        li = Person.query.filter_by(d_id =d_id).first_or_404()
        return render_template("result.html",result="Successfully register")
    else:
        return render_template("result.html",result="Unsuccessfull register")


#rendering the deregistering form
@app.route("/de_register")
def de_register():
    return render_template("deregiter_form.html")


# commiting the deregistering in the database accordingly
@app.route("/de_reg", methods= ['POST', 'GET'])
def de_reg():
    if request.method == "POST":
        d_name = request.form.get("d_name")
        email = request.form.get("Email")
        d_id = dict[d_name]
        li = Person.query.filter_by(d_id =d_id).first_or_404()
        if li.email != None:
            li1 = str(li.email).split(', ')
            try:
                li1.remove(email)
            except:
                return render_template("result.html",result="Please check your email and District Name")
            if not li1:
                li.email = None
            else:
                li.email = ",".join(li1)
            db.session.commit()
            return render_template("result.html",result="Successfully de-register")
        else:
            return render_template("result.html",result="Unsuccessfull de-register")



if __name__ == '__main__':
    app.run(debug=True)