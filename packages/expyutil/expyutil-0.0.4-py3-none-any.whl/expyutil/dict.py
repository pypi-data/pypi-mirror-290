
class DictGetter:
    def __init__(self, v) -> None:
        self.v = v
    
    def get(self, s: str):
        keys = s.split(".")
        item = self.v
        for k in keys:
            item = item[k]
        return item
        