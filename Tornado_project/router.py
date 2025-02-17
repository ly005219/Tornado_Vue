from manager.handler import BaseHandler,UserHandler,TopicHandler,CommentHandler,CollectionHandler,FollowHandler

handlers=[
    (r"/", BaseHandler.MainHandler),
    (r"/api/user/add/?", UserHandler.AddUserHandler),
    (r"/api/send_msg/?", UserHandler.SendEmailHandler),
    (r"/api/user/login/?", UserHandler.LoginHandler),
    (r"/api/user/get/?", UserHandler.GetUserHandler),
    (r"/api/user/update/?", UserHandler.UpdateUserHandler),
    (r"/api/topic/all/?", TopicHandler.GetManyTopicHandler),
    (r"/api/topic/id/?", TopicHandler.GetOneTopicHandler),
    (r"/api/topic/add/?", TopicHandler.AddTopicHandler),
    (r"/api/topic/my/?", TopicHandler.GetMyTopicHandler),
    (r'/api/comment/get/tid/?', CommentHandler.GetCommentHandler),
    (r'/api/comment/add/?', CommentHandler.AddCommentHandler),
    (r'/api/comment/my?', CommentHandler.GetMyCommentHandler),
    ('/api/collection/add/?',CollectionHandler.AddCollectionHandler), 
    ('/api/collection/my/?',CollectionHandler.GetMyCollectionHandler), 
    ('/api/collection/delete/?',CollectionHandler.DeleteMyCollectionHandler), 
    ('/api/follow/add/?',FollowHandler.AddFollowHandler),
    ('/api/follow/judge/?',FollowHandler.GetFollowHandler),
    ('/api/follow/delete/?',FollowHandler.DeleteFollowHandler),
    ('/api/follow/get/?',FollowHandler.GetFollowHandler),
    ('/api/follow/num/?',FollowHandler.FollowNumHandler),
   

]
