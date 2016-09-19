from google.appengine.ext import db
from google.appengine.ext import ndb
from handler import Handler
from utilities import Utilities
from models.blogposts import BlogPosts


class EditPostHandler(Handler):
    def get(self, bpid):
        username = ""
        user_id = self.request.cookies.get("user_id")
        if user_id and len(user_id) > 0:
            l = user_id.split("|")
            if (user_id == Utilities.make_cookie_val(l[0])):
                username = l[0]
                #self.response.headers.add_header('set-cookie', str('user_id=%s' % make_cookie_val(username)))
                bp = BlogPosts.get_by_id(long(bpid))

                self.render("editpost.html", username = username, subject = bp.subject, contents = bp.content, blogid = str(bpid))
            else:
                self.response.headers.add_header('set-cookie', str('user_id=;Path=/'))
                self.redirect('/blog')
        else:
            self.response.headers.add_header('set-cookie', str('user_id=;Path=/'))
            self.redirect('/blog')
   
    def post(self, bpid):
        user_id = self.request.cookies.get("user_id")
        if user_id and len(user_id) > 0:
            l = user_id.split("|")
            if (user_id == Utilities.make_cookie_val(l[0])):
                username = l[0]
                subject = self.request.get("subject")
                content = self.request.get("content")
                if not subject or not content:
                    error_msg = "Both Subject and Content are required."
                    self.render("newpost.html", username = username, error_msg = error_msg, content = content, subject = subject)
                else:
                    #Update the blog post in data store and publish the permalink with /blog/[NUMBER] where NUMBER is obj.key().id()
                    bp = BlogPosts.get_by_id(long(bpid))
                    bp.subject = subject
                    bp.content = content
                    bp.put()
                    self.redirect("/blog/"+str(bp.key().id()))
            else:
                self.response.headers.add_header('set-cookie', str('user_id=;Path=/'))
                self.redirect('/blog')
        else:
            self.response.headers.add_header('set-cookie', str('user_id=;Path=/'))
            self.redirect('/blog')
