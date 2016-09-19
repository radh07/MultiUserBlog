from google.appengine.ext import db
from google.appengine.ext import ndb
import json
import logging

from handler import Handler
from utilities import Utilities
from models.likes import Likes
from models.blogposts import BlogPosts

class LikeHandler(Handler):

    @db.transactional(xg=True)
    def updateDB(self, bp, blogid, username, change, like=None, deletelikes=None):
        bp.likes = bp.likes + change
        bp.put()
        if change == 1 and like:
            like.put()
        if change == -1 and deletelikes:
            db.delete(deletelikes)
        
        return bp.likes


    def post(self):
        logging.info(self.request.body)
        data = json.loads(self.request.body)
        
        # Need blog ID to update # of likes
        # Need username so you don't like a post more than once
        # Like or unlike flag
        user_id = self.request.cookies.get("user_id")
        if user_id and len(user_id) > 0:
            l = user_id.split("|")
            if (user_id == Utilities.make_cookie_val(l[0])):
                bp = BlogPosts.get_by_id(long(data['blogid']))
                if(data['todo'] == "like"):
                    # Create a row in Likes for this user and blog combo
                    like = Likes(blogid = data['blogid'], username = data['username'])
                    # Add it to datastore and inc like count
                    count = self.updateDB(bp, data['blogid'], data['username'], 1, like=like)
                    #self.response.out.write(json.dumps(({'likes': bp.likes})))
            
                if(data['todo'] == "unlike"):
                    # Delete the entry  for this user and blog combo from Likes 
                    gqd = db.GqlQuery("select * from Likes where blogid = :1 and username = :2" , data['blogid'], data['username'])
                    deletelikes = gqd.get()
                    count = self.updateDB(bp, data['blogid'], data['username'], -1, deletelikes=deletelikes)
                self.response.out.write(json.dumps(({'likes': count})))
            else:
                self.response.headers.add_header('set-cookie', str('user_id=;Path=/'))
                self.redirect('/blog')
        else:
            self.response.headers.add_header('set-cookie', str('user_id=;Path=/'))
            self.redirect('/blog')
