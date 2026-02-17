# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

# Tamra Akt I
define player = Character("[player_name]", color="#000000")
define milim = Character("Milim", color="#c24448")
define larisa = Character("Larisa", color="#c6a858")
define heidra = Character("Heidra", color="#7c3f1c")
define mern = Character("Mern", color="#dc4488")

# The game starts here.

label start:
    jump arrival

screen worldmap:
    zorder 200
    modal True
    add "worldmap"

    use call_image_button(hermea)
    use call_image_button(desert)
    use call_image_button(mountains)
    use call_image_button(rainforest)
    use call_image_button(elf_forest)
    use call_image_button(traumatien)
    use call_image_button_no_target(arrow_down, [Hide("worldmap"), Show("call_gui")])

    key "m" action [Hide("worldmap"), Show("call_gui")]
    key "game_menu" action [Hide("worldmap"), Show("call_gui")]

label hermea:
    pass

label ocean:
    pass

label desert:
    pass

label mountains:
    pass

label rainforest:
    pass

label elf_forest:
    pass

label traumatien:
    pass