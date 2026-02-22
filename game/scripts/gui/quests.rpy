init python:

    # --- Quest Class ---
    class Quest():
        def __init__(self, name, description):
            self.name = name
            self.description = description
            
    def give_quest(quest_to_add):
        if quest_to_add not in quests:
            quests.append(quest_to_add)

    def remove_quest(quest_to_remove):
        if quest_to_remove in quests:
            quests.remove(quest_to_remove)


# Define Quests
default quests = []
default mern_ressources = Quest("Mern's Ressources", "Find suitable ressources and give them to Mern")


screen quest_menu():
    modal True
    zorder 1000
    add "background_quest"

    viewport:
        xalign 0.5
        yalign 0.5
        xsize 900
        ysize 900
        scrollbars None
        mousewheel True
        draggable True

        vbox:
            spacing 20
            for q in quests:
                vbox:
                    text q.name color "#000000" size 40 bold True
                    text q.description color "#000000" size 30 xsize 900
                    null height 20

    use call_image_button_no_target(arrow_down, [Hide("quest_menu"), Show("call_gui")])

    key "q" action [Hide("quest_menu"), Show("call_gui")]
    key "game_menu" action [Hide("quest_menu"), Show("call_gui")]