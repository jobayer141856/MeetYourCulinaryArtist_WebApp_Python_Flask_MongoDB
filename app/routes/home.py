from app import *

@app.route('/', methods=['GET', 'POST'])
def home():
    cuser=0
    nameuser = []
    desuser = []
    usernameuser = []
    for userth in db_user_th.find():
        nameuser.append(userth["name"])
        desuser.append(userth["description"])
        usernameuser.append(userth["username"])
        cuser+=1

    cchef=0
    namechef = []
    deschef = []
    skillchef = []
    usernamechef = []
    for chefth in db_chef_th.find():
        namechef.append(chefth["name"])
        deschef.append(chefth["description"])
        usernamechef.append(chefth["username"])
        skillchef.append(chefth["skill"])
        cchef+=1
    chef = 0
    user = 0
    chefx = False
    for x in db_chef.find():
        chef = chef+1
    for x in db_x.find():
        user = user+1
    if 'username' in session:
        username = session["username"]
        if db_chef.find_one({'username':username}):
             chefx = True

    return render_template("home.html", **locals())
