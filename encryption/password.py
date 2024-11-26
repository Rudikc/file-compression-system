class Password:
    def __init__(self, value):
        if not value or len(value) < 6:
            raise ValueError("Password must be at least 6 characters long")
        self.value = value

    def to_bytes(self):
        return self.value.encode()

    def __str__(self):
        return "*" * len(self.value)
