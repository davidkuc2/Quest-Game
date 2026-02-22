#Imagebutton Class
init python:
    class ImageButton:
        def __init__(self, image_path, action=NullAction(), target_label=None):
            self.image_path = image_path
            self.action = action
            self.target_label = target_label

# Imagebutton Function with predefined parameters
screen call_image_button(btn):
    imagebutton:
        focus_mask True
        auto btn.image_path
        action btn.action

# Imagebutton Function with given parameters
screen call_image_button_no_target(btn, action):
    imagebutton:
        focus_mask True
        auto btn.image_path
        action action

# Define imagebuttons with predefined parameters

# GUI
default backpack = ImageButton("images/imagebuttons/backpack_%s.png", [Hide("call_gui"), Show("inventory")])
default open_map = ImageButton("images/imagebuttons/map_%s.png", [Hide("call_gui"), Show("worldmap")])
default quest_menu = ImageButton("images/imagebuttons/quest_menu_%s.png", [Hide("call_gui"), Show("quest_menu")])
default follower_logbook = ImageButton("images/imagebuttons/follower_logbook_%s.png", [Hide("call_gui"), Show("follower_logbook")])

# Combat
default attack = ImageButton("images/combat/attack_button_%s.png")
default defend = ImageButton("images/combat/defend_button_%s.png", Call("player_defend"))
default power = ImageButton("images/combat/power_button_%s.png", Call("follower_power"))

# Worldmap
default hermea = ImageButton("images/maps/imagebuttons/hermea_%s.png", Jump("hermea"))
default desert = ImageButton("images/maps/imagebuttons/desert_%s.png", Jump("desert"))
default mountains = ImageButton("images/maps/imagebuttons/mountains_%s.png", Jump("mountains"))
default rainforest = ImageButton("images/maps/imagebuttons/rainforest_%s.png", Jump("rainforest"))
default elf_forest = ImageButton("images/maps/imagebuttons/elf_forest_%s.png", Jump("elf_forest"))
default traumatien = ImageButton("images/maps/imagebuttons/traumatien_%s.png", Jump("traumatien"))

# Church Tamra
default church = ImageButton("images/act1/tamra/imagebuttons/church_%s.png", Jump("church"))

# Guild Tamra
default guild = ImageButton("images/act1/tamra/imagebuttons/adventurers_guild_%s.png", Jump("guild"))
default reception = ImageButton("images/act1/tamra/imagebuttons/guild_reception_%s.png", Jump("reception"))
default quest_board = ImageButton("images/act1/tamra/imagebuttons/guild_quest_board_%s.png", Jump("quest_board"))

# Blacksmith Tamra
default blacksmith = ImageButton("images/act1/tamra/imagebuttons/blacksmith_%s.png", Jump("blacksmith"))
default mern_button = ImageButton("images/act1/people/mern_%s.png", Jump("menu_mern"))

# Mages Tower Tamra
default mages_tower = ImageButton("images/imagebuttons/arrow_left_%s.png", Jump("mages_tower"))


# Define imagebuttons with given parameters

# Arrows
default arrow_up = ImageButton("images/imagebuttons/arrow_up_%s.png")
default arrow_down = ImageButton("images/imagebuttons/arrow_down_%s.png")
default arrow_left = ImageButton("images/imagebuttons/arrow_left_%s.png")
default arrow_right = ImageButton("images/imagebuttons/arrow_right_%s.png")