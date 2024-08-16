class ChainIter:
    def __init__(self, iterable=None, offset=0):
        self.current = self
        self.next: ChainIter = None
        self._offset = offset
        self.tail = self.current
        if not iterable is None:
            self.iter = iterable
        else:
            self.iter = ChainIter.empty_iter()

    @classmethod
    def empty_iter(cls):
        return
        yield

    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            while self.current._offset > 0:
                next(self.current.iter)
                self.current._offset -= 1
            return next(self.current.iter)
        except StopIteration:
            if self.current.next is None:
                raise
            else:
                self.current = self.current.next
                return next(self.current)

    def __add__(self, next_iter):
        self.tail.next = next_iter
        self.tail = next_iter
        return self

    def offset(self, num):
        self.current._offset = num
        return self
    
    @classmethod
    def sum(cls, *args: list):
        return sum(args, start=cls())
