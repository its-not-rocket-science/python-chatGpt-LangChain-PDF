from flask import current_app
from threading import Thread
from queue import Queue
from app.chat.callbacks.stream import StreamingHandler


class StreamableChain:
    def strean(self, input, config, **kwargs):
        queue = Queue()
        handler = StreamingHandler(queue)

        def task(app_context):
            app_context.push()
            self.invoke(input, config, **kwargs, callbacks=[handler])

        Thread(target=task, args=[current_app.app_context()]).start()

        while True:
            token = queue.get()
            if token is None:
                break
            yield token
