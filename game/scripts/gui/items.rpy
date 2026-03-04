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
        def __init__(self, name, cost, quantity, image, image_hover, rarity, buff=None):
            Item.__init__(self, name, cost, quantity, image, image_hover)
            self.rarity = rarity
            self.buff = buff

    class Weapon(Equippable):
        def __init__(self, name, cost, quantity, image, image_hover, rarity, element, buff=None):
            Equippable.__init__(self, name, cost, quantity, image, image_hover, rarity, buff)
            self.element = element
            
    class Armor(Equippable):
        def __init__(self, name, cost, quantity, image, image_hover, rarity, resistance, weakness, buff=None):
            Equippable.__init__(self, name, cost, quantity, image, image_hover, rarity, buff)
            self.resistance = resistance
            self.weakness = weakness

    class Accessory(Equippable):
        def __init__(self, name, cost, quantity, image, image_hover, rarity, buff):
            Equippable.__init__(self, name, cost, quantity, image, image_hover, rarity, buff)

    class Lootbox(Item):
        def __init__(self, name, cost, quantity, image, image_hover, content, clickable=True):
            Item.__init__(self, name, cost, quantity, image, image_hover)
            self.content = content
            self.clickable = clickable


# Define Items
default documents = Item("documents", 0, 1, "images/inventory/item/documents.png", "images/inventory/item/documents_hover.png")
default guild_certificate = Item("guild certificate", 0, 1, "images/inventory/item/guild_certificate.png", "images/inventory/item/guild_certificate_hover.png")


# Define Weapons
default dagger = Weapon("dagger", 10, 1, "images/inventory/weapon/dagger_idle.png", "images/inventory/weapon/dagger_hover.png", "common", [], {})
default iron_sword = Weapon("iron sword", 15, 1, "images/inventory/weapon/iron_sword_idle.png", "images/inventory/weapon/iron_sword_hover.png", "common", ["Iron"], {"attack_bonus_flat": 1})
default rapier = Weapon("rapier", 25, 1, "images/inventory/weapon/rapier_idle.png", "images/inventory/weapon/rapier_hover.png", "common", ["Iron"], {})
default halberd = Weapon("halberd", 25, 1, "images/inventory/weapon/halberd_idle.png", "images/inventory/weapon/halberd_hover.png", "common", [], {"attack_bonus_flat": 1})
default morningstar = Weapon("morningstar", 25, 1, "images/inventory/weapon/morningstar_idle.png", "images/inventory/weapon/morningstar_hover.png", "common", ["Iron"], {"attack_multiplier": 1.1})

default longsword = Weapon("longsword", 45, 1, "images/inventory/weapon/longsword_idle.png", "images/inventory/weapon/longsword_hover.png", "rare", ["Iron"], {"attack_bonus_flat": 1})
default shuriken = Weapon("shuriken", 30, 1, "images/inventory/weapon/shuriken_idle.png", "images/inventory/weapon/shuriken_hover.png", "rare", ["Force"], {"attack_bonus_flat": 2})
default corrupt_edge = Weapon("corrupt edge", 50, 1, "images/inventory/weapon/corrupt_edge_idle.png", "images/inventory/weapon/corrupt_edge_hover.png", "rare", ["Acid"], {"attack_bonus_flat": 2})
default silence = Weapon("silence", 45, 1, "images/inventory/weapon/silence_idle.png", "images/inventory/weapon/silence_hover.png", "rare", ["Psychic"], {})
default mystic_blade = Weapon("mystic blade", 75, 1, "images/inventory/weapon/mystic_blade_idle.png", "images/inventory/weapon/mystic_blade_hover.png", "rare", ["Spectral"], {"attack_bonus_flat": 2})

default dream_shatter = Weapon("dream shatter", 100, 1, "images/inventory/weapon/dream_shatter_idle.png", "images/inventory/weapon/dream_shatter_hover.png", "epic", ["Dream"], {"attack_multiplier": 1.2})
default ice_bane = Weapon("ice bane", 85, 1, "images/inventory/weapon/ice_bane_idle.png", "images/inventory/weapon/ice_bane_hover.png", "epic", ["Ice", "Water"], {"attack_bonus_dice": "1d4"})
default dawn_bringer = Weapon("dawn bringer", 110, 1, "images/inventory/weapon/dawn_bringer_idle.png", "images/inventory/weapon/dawn_bringer_hover.png", "epic", ["Holy"], {"attack_bonus_flat": 3})
default flame_sword = Weapon("flame sword", 90, 1, "images/inventory/weapon/flame_sword_idle.png", "images/inventory/weapon/flame_sword_hover.png", "epic", ["Fire"], {})

default the_siphoner = Weapon("the siphoner", 200, 1, "images/inventory/weapon/the_siphoner_idle.png", "images/inventory/weapon/the_siphoner_hover.png", "legendary", [], {"attack_multiplier": 2})
default hell_reaver = Weapon("hell reaver", 250, 1, "images/inventory/weapon/hell_reaver_idle.png", "images/inventory/weapon/hell_reaver_hover.png", "legendary", ["Fire", "Ice", "Necrotic"], {"attack_bonus_dice": "1d6"})
default heaven_slayer = Weapon("heaven slayer", 250, 1, "images/inventory/weapon/heaven_slayer_idle.png", "images/inventory/weapon/heaven_slayer_hover.png", "legendary", ["Holy", "Psychic", "Force"], {"attack_bonus_dice": "1d6"})

