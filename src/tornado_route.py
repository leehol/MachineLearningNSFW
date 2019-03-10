from handlers import nsfw_handler as nh


routes = [
        (r"/video_check", nh.NSFWHandler),
]
