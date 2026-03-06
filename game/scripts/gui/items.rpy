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
        def __init__(self, name, cost, quantity, image, image_hover, rarity, buff=None, lootable=True):
            Item.__init__(self, name, cost, quantity, image, image_hover)
            self.rarity = rarity
            self.buff = buff
            self.lootable = lootable

    class Weapon(Equippable):
        def __init__(self, name, cost, quantity, image, image_hover, rarity, element, buff=None, lootable=True):
            Equippable.__init__(self, name, cost, quantity, image, image_hover, rarity, buff, lootable)
            self.element = element
            
    class Armor(Equippable):
        def __init__(self, name, cost, quantity, image, image_hover, rarity, resistance, weakness, buff=None, lootable=True):
            Equippable.__init__(self, name, cost, quantity, image, image_hover, rarity, buff, lootable)
            self.resistance = resistance
            self.weakness = weakness

    class Accessory(Equippable):
        def __init__(self, name, cost, quantity, image, image_hover, rarity, buff, lootable=True):
            Equippable.__init__(self, name, cost, quantity, image, image_hover, rarity, buff, lootable)

    class Lootbox(Item):
        def __init__(self, name, cost, quantity, image, image_hover, content, clickable=True):
            Item.__init__(self, name, cost, quantity, image, image_hover)
            self.content = content
            self.clickable = clickable

    # --- Loot Table Generation ---
    # This dictionary will hold all lootable items, sorted by type and rarity.
    loot_tables = {
        "weapon": {"common": [], "rare": [], "epic": [], "legendary": [], "unique": []},
        "armor": {"common": [], "rare": [], "epic": [], "legendary": [], "unique": []},
        "accessory": {"common": [], "rare": [], "epic": [], "legendary": [], "unique": []},
        "follower": {"common": [], "rare": [], "epic": [], "legendary": [], "unique": []}
    }

    def populate_loot_tables():
        """
        Iterates through all defined items and followers in the Ren'Py store
        and adds them to the loot_tables if they are 'lootable'.
        """
        # Clear existing tables to avoid duplicates
        for type_key in loot_tables:
            for rarity_key in loot_tables[type_key]:
                loot_tables[type_key][rarity_key] = []

        item_map = {
            Weapon: "weapon",
            Armor: "armor",
            Accessory: "accessory"
        }
        for item in renpy.store.__dict__.values():
            for item_class, item_type in item_map.items():
                if isinstance(item, item_class) and getattr(item, 'lootable', False):
                    if hasattr(item, 'rarity') and item.rarity in loot_tables[item_type]:
                        loot_tables[item_type][item.rarity].append(item)
                    # Once type is found, move to the next item in the store
                    break

        # Populate followers from the all_followers list (defined in follower.rpy)
        if 'all_followers' in renpy.store.__dict__:
            for follower in renpy.store.all_followers:
                # We check for lootable and also that it's not the dummy follower
                if getattr(follower, 'lootable', False) and follower.name != "":
                    if hasattr(follower, 'rarity') and follower.rarity in loot_tables["follower"]:
                        loot_tables["follower"][follower.rarity].append(follower)


# Define Items
default documents = Item("Documents", 0, 1, "images/inventory/item/documents.png", "images/inventory/item/documents_hover.png")
default guild_certificate = Item("Guild Certificate", 0, 1, "images/inventory/item/guild_certificate.png", "images/inventory/item/guild_certificate_hover.png")


# Define Weapons
default dagger = Weapon("Dagger", 10, 1, "images/inventory/weapon/dagger_idle.png", "images/inventory/weapon/dagger_hover.png", "common", [], {})
default iron_sword = Weapon("Iron Sword", 15, 1, "images/inventory/weapon/iron_sword_idle.png", "images/inventory/weapon/iron_sword_hover.png", "common", ["Iron"], {"attack_bonus_flat": 1})
default rapier = Weapon("Rapier", 25, 1, "images/inventory/weapon/rapier_idle.png", "images/inventory/weapon/rapier_hover.png", "common", ["Iron"], {})
default halberd = Weapon("Halberd", 25, 1, "images/inventory/weapon/halberd_idle.png", "images/inventory/weapon/halberd_hover.png", "common", [], {"attack_bonus_flat": 1})
default morningstar = Weapon("Morningstar", 25, 1, "images/inventory/weapon/morningstar_idle.png", "images/inventory/weapon/morningstar_hover.png", "common", ["Iron"], {"attack_multiplier": 1.1})

