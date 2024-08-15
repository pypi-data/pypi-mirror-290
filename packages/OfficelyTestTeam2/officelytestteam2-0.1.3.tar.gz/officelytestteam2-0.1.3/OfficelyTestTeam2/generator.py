from dataclasses import dataclass
import queue



@dataclass
class ThreadedGenerator:
    team:bool = False
    is_answer:bool = False
    full_answer:str = ""

    def __post_init__ (self):
        self.queue = queue.Queue()
        


    def __iter__(self):
        return self

    def __next__(self):
        item = self.queue.get()
        if item is StopIteration:
            raise item
        return item

    def send(self, data, is_answer=True):
        if is_answer:
            self.full_answer += data
        self.queue.put(data)

    def close(self):
        self.queue.put(StopIteration)