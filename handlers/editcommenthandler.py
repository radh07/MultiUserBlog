from google.appengine.ext import db
from google.appengine.ext import ndb
import json
import logging
from datetime import datetime

from handler import Handler
from utilities import Utilities
from models.comments import Comments

class EditCommentHandler(Handler):
    def post(self):
        logging.info(self.request.body)
        data = json.loads(self.request.body)
        # Get the comment from data store
        user_id = self.request.cookies.get("user_id")
        if user_id and len(user_id) > 0:
            l = user_id.split("|")
            if (user_id == Utilities.make_cookie_val(l[0])):
                c = Comments.get_by_id(long(data['commentid']))
                c.comment = data['updatedcomment']
                c.put()
                self.response.out.write(json.dumps(({"added": datetime.strftime(c.added, '%b %d,  %Y %I:%M %p')})))
            else:
                self.response.headers.add_header('set-cookie', str('user_id=;Path=/'))
                self.redirect('/blog')
        else:
                self.response.headers.add_header('set-cookie', str('user_id=;Path=/'))
                self.redirect('/blog')