default kingly_redemption = Weapon("kingly redemption", 1000, 1, "images/inventory/weapon/kingly_redemption_idle.png", "images/inventory/weapon/kingly_redemption_hover.png", "unique", ["Acid", "Water", "Psychic", "Holy", "Fire"], {"attack_bonus_flat": 10})


# Define Armors
default copper_armor = Armor("copper armor", 10, 1, "images/inventory/armor/copper_armor_idle.png", "images/inventory/armor/copper_armor_hover.png", "common", [], [], {"max_hp": 1})
default iron_armor = Armor("iron armor", 15, 1, "images/inventory/armor/iron_armor_idle.png", "images/inventory/armor/iron_armor_hover.png", "common", ["Iron"], ["Fire"], {"max_hp": 1})
default silver_armor = Armor("silver armor", 20, 1, "images/inventory/armor/silver_armor_idle.png", "images/inventory/armor/silver_armor_hover.png", "common", ["Earth"], ["Acid"], {})
default gold_armor = Armor("gold armor", 25, 1, "images/inventory/armor/gold_armor_idle.png", "images/inventory/armor/gold_armor_hover.png", "common", ["Spectral"], [], {})
default platinum_armor = Armor("platinum armor", 30, 1, "images/inventory/armor/platinum_armor_idle.png", "images/inventory/armor/platinum_armor_hover.png", "common", ["Necrotic"], ["Dream"], {})

default dragon_bane = Armor("dragon bane", 45, 1, "images/inventory/armor/dragon_bane_idle.png", "images/inventory/armor/dragon_bane_hover.png", "rare", ["Fire"], [], {"max_hp": 2})
default undead_bane = Armor("undead bane", 40, 1, "images/inventory/armor/undead_bane_idle.png", "images/inventory/armor/undead_bane_hover.png", "rare", ["Necrotic"], ["Holy"], {"max_hp": 1})
default warrior_bane = Armor("warrior bane", 35, 1, "images/inventory/armor/warrior_bane_idle.png", "images/inventory/armor/warrior_bane_hover.png", "rare", ["Force", "Iron", "Fire"], ["Acid", "Psychic"], {"max_hp": 1})
default slime_bane = Armor("slime bane", 30, 1, "images/inventory/armor/slime_bane_idle.png", "images/inventory/armor/slime_bane_hover.png", "rare", ["Water", "Acid"], ["Fire", "Ice", "Force"], {"max_hp": 2})
default silent_life = Armor("silent life", 45, 1, "images/inventory/armor/silent_life_idle.png", "images/inventory/armor/silent_life_hover.png", "rare", [], [], {"max_hp": 3})

default heavens_curse = Armor("heaven's curse", 100, 1, "images/inventory/armor/heavens_curse_idle.png", "images/inventory/armor/heavens_curse_hover.png", "epic", ["Holy"], ["Necrotic"], {"max_hp": 2})
default hells_redemption = Armor("hell's redemption", 100, 1, "images/inventory/armor/hells_redemption_idle.png", "images/inventory/armor/hells_redemption_hover.png", "epic", ["Fire", "Ice", "Necrotic"], ["Holy"], {"max_hp": 2})
default elemental_master = Armor("elemental master", 110, 1, "images/inventory/armor/elemental_master_idle.png", "images/inventory/armor/elemental_master_hover.png", "epic", ["Fire", "Ice", "Stone", "Water", "Earth"], [], {})
default pride = Armor("pride", 200, 1, "images/inventory/armor/pride_idle.png", "images/inventory/armor/pride_hover.png", "epic", [], [], {})

default lifeline = Armor("lifeline", 250, 1, "images/inventory/armor/lifeline_idle.png", "images/inventory/armor/lifeline_hover.png", "legendary", [], [], {"max_hp": 5})
default invisible_barrier = Armor("invisible barrier", 250, 1, "images/inventory/armor/invisible_barrier_idle.png", "images/inventory/armor/invisible_barrier_hover.png", "legendary", ["Psychic", "Dream", "Spectral", "Force"], ["Iron"], {"max_hp": 3})
default realm_holder = Armor("realm holder", 250, 1, "images/inventory/armor/realm_holder_idle.png", "images/inventory/armor/realm_holder_hover.png", "legendary", ["Holy", "Nectoric"], [], {"max_hp": 3})

default aetherium_armor = Armor("aetherium armor", 1000, 1, "images/inventory/armor/aetherium_armor_idle.png", "images/inventory/armor/aetherium_armor_hover.png", "unique", ["Fire", "Ice", "Acid", "Necrotic", "Holy", "Psychic", "Force", "Earth", "Water", "Stone", "Spectral", "Dream", "Plant", "Iron"], [], {"max_hp": 10})


