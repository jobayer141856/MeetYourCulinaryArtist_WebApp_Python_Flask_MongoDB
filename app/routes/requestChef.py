from app import *

@app.route("/requestChef/<string:s>",  methods=['GET','POST'])

def requestChef(s):

    if request.method == 'POST':
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]

        for k in db_x.find({"username": s}):
            maill = k["email"]
        print(maill)

        msg = Message('want to be hired? ', sender='meet.hunger479@gmail.com', recipients=[maill])
        msg.body = "Message from requester for you: " + message + "\n""Requested by  " + name + "\n" "For Details Contact with " + email + " And Phone Number: " + phone
        mail.send(msg)
        return redirect(url_for("findachef"))
    return render_template("requestChef.html", **locals())
