import Pyro4

@Pyro4.expose
class CentralServer:
    def __init__(self):
        self.request_queue = []
        self.in_cs = False

    def request_cs(self):
        self.request_queue.append(True)
        return True

    def release_cs(self):
        if self.request_queue:
            self.request_queue.pop(0)
            return True
        return False 

    def can_enter_cs(self):
        return not self.in_cs and self.request_queue and self.request_queue[0]

def main():
    central_server = CentralServer()
    daemon = Pyro4.Daemon(port=50000)
    uri = daemon.register(central_server, objectId="central_server")
    print("Central Server URI:", uri)
    daemon.requestLoop()

if __name__ == "__main__":
    main()
