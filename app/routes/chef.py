from pydoc import describe
from app import *

app.config['UPLOAD_FOLDER'] = '../static/img/'
app.config['SECRET_KEY'] = 'supersecretkey'


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/joinaschef', methods=['GET', 'POST'])
def joinaschef():
    if "username" in session:
        if request.method == 'POST':
            city = request.form["city"]
            skill = request.form["skill"]
            location = request.form["location"]
            esalary = request.form["salary"]
            workex = request.form["workex"]
            description = request.form["description"]

            chef = dict()
            chef["username"] = session["username"]
            chef["city"] = city
            chef["skill"] = skill
            chef["location"] = location
            chef["salary"] = esalary
            chef["workex"] = workex
            chef["description"] = description
            db_chef.insert_one(chef)
            return redirect("/findachef/"+session["username"])
        return render_template("joinaschef.html")
    else:
        return redirect(url_for("login"))


@app.route('/findachef/<string:s>', methods=['GET', 'POST'])
def findchefbycity(s):
    x = db_x.find_one({"username": s})
    y = db_chef.find_one({"username": s})
    return render_template("contact_chef.html", x=x, y=y)



@app.route('/chefthpost', methods=['GET', 'POST'])
def chefthpost():
    existchefpost = False
    if "username" in session:
        if (db_chef_th.find_one({'username': session["username"]})):
            existchefpost = True
        if request.method == 'POST':
            desc = request.form["descrp"]
            post = dict()
            if(db_chef.find_one({'username': session["username"]})) and (db_x.find_one({'username': session["username"]})):
                for x in db_chef.find({'username': session["username"]}):
                    post["username"] = x["username"]
                    post["skill"] = x["skill"]  
                for y in db_x.find({'username': session["username"]}):   
                    post["name"] = y["fullname"]
                    
                    
                                           
            post["description"] = desc

            db_chef_th.insert_one(post)
            return redirect(url_for('home'))

    print(chefthpost)

    return render_template("chefthpost.html", **locals())


@app.route('/findachef', methods=['GET', 'POST'])
def findachef():
    if "username" in session:
        if request.method == 'POST':
            city = request.form["city"]
            type = request.form["skill"]
            name = []
            city1 = []
            skill = []
            salary = []
            location = []
            description = []
            cnt = 0
            for x in db_chef.find({'city': city, 'skill': type}):
                name.append(x["username"])
                city1.append(x["city"])
                skill.append(x["skill"])
                salary.append(x["salary"])
                location.append(x["location"])
                description.append(x["description"])
                cnt = cnt+1
            return render_template("findchefbycity.html", **locals())
        name = []
        skill = []
        location = []
        description = []
        city = []
        salary = []
        cnt = 0
        for x in db_chef.find():
            name.append(x["username"])
            skill.append(x["skill"])
            location.append(x["location"])
            salary.append(x["salary"])
            description.append(x["description"])
            city.append(x["city"])
            cnt = cnt+1
        return render_template("chefs.html", **locals())
    else:
        return redirect(url_for("login"))
