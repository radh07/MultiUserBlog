from utilities import Utilities
from handler import Handler

class LoginHandler(Handler):
    def get(self):
        self.render("login.html")

    def post(self):
        # verify login name and password from datastore.
        username = self.request.get("username")
        password = self.request.get("password")
        if username and password and Utilities.valid_username(username) and Utilities.valid_password(password) and Utilities.valid_user(username, password):
            self.response.headers.add_header('set-cookie', str('user_id=%s' % Utilities.make_cookie_val(username)))
            self.redirect('/blog')
        else:
            self.render("login.html", error_message = "Invalid login.")
