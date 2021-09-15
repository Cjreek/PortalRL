from enum import IntEnum

class EquipmentSlot(IntEnum):
    NONE = -1,
    HEAD = 0,
    BODY = 1,
    FEET = 2,
    MAINHAND = 3,
    OFFHAND = 4

    @property
    def displayName(self):
        __displayValues = {
            EquipmentSlot.NONE: "",
            EquipmentSlot.HEAD: "Head",
            EquipmentSlot.BODY: "Body",
            EquipmentSlot.FEET: "Feet",
            EquipmentSlot.MAINHAND: "Weapon",
            EquipmentSlot.OFFHAND: "Shield"
        }
        return __displayValues[self.value]