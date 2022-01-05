import os, warnings

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///calendar.db")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id, group_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        get_username = request.form.get("username")
        get_password = request.form.get("password")

        # Ensure username was submitted
        if not get_username:
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not get_password:
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", get_username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], get_password):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["group_id"] = rows[0]["group_id"]

        # Flash for successful log-in
        flash('Logged In!')

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id, group_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST
    if request.method == "POST":
        get_username = request.form.get("username")
        get_password = request.form.get("password")
        get_confirmation = request.form.get("confirmation")
        
        # Ensure username was submitted
        if not get_username:
            return apology("must provide username", 400)

        # Ensure ' is not in the username
        elif "'" in get_username:
            return apology("cannot enter prohibited character", 400)

        # Ensure password was submitted
        elif not get_password:
            return apology("must provide password", 400)

        # Ensure password was re-submitted
        elif not get_confirmation:
            return apology("must confirm your password", 400)
        
        # Ensure username is new
        test = db.execute("SELECT * FROM users WHERE username = ?", get_username)
        if len(test) == 1:
            return apology("this username already exists", 400)
        
        # Ensure the password and the confirmation password match
        if get_password != get_confirmation:
            return apology("the passwords must match", 400)

        # Insert the username and the hashed password into the table users
        hashed_password = generate_password_hash(get_password)
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", get_username, hashed_password)
        
        # Remember which user has logged in
        rows = db.execute("SELECT * FROM users WHERE username = ?", get_username)
        session["user_id"] = rows[0]["id"]
        session["group_id"] = rows[0]["group_id"]

        # Flash successful registering
        flash('Registered!')

        # Redirect user to home page
        return redirect("/")
        
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

# General function for creating calendar. The input is the calendar's user_id.
def calendar(user_id):
    events = db.execute("SELECT title, start, end, color FROM events WHERE user_id = ?", user_id)
    return events

@app.route("/")
@login_required
def index():
    """Homepage"""

    # Returns the homepage, which is the user's own calendar
    return render_template("calendar.html", events=calendar(session["user_id"]), username="My")

@app.route("/add-events", methods=["GET", "POST"])
@login_required
def addEvents():
    """Add/Create Events"""

    # User reached route via POST
    if request.method == "POST":

        get_eventname = request.form.get("event-name")
        get_startdate = request.form.get("start-date")
        get_starttime = request.form.get("start-time")
        get_enddate = request.form.get("end-date")
        get_endtime = request.form.get("end-time")

        # Ensure event was submitted
        if not get_eventname:
            return apology("must provide event", 400)

        # Ensure start date was submitted
        elif not get_startdate:
            return apology("must provide start date", 400)

        # Ensure start time was submitted
        elif not get_starttime:
            return apology("must provide start time", 400)

        # Ensure end date was submitted
        elif not get_enddate:
            return apology("must provide end date", 400)
        
        # Ensure end time was submitted
        elif not get_endtime:
            return apology("must provide end time", 400)

        # Ensure start date is before the end date
        elif get_startdate > get_enddate:
            return apology("invalid time", 400)

        # Ensure that a single-day event's start time is before the end time
        elif (get_startdate == get_enddate) and (get_starttime > get_endtime):
            return apology("invalid time", 400)

        # Ensure the problematic characters ', ", \, or & are not in the event title
        prohibited_chars = ["'" , '"' , '\\' , '&']
        for char in prohibited_chars:
            if char in get_eventname:
                return apology("cannot enter prohibited characters", 400)

        # Create a string that combines the date and time suited for FullCalendar
        start_timestamp = get_startdate + "T" + get_starttime + ":55.008"
        end_timestamp = get_enddate + "T" + get_endtime + ":55.008"
        time = get_startdate + " @" + get_starttime + " to " + get_enddate + " @" + get_endtime
        color = request.form.get("color")

        # Insert event information to the events table
        db.execute("INSERT INTO events (user_id, title, start, end, time, color) VALUES(?, ?, ?, ?, ?, ?)", 
                   session["user_id"], get_eventname, start_timestamp, end_timestamp, time, color)
        
        # Flash successful event addition
        flash('Added Event!')

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        # A list of possible color choices
        colors = ['red', 'blue', 'green', 'purple', 'pink', 'yellow', 'aqua', 'orange', 'gray', 'black',
                  'aliceblue', 'antiquewhite', 'aquamarine', 'azure', 'beige', 'bisque', 'blanchedalmond',
                  'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue',
                  'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen',
                  'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 
                  'darkseagreen', 'darkslateblue', 'darkslategray', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 
                  'dimgray', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 
                  'goldenrod', 'greenyellow', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 
                  'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 
                  'lightgray', 'lightgreen', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 
                  'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'maroon', 'mediumaquamarine', 'mediumblue', 
                  'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 
                  'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccassin', 'navajowhite', 'navy', 'oldlace', 
                  'olive', 'olivedrab', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 
                  'papayawhip', 'peachpuff', 'peru', 'plum', 'powderblue', 'rosybrown', 'royalblue', 'saddlebrown', 'seagreen', 
                  'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'snow', 'springgreen', 'steelblue', 'teal', 
                  'thristle', 'tomato', 'violet', 'white']
        return render_template("add-events.html", colors=colors)

