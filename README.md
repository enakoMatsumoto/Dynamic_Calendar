User's Manual
Demo video: https://youtu.be/DNVE4VrX-Ns

Running the website:
After opening up the project folder in codespace, the user should go into the folder (`cd project`) and then type `flask run` in the terminal to start the server.

Register/Log In:
After opening up the web application, the user is prompted to either log in or register. If the user has not created an account, they could register by entering their username once and their password twice for confirmation and by hitting the `Register and Log In` button. If the user already has an account, then log in by entering the username and password. If there is missing or wrong information, the user gets error warnings.

Different Calendar Functions:

1) User's calendar: When a user logs in, the first page seen is the user's own calendar. The user can always view their calendar by clicking on `Dynamic Calendar` in the top left corner of the web page. The calendar page has multiple features. The user can view the calendar in month, week, or day format by clicking on the buttons on the right hand side. If the page shown does not display today's date, the user can click the button `today` to jump straight back to a page containing today's date.
2) Click `Add Events` in the menu to create events that will be recorded in the calendar. Events, start date and time, end date and time are required, and blank or illogical inputs (like end date/time coming before the start date/time) will give error messages. The event color is optional. The default is a shade of blue, but the user can choose from a wide range of colors with the drop-down selection menu. Hit enter to record the event. The button will automatically redirect the user to their calendar with the newly added event. 
3) Click `Delete Events` in the menu to delete events on the calendar. The drop-down menu lists the events in chronological order. Make a selection and hit `Delete Event` button. No selection will lead to an error warning. After hitting the button, the user will again be directed to their calendar with the proper event deleted. 
4) Click `Create Group` in the menu to create a group name and password that the user can share with fellow groupmates. Fill out all of the three required information (group name, password, confirmation password), and hit `Create Group` button to record your response. If the group name, password, or the confirmation password is left blank or there are other mistakes, the user gets an error warning. 
5) Click `Manage Group` in the menu to join or leave a group. Note that a user can only be in one group at a time. Therefore, if a user is already in a group, they are directed to a page that prompts them to leave a group. The user can click on the `Leave Group` button to leave the group, and then they are automatically redirected to the homepage (a.k.a. the user's calendar). If the user is not in a group, they are prompted to join one by entering the group name and password. If any of the prompted information are left blank or wrong, the user gets an error messsage. Click on the `Join Group` button to record your response; then the user is automatically redirected to the homepage. 
6) Click `See Groupmates` in the menu to select the groupmate whose schedule the user would like to view. If the user is not in a group, they are prompted with an alert that says, "You are currently not in a group." In this case, there are no choices in the selection bar, and even if the user clicks on `See Their Schedule` button, they get an error message. If the user is in a group but is the only member in it, then they get a different alert saying, "You are the only one in this group." Like before, there is no choices in the selection bar, and clicking the button will lead to an error message. If the user, however, is in a group with other groupmates, then the selection bar offers the user with a list of their groupmates' usernames. The user can select one username, and click on `See Their Schedule` button. Then, the user is prompted to that groupmate's calendar (notice how the header changes to {groupmate's username}'s Calendar to clarify that that the user is not looking at their own calendar.) If the user does not make a selection and clicks on `See Their Schedule` button, they get an error message.
7) Click `Change Password` in the menu to change password. The user must entire their old password, the new password, and then confirm the new password. If any of these prompts are left blank and/or wrong, the user receives an error message. The user should click on `Change Password` button to record the change. 
8) Click `Account Info` in the menu to view a table that shows the user's username and groupname (if the user is currently in a group). Any time the user leaves or joins a group, that information is reflected in this section. This is helpful when the user forgets their own username or groupname and would like to quickly access that information.
9) Click `Log Out` in the menu to log out of the current user's account. After clicking on this menu tab, the user is redirected to the original logged out state in which they have the choice of either logging into an already-existing account or register/create a new account. 