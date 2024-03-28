from collections import OrderedDict
from typing import Union

from acq4.devices.Camera import Camera
from acq4.util.Mutex import Mutex

WIDTH = 512
HEIGHT = 512


class TestCamera(Camera):
    def __init__(self, manager, config, name):
        self.camLock = Mutex()
        self.params = OrderedDict(
            [
                ("triggerMode", "Normal"),
                ("exposure", 0.001),
                # ("binning", (1, 1)),
                # ("region", (0, 0, WIDTH, WIDTH)),
                ("binningX", 1),
                ("binningY", 1),
                ("regionX", 0),
                ("regionY", 0),
                ("regionW", WIDTH),
                ("regionH", HEIGHT),
                ("gain", 1.0),
                ("sensorSize", (WIDTH, HEIGHT)),
                ("bitDepth", 16),
            ]
        )

        self.paramRanges = OrderedDict(
            [
                ("triggerMode", (["Normal", "TriggerStart"], True, True, [])),
                ("exposure", ((0.001, 10.0), True, True, [])),
                # ("binning", ([range(1, 10), range(1, 10)], True, True, [])),
                # ("region", ([(0, WIDTH - 1), (0, HEIGHT - 1), (1, WIDTH), (1, HEIGHT)], True, True, [])),
                ("binningX", (list(range(1, 10)), True, True, [])),
                ("binningY", (list(range(1, 10)), True, True, [])),
                ("regionX", ((0, WIDTH - 1), True, True, ["regionW"])),
                ("regionY", ((0, HEIGHT - 1), True, True, ["regionH"])),
                ("regionW", ((1, WIDTH), True, True, ["regionX"])),
                ("regionH", ((1, HEIGHT), True, True, ["regionY"])),
                ("gain", ((0.1, 10.0), True, True, [])),
                ("sensorSize", (None, False, True, [])),
                ("bitDepth", (None, False, True, [])),
            ]
        )

        self.groupParams = {
            "binning": ("binningX", "binningY"),
            "region": ("regionX", "regionY", "regionW", "regionH"),
        }


        Camera.__init__(self, manager, config, name)  # superclass will call setupCamera when it is ready.

    def setupCamera(self):
        pass

    def globalTransformChanged(self):
        pass

    def startCamera(self):
        pass

    def stopCamera(self):
        pass


    def newFrames(self):
        """Return a list of all frames acquired since the last call to newFrames."""
        return []

    def quit(self):
        pass

    def listParams(self, params: Union[list, str, None] = None):
        """List properties of specified parameter(s), or of all parameters if None"""
        if params is None:
            return self.paramRanges
        if isinstance(params, str):
            return self.paramRanges[params]

        return {k: self.paramRanges[k] for k in params}

    def setParams(self, params, autoRestart=True, autoCorrect=True):
        dp = []
        ap = {}
        for k in params:
            if k in self.groupParams:
                ap.update(dict(zip(self.groupParams[k], params[k])))
                dp.append(k)
        params.update(ap)
        for k in dp:
            del params[k]

        self.params.update(params)
        newVals = params
        restart = True
        if autoRestart and restart:
            self.restart()
        self.sigParamsChanged.emit(newVals)
        return (newVals, restart)

    def getParams(self, params=None):
        if params is None:
            params = list(self.listParams().keys())
        vals = OrderedDict()
        for k in params:
            if k in self.groupParams:
                vals[k] = list(self.getParams(self.groupParams[k]).values())
            else:
                vals[k] = self.params[k]
        return vals

    def setParam(self, param, value, autoRestart=True, autoCorrect=True):
        return self.setParams({param: value}, autoRestart=autoRestart, autoCorrect=autoCorrect)

    def getParam(self, param):
        return self.getParams([param])[param]

    def createTask(self, cmd, parentTask):
        pass