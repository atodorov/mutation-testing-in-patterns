class UrbanRoad(object):
    def __init__(self, speedLimit=50, *args, **kwargs):
        self.speedLimit = speedLimit

class RuralRoad(UrbanRoad):
    def __init__(self, speedLimit=90, *args, **kwargs):
        UrbanRoad.__init__(self, *args, **kwargs)

class BaseMotorway(object):
    def __init__(self, *args, **kwargs):
        self.minSpeed = 50

class Motorway(BaseMotorway):
    def __init__(self, speedLimit=130, *args, **kwargs):
        BaseMotorway.__init__(self, speedLimit, *args, **kwargs)
