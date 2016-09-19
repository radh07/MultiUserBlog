from google.appengine.ext import db
from google.appengine.ext import ndb
import json
import logging

from handler import Handler
from utilities import Utilities
from models.comments import Comments
from models.likes import Likes
from models.blogposts import BlogPosts

class DeletePostHandler(Handler):

    @db.transactional(xg=True)
    def deletePostInDB(self, c, l, bp):
        logging.info("in deletePostInDB")
        if c:          
            db.delete(c)
            logging.info("in deletePostInDB del c")

        if l:          
            db.delete(l)
            logging.info("in deletePostInDB del l")

        db.delete(bp)
        logging.info("in deletePostInDB del bp")
        return True

    def post(self, blogid):
        logging.info("post del")
        user_id = self.request.cookies.get("user_id")
        if user_id and len(user_id) > 0:
            l = user_id.split("|")
            if (user_id == Utilities.make_cookie_val(l[0])):
                # Get the comments from data store
                cq = db.GqlQuery("select * from Comments where blogid = :1", blogid)
                c = cq.get()
                # and the likes
                lq = db.GqlQuery("select * from Likes where blogid = :1", blogid)
                l = lq.get()
                # and the blogpost itself
                bp = BlogPosts.get_by_id(long(blogid))
                if self.deletePostInDB(c, l, bp):
                    self.response.out.write(json.dumps(({'delete': "success"})))
            else:
                self.response.headers.add_header('set-cookie', str('user_id=;Path=/'))
                self.redirect('/blog')
        else:
                self.response.headers.add_header('set-cookie', str('user_id=;Path=/'))
                self.redirect('/blog')
