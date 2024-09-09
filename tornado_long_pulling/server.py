import tornado.gen
import tornado.ioloop
import tornado.web

# Simulate some "messages" that clients might want to poll
messages = []


# A simple handler that will perform long-polling
class LongPollingHandler(tornado.web.RequestHandler):
    async def get(self):
        last_message_index = int(self.get_argument("last_message", 0))

        # Check if there are new messages to send to the client
        while last_message_index >= len(messages):
            # Wait for 1 second and then check again (simulating long polling)
            await tornado.gen.sleep(1)

        # Return new messages to the client
        self.write({"messages": messages[last_message_index:]})


class PostMessageHandler(tornado.web.RequestHandler):
    def post(self):
        message = self.get_argument("message")
        messages.append(message)
        self.write({"status": "Message received!"})


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")  # Render the HTML file


def make_app():
    return tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/poll", LongPollingHandler),
            (r"/post", PostMessageHandler),
        ]
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Long-polling server started on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
