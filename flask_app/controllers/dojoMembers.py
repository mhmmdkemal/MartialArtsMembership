from flask_app import app
from flask_app.models import user, dojoMember 
from flask import render_template, request, redirect, session

#Routes below
@app.route("/member/dashboard")
def all_member_page():
    #check if "user_id" is not in session if not redirect
    if "user_id" not in session:
        return redirect("/")
    #get id from session
    data = {
        "id": session["user_id"]
    }
    return render_template("all_dojoMember.html", this_user= user.User.get_user_by_id(data), all_member=dojoMember.DojoMember.get_all_member())

#route that will show the new dojoMember page 
@app.route("/member/new/member")
def new_member_page():
    #check if "user_id" is not in session if not redirect
    if "user_id" not in session:
        return  redirect("/")
    data = {
        "id": session["user_id"]
    }
    return render_template("add_dojoMember.html", this_user= user.User.get_user_by_id(data))

#route that will show the edit dojoMember page 
@app.route("/member/<int:id>/edit")
def edit_member_page(id):
    #check if "user_id" is not in session if not redirect
    if "user_id" not in session:
        return  redirect("/")
    data = {
        "id": id
    }
    return render_template("edit_dojoMember.html", this_dojoMember = dojoMember.DojoMember.get_one_member(data))

#route that will show a dojoMember page 
@app.route("/member/show/<int:id>")
def view_member_page(id):
    #check if "user_id" is not in session if not redirect
    if "user_id" not in session:
        return  redirect("/")

    data = {
        "id": id
    }
    return render_template("view_dojoMember.html", this_dojoMember = dojoMember.DojoMember.get_one_member(data))

#route that shows a user's member
@app.route("/user/account")
def user_account_member_page():
    #check if "user_id" is not in session if not redirect
    if "user_id" not in session:
        return redirect("/")
    #get id from session
    data = {
        "id": session["user_id"]
    }
    return render_template("user_account_dojoMember.html", this_user= user.User.get_user_by_id(data), all_member=dojoMember.DojoMember.get_all_member())


#route that will delete a dojoMember from db 
@app.route("/member/<int:id>/delete")
def delete_member(id):
    #check if "user_id" is not in session if not redirect
    if "user_id" not in session:
        return  redirect("/")    
    data = {
        "id": id
    }
    dojoMember.DojoMember.delete_member(data)
    return redirect("/user/account")


#route that will delete a dojoMember from db 
@app.route("/member/add_to_db", methods=["POST"])
def add_member_to_db():
    #check if "user_id" is not in session if not redirect
    if "user_id" not in session:
        return  redirect("/") 
    #validate user input if it fails redirect 
    if not dojoMember.DojoMember.validate_member(request.form):
        return redirect("/member/new/member")
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "age": request.form["age"],
        "location": request.form["location"],
        "martial_type": request.form["martial_type"],
        "plan_type": request.form["plan_type"],
        "date_received": request.form["date_received"],
        "user_id": session["user_id"],
    }
    dojoMember.DojoMember.add_member_to_db(data) #talk to the model to add dojoMember to the db
    return redirect ("/member/dashboard")

#route that will edit a dojoMember in db 
@app.route("/member/<int:id>/edit_in_db", methods=["POST"])
def edit_member_in_db(id):
    #check if "user_id" is not in session if not redirect
    if "user_id" not in session:
        return  redirect("/")
    #check if the validatin passes, if it fails, redirect
    if not dojoMember.DojoMember.validate_member(request.form):
        return redirect(f"/member/{id}/edit")

    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "age": request.form["age"],
        "location": request.form["location"],
        "martial_type": request.form["martial_type"],
        "plan_type": request.form["plan_type"],
        "date_received": request.form["date_received"],
        "id": id,
    }
    dojoMember.DojoMember.update_member(data)
    return redirect("/member/dashboard")