from google.appengine.ext import db
from google.appengine.ext import ndb

from utilities import Utilities
from handler import Handler
from models.blogposts import BlogPosts
from models.comments import Comments
from models.likes import Likes

class BlogPostHandler(Handler):
    def get(self, bpid):        
        username = ""
        user_id = self.request.cookies.get("user_id")
        if user_id and len(user_id) > 0:
            l = user_id.split("|")
            if (user_id == Utilities.make_cookie_val(l[0])):
                username = l[0]
        bp = BlogPosts.get_by_id(long(bpid))
        likedposts = []
        if username and len(username) > 0:
            #self.response.headers.add_header('set-cookie', str('user_id=%s' % make_cookie_val(username)))
            gql = db.GqlQuery("select * from Likes where blogid = :1 and username = :2" , bpid, username)
            if gql.fetch(1):
                likedposts.append(bpid)
        # Get all comments for this blog post
        comments = db.GqlQuery("Select * from Comments where blogid = :1 order by added desc", bpid)

        self.render("blogpost.html", username = username, blogpost = bp, likedposts = likedposts, comments = comments)

    #6333186975989760
    def post(self):
        self.response.out.write(self.request)
