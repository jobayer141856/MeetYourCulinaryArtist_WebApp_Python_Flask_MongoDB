from app import *


@app.route('/userthpost1', methods=['GET', 'POST'])

def userthpost1():
    exist = False
    if "username" in session:
        name = session["username"]
        if (db_user_th.find_one({'username': name})):
            exist = True
        if request.method == 'POST':
            desc = request.form["descrp"]
            print(desc)
            post = dict()
            for z in db_x.find({'username': session["username"]}):
                post["username"] = z["username"]
                post["name"] = z["fullname"]
                post["description"] = desc
                db_user_th.insert_one(post)
                print(post)
                return redirect(url_for('home'))
    print (exist)
    return render_template("userthpost.html", **locals())
