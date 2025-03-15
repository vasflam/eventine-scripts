import json
import os
import importlib.util

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


class SimpleJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, "__dict__"):
            return o.__dict__
        if isinstance(o, tuple):
            return list[o]
        return super().default(o)

def get_settings_file(cls):
    module_dir = os.path.dirname(os.path.abspath(importlib.util.find_spec("bigfish").origin))
    return os.path.join(module_dir, "settings", "{}.json".format(cls.__name__))

def load_settings_from_json(cls):
    settings_file = get_settings_file(cls)
    with open(settings_file, 'r') as f:
        try:
            data = json.load(f)
            return cls.from_dict(data)
        except Exception:
            return cls()

def save_settings_to_json(cls, o):
    settings_file = get_settings_file(cls)
    with open(settings_file, 'w') as f:
        json_data = json.dumps(o, indent=4, ensure_ascii=False, cls=SimpleJsonEncoder)
        f.write(json_data)

class SettingsAware:
    def save(self):
        save_settings_to_json(self.__class__, self)

    @classmethod
    def load(cls):
        settings_file = get_settings_file(cls)
        if not os.path.exists(settings_file):
            cls().save()
        return load_settings_from_json(cls)

    @classmethod
    def from_dict(cls, dct):
        raise NotImplementedError
