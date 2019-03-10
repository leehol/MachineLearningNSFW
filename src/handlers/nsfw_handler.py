from tornado.concurrent import run_on_executor
from business_logic.nsfw_detection import is_nsfw
from handlers.basics.base_handler import BasicHandler


class NSFWHandler(BasicHandler):
    @run_on_executor
    def background_task(self):
        data = self.verify()
        res = is_nsfw(data)
        return res
