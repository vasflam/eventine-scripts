class Observable:
    def __init__(self):
        self._observers = []

    def notify(self, modifier = None):
        for observer in self._observers:
            if modifier != observer:
                observer.update(self)

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

class Observer:
    def update(self, observable: Observable):
        pass
