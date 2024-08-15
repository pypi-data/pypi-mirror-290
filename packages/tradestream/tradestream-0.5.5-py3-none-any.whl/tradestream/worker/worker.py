import os

import redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()


# import os

# from redis import Redis
# from rq import Worker, Queue, Connection
# from typing import List

# DEFAULT_CONNECTION_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')

# class TaskMaster:
#     def __init__(self, connection_url: str = DEFAULT_CONNECTION_URL, channel_subscriptions: List[str] = None):
#         """
#         Initialize the TaskMaster with the given connection URL.
#         """
#         self.connection = Redis.from_url(connection_url)
#         self.job_queue = Queue(connection=self.connection)
#         self.channel_subscriptions = channel_subscriptions or []

#     def work(self):
#         """
#         Start the worker and process tasks from the queue.
#         """
#         with Connection(self.connection):
#             print("Connected to Redis")
#             worker = Worker([self.job_queue])
#             print("Worker created")
#             worker.work()
#             print("Worker working")

# # Create a queue
# q = Queue(connection=Redis.from_url(DEFAULT_CONNECTION_URL))

# # Create a connection to the Redis server
# REDIS_CONNECTION_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
# worker_listen: List[str] = ["high", "default", "low"]

# # Create a worker
# worker = TaskMaster(REDIS_CONNECTION_URL,worker_listen)
