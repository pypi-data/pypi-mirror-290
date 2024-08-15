import json
import sys
import importlib.util
import os
from datetime import datetime
from dataclasses import dataclass, field



DIR = os.getcwd()


def new_namespace(namespace: str):
    """Creates and returns a new namespace as a module, isolated from 
    the original pytzen package.
    """

    pytzen = importlib.util.find_spec('pytzen')
    vars()[namespace] = importlib.util.module_from_spec(pytzen)
    pytzen.loader.exec_module(vars()[namespace])
    sys.modules[namespace] = vars()[namespace]
    vars()[namespace].MetaType.NAMESPACE = namespace

    return vars()[namespace]



class MetaType(type):
    """Metaclass for ProtoType class. It is responsible for adding the 
    meta_attr attribute to the class and initializing the ProtoType 
    class.
    """

    NAMESPACE: str = None
    def __new__(cls, name, bases, attrs) -> type:
        """Enriches a class with logging, data storage, and closure 
        capabilities.
        """

        attrs['log'] = cls.log
        attrs['store'] = cls.store
        attrs['close'] = cls.close
        new_cls = super().__new__(cls, name, bases, attrs)

        return new_cls
    

    def __call__(self, *args, **kwargs) -> object:
        """Initializes an instance of a derived class within a 
        prototype-based design.
        """
        
        ProtoType.__init__(self)

        return super().__call__(*args, **kwargs)
    

    @classmethod
    def log(cls, message, stdout=True, write=True) -> None:
        """Records a log message with an optional display and storage 
        behavior.
        """

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        if write:
            ProtoType.data.log[timestamp] = message
        if stdout:
            print(f'{timestamp}: {message}')


    @classmethod
    def store(cls, name, value) -> None:
        """Stores a named value within the class's shared data store.
        """

        ProtoType.data.store[name] = value
    

    @classmethod
    def close(cls) -> None:
        """Finalizes operations by persistently storing class data.
        """

        namespace = MetaType.NAMESPACE
        pack = {
            f'{namespace}_dataclasses.json': ProtoType.data.classes,
            f'{namespace}_log.json': ProtoType.data.log,
            f'{namespace}_store.json': ProtoType.data.store,
        }
        for k, v in pack.items():
            if v:
                path = os.path.join(sys.modules['pytzen'].DIR, k)
                with open(path, 'w') as json_file:
                    json.dump(v, json_file, indent=4)



class ProtoType(metaclass=MetaType):
    """
    The `ProtoType` class serves as a foundational component in a 
    dynamic class creation and configuration management system, 
    leveraging a custom metaclass `MetaType` to control instantiation 
    behavior.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the `ProtoType` class, 
        orchestrated under the controlled instantiation behavior 
        enforced by the `MetaType` metaclass.
        """
        self.class_path = f'{self.__module__}.{self.__name__}'

        if not hasattr(ProtoType, 'config'):
            path = os.path.join(sys.modules['pytzen'].DIR, 'config.json')
            with open(path, 'r') as json_file:
                config = json.load(json_file)
            ProtoType.config = type('ConfigurationFile', (), config)

        if not hasattr(ProtoType, 'data'):
            ProtoType.data = SharedData()
        ProtoType.data.classes[self.class_path] = {
            'attributes': {},
            'methods': [k for k, v in self.__dict__.items() 
                        if callable(v) and '__' not in k],
        }
    

    def __setattr__(self, key, value) -> None:
        """
        Overrides the default behavior for setting attributes to ensure 
        that every new attribute added to an instance of `ProtoType` or 
        its derived classes is registered in a shared data structure.
        """

        setattr(ProtoType.data, key, value)
        attr_type = str(type(value).__name__)
        ProtoType.data.classes[self.class_path]\
            ['attributes'][key] = attr_type



@dataclass
class SharedData:
    """
    A data class for storing and managing shared pipeline information in 
    an immutable structure.
    """
    classes: dict = field(default_factory=dict)
    log: dict = field(default_factory=dict)
    store: dict = field(default_factory=dict)
    

    def __setattr__(self, key, value) -> None:
        """
        Overrides the default attribute setting behavior specifically to 
        enforce immutability for attributes once they have been set.
        """

        if hasattr(self, key):
            error = f"Attribute '{key}' already exists and cannot be changed."
            raise AttributeError(error)
        else:
            super().__setattr__(key, value)
