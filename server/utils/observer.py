import abc


class AbstractSubject(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def subscribe(self, obs):
        pass

    @abc.abstractmethod
    def unsubscribe(self, obs):
        pass

    @abc.abstractmethod
    def do_notify(self):
        pass


class AbstractObserver(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def do_update(self, value):
        pass


class Subject(AbstractSubject):
    def __init__(self, value):
        self.observers = []
        self.value = value

    def subscribe(self, obs):
        if obs not in self.observers:
            self.observers.append(obs)

    def unsubscribe(self, obs):
        if obs in self.observers:
            self.observers.remove(obs)

    def do_notify(self):
        for observer in self.observers:
            if isinstance(observer, AbstractObserver):
                observer.do_update(*self.value)
            elif callable(observer):
                observer(*self.value)
            else:
                raise ValueError('observer must be instance of AbstractObserver or a function')

    def next(self, *value):
        self.value = value
        self.do_notify()