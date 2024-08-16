
from .engine import * 
from .ddf import * 
from .script import * 
from .particle_ddf_pb2 import Emitter,Modifier,ParticleFX,SplinePoint 
from .gameobject import * 
from .resource import * 
from .graphics import * 
from .input_ddf_pb2 import GamepadMap,GamepadMapEntry,GamepadMaps,GamepadModifier_t,GamepadTrigger,InputBinding,KeyTrigger,MouseTrigger,TextTrigger,TouchTrigger 
from .render import * 
from .gamesys import * 
from .rig_ddf_pb2 import AnimationInstanceDesc,AnimationSet,AnimationSetDesc,AnimationTrack,Bone,EventKey,EventTrack,IK,Mesh,MeshSet,Model,RigAnimation,RigScene,Skeleton 

version="1.9.2-alpha"

import importlib , pkgutil , collections , os 
class TypesGenerator : 
    def getDefoldTypes(self) : 
        result = dict()
        pkg_lib = importlib.import_module('PyDefold')
        for elem in dir(pkg_lib) : 
            may_msg = pkg_lib.__getattribute__(elem)
            if type(may_msg).__name__ == 'MessageMeta' : 
                result[may_msg.__name__] = may_msg
        return collections.namedtuple('Defold' , result.keys() )(**result)
Defold = TypesGenerator().getDefoldTypes()
Bob=os.path.join(os.path.dirname(__file__),"bob-light.jar")
########
__all__ = ['Defold','version','bob']
