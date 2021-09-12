from triggers.triggerFunction import TriggerFunction

class Trigger:
    def __init__(self, triggerObject: TriggerFunction, once: bool = True) -> None:
        self.triggerObject = triggerObject
        self.once = once