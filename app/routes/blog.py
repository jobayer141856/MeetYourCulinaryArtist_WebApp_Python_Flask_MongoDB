from app import *
from datetime import datetime
from bson.objectid import ObjectId
import base64

app.config['UPLOAD_FOLDER'] = '../static/img/'
app.config['SECRET_KEY'] = 'supersecretkey'


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")
cnt = 1
@app.route('/addblog', methods=['GET', 'POST'])
def addblog():
    cnt = {}
    blogg = dict()
    blog_pic = randint(00000000, 99999999)
    fname = ""
    if "username" in session:
        form = UploadFileForm()
        if form.validate_on_submit():
            file = form.file.data  # First grab the file
            file.filename = str(blog_pic) + ".jpg"
            file.save(os.path.join(os.path.abspath(os.path.dirname(
                __file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))  # Then save the file
            fname = file.filename
            blogg["blog_pic"] = fname
            return render_template("addblog.html", form=form, fname=fname)

        if request.method == 'POST':
            title = request.form["title"]
            des = request.form["descrp"]
            blogg["title"] = title
            blogg["des"] = des
            blogg["current_time"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            blogg["blog_pic"] = str(blog_pic)+".jpg"
            blogg["username"] = session["username"]
            db_blog.insert_one(blogg)
            return redirect(url_for("blog"))
    else:
        return redirect(url_for("login"))
    return render_template("addblog.html", **locals())


@app.route('/blog', methods=['GET', 'POST'])
def blog():
    title = []
    des = []
    blog_pic = []
    current_time = []
    cnt = 0
    username = []
    id = []
    for z in db_blog.find():
        title.append(z["title"])
        des.append(z["des"])
        blog_pic.append(z["blog_pic"])
        username.append(z["username"])
        current_time.append(z["current_time"])
        id.append(z["_id"])
        cnt += 1
        # x["blog_pic"]=z["blog_pic"]
    return render_template("blog.html", **locals())


@app.route('/showblog/<string:s>', methods=['GET', 'POST'])
def showSingleblog(s):
    x = db_blog.find_one({"blog_pic": s})
    return render_template("singleBlog.html", **locals())

@app.route('/delete/<string:s>',  methods=['GET', 'POST'])
def delete(s):

    if "username" in session:
        username = session["username"]
        s = str(s)
        print("Object id " +s)
        print("username: "+ username)
        for x in db_blog.find({"username": username}):
            id = x["_id"]
            print(str(id))
            if str(id) == s:
                db_blog.delete_many({'_id': ObjectId(s)})
                return "Delete successfully"

            else:
                return "you can not delete this blog. Because you can not post this blog"

    return render_template("Blog.html", **locals())




@app.route('/userthpost',  methods=['GET', 'POST'])

def userthpost():

    return render_template("userthpost.html", **locals())
