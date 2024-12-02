# Define courier class
class Courier:
    def __init__(self, location):
        self.location = location  # (x, y)
        self.is_busy = False
        self.current_order = None