default longsword = Weapon("Longsword", 45, 1, "images/inventory/weapon/long_sword_idle.png", "images/inventory/weapon/long_sword_hover.png", "rare", ["Iron"], {"attack_bonus_flat": 1})
default shuriken = Weapon("Shuriken", 30, 1, "images/inventory/weapon/shuriken_idle.png", "images/inventory/weapon/shuriken_hover.png", "rare", ["Force"], {"attack_bonus_flat": 2})
default corrupt_edge = Weapon("Corrupt Edge", 50, 1, "images/inventory/weapon/corrupt_edge_idle.png", "images/inventory/weapon/corrupt_edge_hover.png", "rare", ["Acid"], {"attack_bonus_flat": 2})
default silence = Weapon("Silence", 45, 1, "images/inventory/weapon/silence_idle.png", "images/inventory/weapon/silence_hover.png", "rare", ["Psychic"], {})
default mystic_blade = Weapon("Mystic Blade", 75, 1, "images/inventory/weapon/mystic_blade_idle.png", "images/inventory/weapon/mystic_blade_hover.png", "rare", ["Spectral"], {"attack_bonus_flat": 2})

default dream_shatter = Weapon("Dream Shatter", 100, 1, "images/inventory/weapon/dream_shatter_idle.png", "images/inventory/weapon/dream_shatter_hover.png", "epic", ["Dream"], {"attack_multiplier": 1.2})
default ice_bane = Weapon("Ice Bane", 85, 1, "images/inventory/weapon/ice_bane_idle.png", "images/inventory/weapon/ice_bane_hover.png", "epic", ["Ice", "Water"], {"attack_bonus_dice": "1d4"})
default dawn_bringer = Weapon("Dawn Bringer", 110, 1, "images/inventory/weapon/dawn_bringer_idle.png", "images/inventory/weapon/dawn_bringer_hover.png", "epic", ["Holy"], {"attack_bonus_flat": 3})
default flame_sword = Weapon("Flame Sword", 90, 1, "images/inventory/weapon/flame_sword_idle.png", "images/inventory/weapon/flame_sword_hover.png", "epic", ["Fire"], {})

default the_siphoner = Weapon("The Siphoner", 200, 1, "images/inventory/weapon/the_siphoner_idle.png", "images/inventory/weapon/the_siphoner_hover.png", "legendary", [], {"attack_multiplier": 2})
default hell_reaver = Weapon("Hell Reaver", 250, 1, "images/inventory/weapon/hell_reaver_idle.png", "images/inventory/weapon/hell_reaver_hover.png", "legendary", ["Fire", "Ice", "Necrotic"], {"attack_bonus_dice": "1d6"})
default heaven_slayer = Weapon("Heaven Slayer", 250, 1, "images/inventory/weapon/heaven_slayer_idle.png", "images/inventory/weapon/heaven_slayer_hover.png", "legendary", ["Holy", "Psychic", "Force"], {"attack_bonus_dice": "1d6"})

default kingly_redemption = Weapon("Kingly Redemption", 1000, 1, "images/inventory/weapon/kingly_redemption_idle.png", "images/inventory/weapon/kingly_redemption_hover.png", "unique", ["Acid", "Water", "Psychic", "Holy", "Fire"], {"attack_bonus_flat": 10})


# Define Armors
default copper_armor = Armor("Copper Armor", 10, 1, "images/inventory/armor/copper_armor_idle.png", "images/inventory/armor/copper_armor_hover.png", "common", [], [], {"max_hp": 1})
default iron_armor = Armor("Iron Armor", 15, 1, "images/inventory/armor/iron_armor_idle.png", "images/inventory/armor/iron_armor_hover.png", "common", ["Iron"], ["Fire"], {"max_hp": 1})
default silver_armor = Armor("Silver Armor", 20, 1, "images/inventory/armor/silver_armor_idle.png", "images/inventory/armor/silver_armor_hover.png", "common", ["Earth"], ["Acid"], {})
default gold_armor = Armor("Gold Armor", 25, 1, "images/inventory/armor/gold_armor_idle.png", "images/inventory/armor/gold_armor_hover.png", "common", ["Spectral"], [], {})
default platinum_armor = Armor("Platinum Armor", 30, 1, "images/inventory/armor/platinum_armor_idle.png", "images/inventory/armor/platinum_armor_hover.png", "common", ["Necrotic"], ["Dream"], {})

