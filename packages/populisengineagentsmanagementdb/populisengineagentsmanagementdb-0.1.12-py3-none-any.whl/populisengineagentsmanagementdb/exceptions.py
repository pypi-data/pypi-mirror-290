class ItemNotFound(Exception):
    def __init__(self, item_id):
        self.message = f"Item with id {item_id} not found."
        super().__init__(self.message)
