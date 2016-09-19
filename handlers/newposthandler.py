from handler import Handler
from utilities import Utilities

from models.blogposts import BlogPosts

class NewPostHandler(Handler):
    def get(self):
        username = ""
        user_id = self.request.cookies.get("user_id")
        if user_id and len(user_id) > 0:
            l = user_id.split("|")
            if (user_id == Utilities.make_cookie_val(l[0])):
                username = l[0]
                #self.response.headers.add_header('set-cookie', str('user_id=%s' % make_cookie_val(username)))
                self.render("newpost.html", username = username)
            else:
                self.redirect("/blog")
        else:
            self.redirect("/blog")
    
    def post(self):
        user_id = self.request.cookies.get("user_id")
        if user_id and len(user_id) > 0:
            l = user_id.split("|")
            if (user_id == Utilities.make_cookie_val(l[0])):
                username = l[0]
                subject = self.request.get("subject")
                content = self.request.get("content")
                if not subject or not content:
                    error_msg = "Both Subject and Content are required."
                    self.render("newpost.html", username= username, error_msg = error_msg, content = content, subject = subject)
                else:
                    #Add a new blog post to data store and publish the permalink with /blog/[NUMBER] where NUMBER is obj.key().id()
                    bp = BlogPosts(subject = subject, content = content, author = username)#, permalink = "/blog/")
                    # bpkey = bp.put()
                    # bp = db.get(bpkey)
                    # # bp.permalink = "/blog/"+str(bpkey.id())
                    bp.put()
                    self.redirect("/blog/"+str(bp.key().id()))
            else:
                self.response.headers.add_header('set-cookie', str('user_id=;Path=/'))
                self.redirect('/blog')