default dragon_bane = Armor("Dragon Bane", 45, 1, "images/inventory/armor/dragon_bane_idle.png", "images/inventory/armor/dragon_bane_hover.png", "rare", ["Fire"], [], {"max_hp": 2})
default undead_bane = Armor("Undead Bane", 40, 1, "images/inventory/armor/undead_bane_idle.png", "images/inventory/armor/undead_bane_hover.png", "rare", ["Necrotic"], ["Holy"], {"max_hp": 1})
default warrior_bane = Armor("Warrior Bane", 35, 1, "images/inventory/armor/warrior_bane_idle.png", "images/inventory/armor/warrior_bane_hover.png", "rare", ["Force", "Iron", "Fire"], ["Acid", "Psychic"], {"max_hp": 1})
default slime_bane = Armor("Slime Bane", 30, 1, "images/inventory/armor/slime_bane_idle.png", "images/inventory/armor/slime_bane_hover.png", "rare", ["Water", "Acid"], ["Fire", "Ice", "Force"], {"max_hp": 2})
default silent_life = Armor("Silent Life", 45, 1, "images/inventory/armor/silent_life_idle.png", "images/inventory/armor/silent_life_hover.png", "rare", [], [], {"max_hp": 3})

default heavens_curse = Armor("Heaven's Curse", 100, 1, "images/inventory/armor/heavens_curse_idle.png", "images/inventory/armor/heavens_curse_hover.png", "epic", ["Holy"], ["Necrotic"], {"max_hp": 2})
default hells_redemption = Armor("Hell's Redemption", 100, 1, "images/inventory/armor/hells_redemption_idle.png", "images/inventory/armor/hells_redemption_hover.png", "epic", ["Fire", "Ice", "Necrotic"], ["Holy"], {"max_hp": 2})
default elemental_master = Armor("Elemental Master", 110, 1, "images/inventory/armor/elemental_master_idle.png", "images/inventory/armor/elemental_master_hover.png", "epic", ["Fire", "Ice", "Stone", "Water", "Earth"], [], {})
default pride = Armor("Pride", 200, 1, "images/inventory/armor/pride_idle.png", "images/inventory/armor/pride_hover.png", "epic", [], [], {})

default lifeline = Armor("Lifeline", 250, 1, "images/inventory/armor/lifeline_idle.png", "images/inventory/armor/lifeline_hover.png", "legendary", [], [], {"max_hp": 5})
default invisible_barrier = Armor("Invisible Barrier", 250, 1, "images/inventory/armor/invisible_barrier_idle.png", "images/inventory/armor/invisible_barrier_hover.png", "legendary", ["Psychic", "Dream", "Spectral", "Force"], ["Iron"], {"max_hp": 3})
default realm_holder = Armor("Realm Holder", 250, 1, "images/inventory/armor/realm_holder_idle.png", "images/inventory/armor/realm_holder_hover.png", "legendary", ["Holy", "Necrotic"], [], {"max_hp": 3})

default aetherium_armor = Armor("Aetherium Armor", 1000, 1, "images/inventory/armor/aetherium_armor_idle.png", "images/inventory/armor/aetherium_armor_hover.png", "unique", ["Fire", "Ice", "Acid", "Necrotic", "Holy", "Psychic", "Force", "Earth", "Water", "Stone", "Spectral", "Dream", "Plant", "Iron"], [], {"max_hp": 10})


# Define Accessories
default copper_ring = Accessory("Copper Ring", 10, 1, "images/inventory/accessory/copper_ring_idle.png", "images/inventory/accessory/copper_ring_hover.png", "common", {})
default iron_bracelet = Accessory("Iron Bracelet", 10, 1, "images/inventory/accessory/iron_bracelet_idle.png", "images/inventory/accessory/iron_bracelet_hover.png", "common", {"attack_bonus_flat": 1})
default silver_necklace = Accessory("Silver Necklace", 15, 1, "images/inventory/accessory/silver_necklace_idle.png", "images/inventory/accessory/silver_necklace_hover.png", "common", {"max_hp": 1})
default gold_charm = Accessory("Gold Charm", 20, 1, "images/inventory/accessory/gold_charm_idle.png", "images/inventory/accessory/gold_charm_hover.png", "common", {"attack_bonus_flat": 1})
default platinum_chain = Accessory("Platinum Chain", 25, 1, "images/inventory/accessory/platinum_chain_idle.png", "images/inventory/accessory/platinum_chain_hover.png", "common", {"max_hp": 1})

