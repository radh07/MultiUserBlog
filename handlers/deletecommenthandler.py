from google.appengine.ext import db
from google.appengine.ext import ndb
import json
import logging

from handler import Handler
from utilities import Utilities
from models.blogposts import BlogPosts
from models.comments import Comments


class DeleteCommentHandler(Handler):

    @db.transactional(xg=True)
    def deleteCommentInDB(self, c, bp):
        bp.comments = bp.comments - 1
        bp.put()
        db.delete(c)
        return bp.comments

    def post(self):
        logging.info(self.request.body)
        data = json.loads(self.request.body)
        user_id = self.request.cookies.get("user_id")
        if user_id and len(user_id) > 0:
            l = user_id.split("|")
            if (user_id == Utilities.make_cookie_val(l[0])):
                # Get the comment from data store
                c = Comments.get_by_id(long(data['commentid']))
                blogid = c.blogid
                # and the blogpost itself
                bp = BlogPosts.get_by_id(long(blogid))
                commentsnum = self.deleteCommentInDB(c,bp)
                self.response.out.write(json.dumps(({'blogid': str(blogid), 'commentsnum': commentsnum})))
            else:
                self.response.headers.add_header('set-cookie', str('user_id=;Path=/'))
                self.redirect('/blog')
        else:
                self.response.headers.add_header('set-cookie', str('user_id=;Path=/'))
                self.redirect('/blog')