@app.route("/delete-events", methods=["GET", "POST"])
@login_required
def deleteEvents():
    """Delete Existing Events"""

    # User reached the route via POST
    if request.method == "POST":

        get_event = request.form.get("event")

        # Ensure event was selected
        if not get_event:
            return apology("must select an event", 400)

        # Delete the selected event from the events table https://www.w3schools.com/python/ref_string_split.asp00
        event_title = get_event.split("'")[3]
        event_time = get_event.split("'")[7]
        db.execute("DELETE FROM events WHERE user_id = ? AND title = ? AND time = ?", 
                   session["user_id"], event_title, event_time)
        
        # Flash successful event addition
        flash('Delete Event!')

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Give the list of possible events 
        list_events = db.execute("SELECT title, time FROM events WHERE user_id = ? ORDER BY time", session["user_id"])
        if len(list_events) == 0:
            warning = "You currently do not have any events."
            return render_template("delete-events.html", warning=warning)
        return render_template("delete-events.html", list_events=list_events)

@app.route("/create-group", methods=["GET", "POST"])
@login_required
def createGroup():
    """Create Group"""

    # User reached route via POST
    if request.method == "POST":
        get_groupname = request.form.get("groupname")
        get_password = request.form.get("password")
        get_confirmation = request.form.get("confirmation")
        
        # Ensure groupname was submitted
        if not get_groupname:
            return apology("must provide group name", 400)

        # Ensure password was submitted
        elif not get_password:
            return apology("must provide password", 400)

        # Ensure password was re-submitted
        elif not get_confirmation:
            return apology("must confirm your password", 400)
        
        # Ensure groupname is new
        test = db.execute("SELECT * FROM groups WHERE groupname = ?", get_groupname)
        if len(test) == 1:
            return apology("this group name already exists", 400)
        
        # Ensure the password and the confirmation password match
        if get_password != get_confirmation:
            return apology("the passwords must match", 400)

        # Insert the groupname and the hashed password into the table groups
        hashed_password = generate_password_hash(get_password)
        db.execute("INSERT INTO groups (groupname, hash) VALUES(?, ?)", get_groupname, hashed_password)
        
        # Remember which group the user has logged in
        rows = db.execute("SELECT * FROM groups WHERE groupname = ?", get_groupname)
        session["group_id"] = rows[0]["id"]

        # Insert the group_id into the table users
        db.execute("UPDATE users SET group_id = ? WHERE id = ?", session["group_id"], session["user_id"])

        # Flash successful registering
        flash('Created Group!')

        # # Redirect user to home page
        return redirect("/")
        
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("create-group.html")

@app.route("/account-info")
@login_required
def accountInfo():
    """Display User's Account Information"""

    # Get the user's username
    user = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]

    # If the user is not associated to a group, make the value for the groupname empty
    if not session["group_id"]:
        user["groupname"] = ""

    # Otherwise, add the groupname to the user dictionary
    else:
        groupname = db.execute("SELECT groupname FROM groups WHERE id = ?", session["group_id"])[0]
        user["groupname"] = groupname["groupname"]
    return render_template("account-info.html", user=user)

@app.route("/manage-group")
@login_required
def manageGroup():
    """Manage Group"""

    # If the user is not in a group, give the option to join a group
    if not session["group_id"]:
        return redirect("/join-group")

    # If the user is already in a group, give an option to leave
    else:
        return redirect("/leave-group")