default topas_pendant = Accessory("Topas Pendant", 30, 1, "images/inventory/accessory/topas_pendant_idle.png", "images/inventory/accessory/topas_pendant_hover.png", "rare", {"attack_bonus_flat": 2})
default ruby_pendant = Accessory("Ruby Pendant", 30, 1, "images/inventory/accessory/ruby_pendant_idle.png", "images/inventory/accessory/ruby_pendant_hover.png", "rare", {"max_hp": 2})
default emerald_pendant = Accessory("Emerald Pendant", 30, 1, "images/inventory/accessory/emerald_pendant_idle.png", "images/inventory/accessory/emerald_pendant_hover.png", "rare", {"attack_bonus_flat": 1, "max_hp": 1})
default sapphire_pendant = Accessory("Sapphire Pendant", 30, 1, "images/inventory/accessory/sapphire_pendant_idle.png", "images/inventory/accessory/sapphire_pendant_hover.png", "rare", {"attack_bonus_flat": 2, "max_hp": 1})
default diamond_pendant = Accessory("Diamond Pendant", 40, 1, "images/inventory/accessory/diamond_pendant_idle.png", "images/inventory/accessory/diamond_pendant_hover.png", "rare", {"max_hp": 3})

default ring_of_defense = Accessory("Ring of Defense", 75, 1, "images/inventory/accessory/ring_of_defense_idle.png", "images/inventory/accessory/ring_of_defense_hover.png", "epic", {"defence": True})
default sharpness_chian = Accessory("Sharpness Chain", 100, 1, "images/inventory/accessory/sharpness_chain_idle.png", "images/inventory/accessory/sharpness_chain_hover.png", "epic", {"attack_multiplier": 1.5})
default armored_charm = Accessory("Armored Charm", 100, 1, "images/inventory/accessory/armored_charm_idle.png", "images/inventory/accessory/armored_charm_hover.png", "epic", {"max_hp": 3, "attack_bonus_flat": 1})
default monocole_of_perserverance = Accessory("Monocle of Perseverance", 100, 1, "images/inventory/accessory/monocole_of_perseverance_idle.png", "images/inventory/accessory/monocole_of_perseverance_hover.png", "epic", {"max_hp": 4})

default chain_of_heroes = Accessory("Chain of Heroes", 200, 1, "images/inventory/accessory/chain_of_heroes_idle.png", "images/inventory/accessory/chain_of_heroes_hover.png", "legendary", {"attack_bonus_dice": "1d6"})
default twin_rings = Accessory("Twin Rings", 250, 1, "images/inventory/accessory/twin_rings_idle.png", "images/inventory/accessory/twin_rings_hover.png", "legendary", {"attack_bonus_flat": 4, "max_hp": 4})
default broken_crown = Accessory("Broken Crown", 200, 1, "images/inventory/accessory/broken_crown_idle.png", "images/inventory/accessory/broken_crown_hover.png", "legendary", {"max_hp": 5})

default void_necklace = Accessory("Void Necklace", 1000, 1, "images/inventory/accessory/void_necklace_idle.png", "images/inventory/accessory/void_necklace_hover.png", "unique", {"attack_multiplier": 2, "max_hp": 10})


# Define Lootboxes
default follower_lootbox = Lootbox("Follower Lootbox", 250, 1, "images/lootboxes/follower_lootbox.png", "images/lootboxes/follower_lootbox_hover.png", "follower")
default armor_lootbox = Lootbox("Armor Lootbox", 100, 1, "images/lootboxes/armor_lootbox.png", "images/lootboxes/armor_lootbox_hover.png", "armor")
default weapon_lootbox = Lootbox("Weapon Lootbox", 100, 1, "images/lootboxes/weapon_lootbox.png", "images/lootboxes/weapon_lootbox_hover.png", "weapon")
default accessory_lootbox = Lootbox("Accessory Lootbox", 100, 1, "images/lootboxes/accessory_lootbox.png", "images/lootboxes/accessory_lootbox_hover.png", "accessory")