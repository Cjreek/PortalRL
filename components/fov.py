class FOV:
    def __init__(self, viewDistance: int) -> None:
        self.viewDistance = viewDistance
        self.fov = []
        self.lightFov = []
        self.dirty = True

    def isVisible(self, x: int, y: int):
        return self.fov[x, y]