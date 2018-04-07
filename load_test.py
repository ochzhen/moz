from locust import HttpLocust, TaskSet

def login(l):
    l.client.post("/login", {"username":"", "password":""})

def index(l):
    l.client.get("/")


class UserBehavior(TaskSet):
    tasks = {index: 2}

    # def on_start(self):
    #     login(self)

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000