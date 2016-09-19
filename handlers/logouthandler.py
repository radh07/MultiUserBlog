from handler import Handler

class LogoutHandler(Handler):
    def get(self):
        self.response.headers.add_header('set-cookie', str('user_id=;Path=/'))
        self.redirect('/blog')
