screen cheat_menu():
    modal True
    zorder 100
    add "cheat_menu"

    vbox:
        align (0.5, 0.5)
        spacing 20

        if world_map_unlocked == False:
            textbutton "enable worldmap" action SetVariable("world_map_unlocked", True)
        textbutton "skip tutorial" action [SetVariable("inventory_unlocked", True), SetVariable("quests_unlocked", True), Hide("cheat_menu"), Show("call_gui"), Jump("tamra")]
        textbutton "+100 coins" action [SetField(inventory, "money", inventory.money + 100)]
        textbutton "test fight" action Jump("test_fight")
        if follower_logbook_unlocked == False:
            textbutton "enable follower logbook" action SetVariable("follower_logbook_unlocked", True)
        if not green_slime.unlocked:
            textbutton "unlock green slime" action Function(green_slime.unlock)

    key "c" action [Hide("cheat_menu"), Show("call_gui")]
    key "game_menu" action [Hide("cheat_menu"), Show("call_gui")]


# Test Fight
default test_enemy = Enemy_Character("Mern", 20, 20, 3, 0, ["water"], ["fire"], ["fire"], 1, "images/act1/people/mern_idle.png")

label test_fight:
    hide screen cheat_menu
    scene blacksmith 
    $ after_combat_label = "tamra"
    $ enemy = test_enemy
    jump fight