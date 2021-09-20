class Position:
    def __init__(self, x: int, y: int) -> None:
        self.__x = x
        self.__y = y
        self.__changed = False

    @property
    def changed(self):
        return self.__changed

    def getX(self) -> int:
        return self.__x

    def setX(self, value: int):
        if self.__x != value:
            self.__x = value
            self.__changed = True

    def getY(self) -> int:
        return self.__y

    def setY(self, value: int):
        if self.__y != value:
            self.__y = value
            self.__changed = True
    
    def setDirty(self, dirty: bool):
        self.__changed = dirty

    X = property(getX, setX)
    Y = property(getY, setY)