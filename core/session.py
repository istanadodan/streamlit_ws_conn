class ChatSession:
    def __init__(self):
        self.session_id = None
        self.history = []

    def start(self):
        import uuid

        self.session_id = uuid.uuid4().hex

    def add(self, role, content):
        self.history.append({"role": role, "content": content})
