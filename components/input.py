class Input:
    def __init__(self) -> None:
        self.Up: bool = False
        self.Down: bool = False
        self.Left: bool = False
        self.Right: bool = False
        self.UpLeft: bool = False
        self.UpRight: bool = False
        self.DownLeft: bool = False
        self.DownRight: bool = False
        self.Wait: bool = False
        self.Escape: bool = False
        
        self.Debug: bool = False
        self.DebugKey: int = -1

    def clear(self):
        self.Up = False
        self.Down = False
        self.Left = False
        self.Right = False
        self.UpLeft = False
        self.UpRight = False
        self.DownLeft = False
        self.DownRight = False
        self.Wait = False
        self.Escape = False
        self.Debug = False
        self.DebugKey = -1