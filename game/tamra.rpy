# Screen Tamra
screen tamra: 
    use call_image_button(church)
    use call_image_button(guild)
    use call_image_button(blacksmith)
    use call_image_button(mages_tower)
    use call_image_button_no_target(arrow_down, Jump("hermea"))

# Tamra
label tamra:
    scene tamra with Dissolve(.5)
    call screen tamra 

# Church
label church:
    pass

# Guild
label guild:
    pass

# Blacksmith
screen blacksmith:
    add "blacksmith"
    use call_image_button(mern_button)
    use call_image_button_no_target(arrow_down, Jump("tamra"))

label blacksmith:
    call screen blacksmith with Dissolve(.5)

default quest_mern = False

label menu_mern:
    scene blacksmith
    show mern_idle at left
    mern "Welcome to my shop adventurer, how can I help you?"
    menu:
        "Let me look at your wares.":
            call screen shop(blacksmith_shop)
            jump menu_mern
        "I just want to talk.":
            mern """
            Wow that is really nice of you, I must say. So anything in particular that might interest you?

            I have quite a lot to tell honestly. It is not everday that I can just talk with someone without any worries.

            Or maybe it is everyday. You know there are quite some customers in my shop. After all I am selling only the finest equipment.

            Even if I might not look the part, I am a pureblood dwarf. As dwarfish as they get although a bit hairy even for my race.

            But nonetheless I am still not disgustingly tall and a talanted blacksmith. That is what counts, am I right?

            My family hails from the mountains but I decided to take my business here. Some fresh new winds when I was young.

            And I got to love our little city of Tamra. The people, the mages, the guild, its a good place, that much I can tell you.

            I might not have traveled far into this world but there is way worse, dont doubt that. 

            Not every city is this open towards non-human races, you know? Quite some racism out there. But I am rambling. 
            """
            jump blacksmith
        "Do you have any work for me?" if quest_mern == False:
            mern "Did the mages tower not provide you with enough work? Dont you want to relax?"
            mern "Well I mean I work all day myself so who am I to talk right?"
            mern "I guess I could use some help gathering materials for my work. Just think of me if you come across anything that looks forgeable."
            $ give_quest(mern_ressources)
            $ renpy.notify("New Quest: Mern's Ressources")
            $ quest_mern = True
            jump blacksmith
        "Fight":
            mern "Me fight you? That's a bit much, don't you think? I am far too old for this kind of stuff."
            mern "Maybe go to the guild, there is always someone looking for a brawl. But be warned, even the drunks can give you a run for your money."
            mern "Another thing. If you ever just ask that again, I wont be selling you any more stuff, got that?"
            jump blacksmith
        "I am just taking a look around":
            jump blacksmith

# Mages Tower
label mages_tower:
    pass