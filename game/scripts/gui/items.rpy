init python:
    import copy

    # --- Item Classes ---
    class Item():
        def __init__(self, name, cost, quantity, image, image_hover):
            self.name = name
            self.quantity = quantity 
            self.cost = cost  
            self.image = image    
            self.image_hover = image_hover
            self.is_equipped = False # Helper flag

    class Equippable(Item):
        def __init__(self, name, cost, quantity, image, image_hover, slot, buff=None):
            Item.__init__(self, name, cost, quantity, image, image_hover)
            self.slot = slot
            self.buff = buff

    class Weapon(Equippable):
        def __init__(self, name, cost, quantity, image, image_hover, slot, element, buff=None):
            Equippable.__init__(self, name, cost, quantity, image, image_hover, slot, buff)
            self.element = element
            
    class Armor(Equippable):
        def __init__(self, name, cost, quantity, image, image_hover, slot, resistance, weakness, buff=None):
            Equippable.__init__(self, name, cost, quantity, image, image_hover, slot, buff)
            self.resistance = resistance
            self.weakness = weakness


    class Accessory(Equippable):
        def __init__(self, name, cost, quantity, image, image_hover, slot, buff):
            Equippable.__init__(self, name, cost, quantity, image, image_hover, slot, buff)

# Define Items
default documents = Item("documents", 0, 1, "images/inventory/documents.png", "images/inventory/documents_hover.png")
default guild_certificate = Item("guild certificate", 0, 1, "images/inventory/guild_certificate.png", "images/inventory/guild_certificate_hover.png")

# Define Weapons
default iron_sword = Weapon("sword", 10, 1, "images/inventory/sword.png", "images/inventory/sword_hover.png", "weapon", [])

# Define Armors
default iron_armor = Armor("armor", 20, 1, "images/inventory/armor.png", "images/inventory/armor_hover.png", "armor", [], [])

# Define Accessories --> for buff use {"atk": 5, "max_hp": 10}