@app.route("/join-group", methods=["GET", "POST"])
@login_required
def joinGroup():
    """Join Group"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        get_groupname = request.form.get("groupname")
        get_password = request.form.get("password")

        # Ensure groupname was submitted
        if not get_groupname:
            return apology("must provide group name", 403)

        # Ensure password was submitted
        elif not get_password:
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM groups WHERE groupname = ?", get_groupname)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], get_password):
            return apology("invalid group name and/or password", 403)

        # Remember which group the user has joined
        session["group_id"] = rows[0]["id"]

        # Record the group id to the user info
        db.execute("UPDATE users SET group_id = ? WHERE id = ?", session["group_id"], session["user_id"])

        # Flash for successful log-in
        flash('Joined Group!')

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("join-group.html")

@app.route("/leave-group", methods=["GET", "POST"])
@login_required
def leaveGroup():
    """Leave Group"""

    # Gets the number of users in this particular group
    numOfUsers = len(db.execute("SELECT * FROM users WHERE group_id = ?", session["group_id"]))

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # If there is only one user left in the group, delete the group
        if numOfUsers == 1:
            db.execute("DELETE FROM groups WHERE id = ?", session["group_id"])

        # Disassociate the user from this group
        db.execute("UPDATE users SET group_id = NULL WHERE id = ?", session["user_id"])
        session.update(group_id = None)
        
        # Flash for successful log-in
        flash('Left Group!')

        # Redirect user to home page
        return redirect("/")

    
    # User reached route via GET (as by clicking a link or via redirect)
    else:

        # If there is only one user left in the group, then offer a warning
        if numOfUsers == 1:
            warning = "You are the last user in this group. Thus, if you leave, this group will be automatically deleted."
            return render_template("leave-group.html", warning=warning)
        else:
            return render_template("leave-group.html")

@app.route("/groupmates", methods=["GET", "POST"])
@login_required
def groupmates():
    """Select and View Groupmate's Schedule"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        get_groupmate = request.form.get("groupmate")

        # Ensure groupmate was submitted
        if not get_groupmate:
            return apology("must select a groupmate", 403)

        # Get the user_id of the selected groupmate
        groupmate = get_groupmate.split("'")[3]
        groupmate_id = db.execute("SELECT id FROM users WHERE username = ?", groupmate)[0].get("id")
        return render_template("calendar.html", events=calendar(groupmate_id), username=groupmate+"'s")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # List of groupmates excluding the user themself
        groupmates = db.execute("SELECT username FROM users WHERE group_id = ? EXCEPT SELECT username FROM users WHERE id = ? ORDER BY username", 
                                    session["group_id"], session["user_id"])

        # If the user is not in a group.
        if not session["group_id"]:
            warning = "You are currently not in a group"
            return render_template("groupmates.html", warning=warning)

        # If the user is the only on in the group
        elif len(groupmates) == 0:
            warning = "You are the only one in this group"
            return render_template("groupmates.html", warning=warning)

        # If the user has groupmates in their group, give the option to select their groupmates (not including the user themself)
        else:
            return render_template("groupmates.html", groupmates=groupmates)

@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    """Change password"""
    
    # User reached route via POST
    if request.method == "POST":

        get_old = request.form.get("old")
        get_new = request.form.get("new")
        get_confirmation = request.form.get("confirmation")

        # Ensure old password was submitted
        if not get_old:
            return apology("must provide old password", 400)

        # Ensure old password is the current password
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        if not check_password_hash(rows[0]["hash"], get_old):
            return apology("incorrect old password", 400)

        # Ensure new password was submitted
        elif not get_new:
            return apology("must provide new password", 400)

        # Ensure password was re-submitted
        elif not get_confirmation:
            return apology("must confirm your new password", 400)
        
        # Ensure the new password and the confirmation password match
        if get_new != get_confirmation:
            return apology("the passwords must match", 400)

        # Update the hashed password into the table users
        hashed_new = generate_password_hash(get_new)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", hashed_new, session["user_id"])
        
        # Flash successful change of password
        flash('Changed Password!')

        # Redirect user to home page
        return redirect("/")
        
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("password.html")
