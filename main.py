# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
from handlers.handler import Handler
from handlers.mainpagehandler import MainPageHandler
from handlers.signuphandler import SignupHandler
from handlers.loginhandler import LoginHandler
from handlers.logouthandler import LogoutHandler
from handlers.blogposthandler import BlogPostHandler
from handlers.newposthandler import NewPostHandler
from handlers.editposthandler import EditPostHandler
from handlers.deleteposthandler import DeletePostHandler
from handlers.likehandler import LikeHandler
from handlers.commenthandler import CommentHandler
from handlers.editcommenthandler import EditCommentHandler
from handlers.deletecommenthandler import DeleteCommentHandler


app = webapp2.WSGIApplication([
    ('/blog', MainPageHandler),
    ('/blog/([0-9]*)', BlogPostHandler),
    ('/blog/newpost', NewPostHandler),
    ('/blog/editpost/([0-9]*)', EditPostHandler),
    ('/blog/deletepost/([0-9]*)', DeletePostHandler),    
    ('/signup', SignupHandler),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/like', LikeHandler),
    ('/comment', CommentHandler),    
    ('/commentedit', EditCommentHandler),
    ('/commentdelete', DeleteCommentHandler)
    
], debug=True)
