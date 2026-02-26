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
        def __init__(self, name, cost, quantity, image, image_hover, slot, rarity, buff=None):
            Item.__init__(self, name, cost, quantity, image, image_hover)
            self.slot = slot
            self.rarity = rarity
            self.buff = buff

    class Weapon(Equippable):
        def __init__(self, name, cost, quantity, image, image_hover, slot, rarity, element, buff=None):
            Equippable.__init__(self, name, cost, quantity, image, image_hover, slot, rarity, buff)
            self.element = element
            
    class Armor(Equippable):
        def __init__(self, name, cost, quantity, image, image_hover, slot, rarity, resistance, weakness, buff=None):
            Equippable.__init__(self, name, cost, quantity, image, image_hover, slot, rarity, buff)
            self.resistance = resistance
            self.weakness = weakness

    class Accessory(Equippable):
        def __init__(self, name, cost, quantity, image, image_hover, slot, rarity, buff):
            Equippable.__init__(self, name, cost, quantity, image, image_hover, slot, rarity, buff= None)

    class Lootbox(Item):
        def __init__(self, name, cost, quantity, image, image_hover, content, clickable=True):
            Item.__init__(self, name, cost, quantity, image, image_hover)
            self.content = content
            self.clickable = clickable


# Define Items
default documents = Item("documents", 0, 1, "images/inventory/documents.png", "images/inventory/documents_hover.png")
default guild_certificate = Item("guild certificate", 0, 1, "images/inventory/guild_certificate.png", "images/inventory/guild_certificate_hover.png")

# Define Weapons
default iron_sword = Weapon("sword", 10, 1, "images/inventory/sword.png", "images/inventory/sword_hover.png", "weapon", "common",[])

# Define Armors
default iron_armor = Armor("armor", 20, 1, "images/inventory/armor.png", "images/inventory/armor_hover.png", "armor", "common", [], [])

# Define Accessories --> for buff use {"attack_bonus_flat": 5, "attack_bonus_dice": "1d4", "attack_multiplier": 1.5, "max_hp": 10}


# Define Lootboxes
default follower_lootbox = Lootbox("follower lootbox", 100, 1, "images/lootboxes/lootbox_follower.png", "images/lootboxes/lootbox_follower_hover.png", "follower")
default armor_lootbox = Lootbox("armor lootbox", 25, 1, "images/lootboxes/lootbox_armor.png", "images/lootboxes/lootbox_armor_hover.png", "armor")
default weapon_lootbox = Lootbox("weapon lootbox", 25, 1, "images/lootboxes/lootbox_weapon.png", "images/lootboxes/lootbox_weapon_hover.png", "weapon")
default accessory_lootbox = Lootbox("accessory lootbox", 50, 1, "images/lootboxes/lootbox_accessory.png", "images/lootboxes/lootbox_accessory_hover.png", "accessory")