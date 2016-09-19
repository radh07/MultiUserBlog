from google.appengine.ext import db
from google.appengine.ext import ndb
import json
import logging
from datetime import datetime

from handler import Handler
from utilities import Utilities
from models.blogposts import BlogPosts
from models.comments import Comments



class CommentHandler(Handler):

    @db.transactional(xg=True)
    def insertCommentAndInc(self, bp, newcomment):
        bp.comments += 1
        bp.put()
        newcomment.put()
        return newcomment.added, bp.comments, newcomment.key().id()

    def post(self):
        logging.info(self.request.body)
        data = json.loads(self.request.body)
        # need blog to increment number of posts
        user_id = self.request.cookies.get("user_id")
        if user_id and len(user_id) > 0:
            l = user_id.split("|")
            if (user_id == Utilities.make_cookie_val(l[0])):
                logging.info(user_id + " " + l[0])
                bp = BlogPosts.get_by_id(long(data['blogid']))
                # new Comment to add to data store
                newcomment = Comments(blogid = str(data['blogid']), comment = data['comment'], commenter = data['username'])
                added, count, commentid = self.insertCommentAndInc(bp, newcomment)
                addedstr = datetime.strftime(added, '%b %d,  %Y %I:%M %p')
                self.response.out.write(json.dumps(({'added': str(addedstr), 'comments': count, "commentid" : commentid })))
            else:
                self.response.headers.add_header('set-cookie', str('user_id=;Path=/'))
                self.redirect('/blog')
        else:
                self.response.headers.add_header('set-cookie', str('user_id=;Path=/'))
                self.redirect('/blog')
