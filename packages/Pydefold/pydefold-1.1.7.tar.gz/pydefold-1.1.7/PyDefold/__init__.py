
import pkgutil , importlib ,  os , collections
current_module_path = os.path.dirname(__file__)
result = dict()
for finder, name, ispkg in pkgutil.iter_modules([current_module_path]):
    full_module_name = f"{__name__}.{name}"
    pkg_lib = importlib.import_module(full_module_name)
    for elem in dir(pkg_lib) : 
        may_msg = pkg_lib.__getattribute__(elem)
        if type(may_msg).__name__ == 'MessageMeta' : 
            result[may_msg.__name__] = may_msg
Defold = collections.namedtuple('Defold' , result.keys() )(**result)

version="1.9.2-alpha"
bob=os.path.join(os.path.dirname(__file__),"bob-light.jar")
__all__ = ['Defold','version','bob']
