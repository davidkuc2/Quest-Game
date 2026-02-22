# Reward for win
label combat_reward:

    pass                                    # create loot table

    hide screen fight
    show screen call_gui
    $ combat_reset()                        # resets all characters back to default state 
    jump expression after_combat_label      # jump to the label name stored in the variable


# Consequences for loss
label combat_loss:                          # kill the player at loss

    "You have lost the fight and died!"
    $ combat_reset()                        # reset all characters back to default state
    $ MainMenu(confirm=False)()             # return to main menu