# Define Accessories
default copper_ring = Accessory("copper ring", 10, 1, "images/inventory/accessory/copper_ring_idle.png", "images/inventory/accessory/copper_ring_hover.png", "common", {})
default iron_bracelet = Accessory("iron bracelet", 10, 1, "images/inventory/accessory/iron_bracelet_idle.png", "images/inventory/accessory/iron_bracelet_hover.png", "common", {"attack_bonus_flat": 1})
default silver_necklace = Accessory("silver necklace", 15, 1, "images/inventory/accessory/silver_necklace_idle.png", "images/inventory/accessory/silver_necklace_hover.png", "common", {"max_hp": 1})
default gold_charm = Accessory("gold charm", 20, 1, "images/inventory/accessory/gold_charm_idle.png", "images/inventory/accessory/gold_charm_hover.png", "common", {"attack_bonus_flat": 1})
default platinum_chain = Accessory("platinum chain", 25, 1, "images/inventory/accessory/platinum_chain_idle.png", "images/inventory/accessory/platinum_chain_hover.png", "common", {"max_hp": 1})

default topas_pendant = Accessory("topas pendant", 30, 1, "images/inventory/accessory/topas_pendant_idle.png", "images/inventory/accessory/topas_pendant_hover.png", "rare", {"attack_bonus_flat": 2})
default ruby_pendant = Accessory("ruby pendant", 30, 1, "images/inventory/accessory/ruby_pendant_idle.png", "images/inventory/accessory/ruby_pendant_hover.png", "rare", {"max_hp": 2})
default emerald_pendant = Accessory("emerald pendant", 30, 1, "images/inventory/accessory/emerald_pendant_idle.png", "images/inventory/accessory/emerald_pendant_hover.png", "rare", {"attack_bonus_flat": 1, "max_hp": 1})
default sapphire_pendant = Accessory("sapphire pendant", 30, 1, "images/inventory/accessory/sapphire_pendant_idle.png", "images/inventory/accessory/sapphire_pendant_hover.png", "rare", {"attack_bonus_flat": 2, "max_hp": 1})
default diamond_pendant = Accessory("diamond pendant", 40, 1, "images/inventory/accessory/diamond_pendant_idle.png", "images/inventory/accessory/diamond_pendant_hover.png", "rare", {"max_hp": 3})

default ring_of_defense = Accessory("ring of defense", 75, 1, "images/inventory/accessory/ring_of_defense_idle.png", "images/inventory/accessory/ring_of_defense_hover.png", "epic", {"defence": True})
default sharpness_chian = Accessory("sharpness chian", 100, 1, "images/inventory/accessory/sharpness_chain_idle.png", "images/inventory/accessory/sharpness_chain_hover.png", "epic", {"attack_multiplier": 1.5})
default armored_charm = Accessory("armored charm", 100, 1, "images/inventory/accessory/armored_charm_idle.png", "images/inventory/accessory/armored_charm_hover.png", "epic", {"max_hp": 3, "attack_bonus_flat": 1})
default monocole_of_perserverance = Accessory("monocole of perserverance", 100, 1, "images/inventory/accessory/monocole_of_perserverance_idle.png", "images/inventory/accessory/monocole_of_perserverance_hover.png", "epic", {"max_hp": 4})

default chain_of_heroes = Accessory("chain of heroes", 200, 1, "images/inventory/accessory/chain_of_heroes_idle.png", "images/inventory/accessory/chain_of_heroes_hover.png", "legendary", {"attack_bonus_dice": "1d6"})
default twin_rings = Accessory("twin rings", 250, 1, "images/inventory/accessory/twin_rings_idle.png", "images/inventory/accessory/twin_rings_hover.png", "legendary", {"attack_bonus_flat": 4, "max_hp": 4})
default broken_crown = Accessory("broken crown", 200, 1, "images/inventory/accessory/broken_crown_idle.png", "images/inventory/accessory/broken_crown_hover.png", "legendary", {"max_hp": 5})

default void_necklace = Accessory("void necklace", 1000, 1, "images/inventory/accessory/void_necklace_idle.png", "images/inventory/accessory/void_necklace_hover.png", "unique", {"attack_multiplier": 2, "max_hp": 10})


# Define Lootboxes
default follower_lootbox = Lootbox("follower lootbox", 250, 1, "images/lootboxes/lootbox_follower.png", "images/lootboxes/lootbox_follower_hover.png", "follower")
default armor_lootbox = Lootbox("armor lootbox", 100, 1, "images/lootboxes/lootbox_armor.png", "images/lootboxes/lootbox_armor_hover.png", "armor")
default weapon_lootbox = Lootbox("weapon lootbox", 100, 1, "images/lootboxes/lootbox_weapon.png", "images/lootboxes/lootbox_weapon_hover.png", "weapon")
default accessory_lootbox = Lootbox("accessory lootbox", 100, 1, "images/lootboxes/lootbox_accessory.png", "images/lootboxes/lootbox_accessory_hover.png", "accessory")