
# Please forgive me for my spaghetti-like code...
# Also, don't blame me for the excessive comments, you asked for it!

import os
import sys
import time
import random
import platform


# * Setting up all the constants, default values, and functions

# A few color constants for customizing some of the text
COLOR = {
    "PURPLE": "\033[95m",
    "BLUE": "\033[94m",
    "GREEN": "\033[92m",
    "GREENB": "\033[32m",
    "G": "\033[92m",  # a shortcut
    "GB": "\033[32m",
    "RED": "\033[91m",
    "REDB": "\033[31m",
    "CYAN": "\033[1;96m",
    "BOLD": "\u001b[1m",
    "ITALIC": "\u001b[3m",
    "END": "\033[0m",
    "ENDC": "\033[0m",
}

# Settings are in a list instead of variables because that's the only way to
# perform 'callby reference' in Python to be able to change the value of a
# boolean outside the function scope.
# Although I hate pointers (as one should), they're
# still useful... They have my utmost respect.
settings_values = [True, True]

# A list of responses used in random if a
# person tried to enter an incorrect input
wrong_choice = ("Please choose one of the available options.",
                "That doesn't seem like an option... Try again.",
                "I don't think this option is available. Try another one.",
                "Nope, that's not one of the options. Give it another try.")

# Characters' names
characters = ("Amon", "Planeswalker", "Pyromaniac", "Sun Fanatic",
              "Visionary", "Vampire", "Folk of Rage", "Shadow of Order",
              "Silver Knight", "Nightmare")

# Thanking the user for playing at the end of the game
end_message = f"\n\n{COLOR['GREEN']}Thanks for playing!{COLOR['ENDC']}"


# Display the title and introduces the game
def title():

    # Clears the terminal to make it look cleaner
    clear_terminal()
    freeze(0.5)

    # Print the title
    print(COLOR["BLUE"], r"""
    ______      __       __                          __
   / ____/___ _/ /____  / /_  ____  __  ______  ____/ /
  / /_  / __ `/ __/ _ \/ __ \/ __ \/ / / / __ \/ __  /
 / __/ / /_/ / /_/  __/ /_/ / /_/ / /_/ / / / / /_/ /
/_/    \__,_/\__/\___/_.___/\____/\__,_/_/ /_/\__,_/

        """, COLOR["ENDC"])
    freeze(1.5)

    # Author (me!)
    typewrite((f"By {COLOR['BLUE']}Kareem Osama{COLOR['ENDC']}"),
              delay=0.04,)

    # Start the game or open the settings first
    typewrite((f"\nPress {COLOR['GREEN']}Enter{COLOR['ENDC']}"
               + " to start the game...|"
               + f"\n(Or enter {COLOR['GREEN']}'s'{COLOR['ENDC']}"
               + " to open the settings)"), pause_chars=[])

    begin = choice_validation(["", "s", "settings"],
                              just_validate=True, message="")

    if begin == "s" or begin == "settings":
        settings()

    typewrite(f"\n{COLOR['CYAN']}Starting the game!{COLOR['ENDC']}",
              end_pause=1.5)

    # typewrite((COLOR["BLUE"] + "\n=============="
    #           + COLOR["ENDC"]), pause=0, end_pause=0.5, pause_chars=[])
    clear_terminal()

    freeze(3)
    print("\n")


def typewrite(text, delay=0.03,  # The delay between each character
              end_pause=2.0, pause=0.5,
              newline_pause=1.0, hidden_pause_chars=["|"],
              newline_pause_chars=["~"],
              pause_chars=[",", ".", ":", ";", "!", "?"],
              # Inserts a new line after writing the given arg
              newline=True,
              # Useful for inputs
              print_end="\n"):

    # Enables or disables the typewrite effect (toggle-able in settings)
    enable = settings_values[0]

    if enable is True:

        # For better ellipses, check the elif char == "`"'s comments for more
        if "..." in text:
            text = text.replace("...", "```")

        for char in text:
            # For phonetic pauses in the middle of the text
            if char in hidden_pause_chars:
                freeze(pause)

            # If the paragraph is not over, but you want to insert
            # a new line with a short pause after it.
            elif char in newline_pause_chars:
                freeze(newline_pause)

            # Also for phonetic pauses
            elif (char in [",", ":"]) and (char in pause_chars):
                # end="" ensures that a new line isn't printed after each char
                # & flush=True constantly updates the character in the terminal
                print(char, end="", flush=True)
                freeze(delay + 0.65)

            # For better ellipses, the . is replaced with a ` for the code to
            # recognize it, then a custom delay is applied to it and . is
            # printed instead of it...
            elif char == "`":
                print(".", end="", flush=True)
                freeze(delay + 0.20)

            # Not the same as the elif statement above (it was initially),
            # since a full stop's pause should be longer than a comma
            elif char in [".", "?", "!"] and (char in pause_chars):
                print(char, end="", flush=True)
                freeze(delay + 0.85)

            # If it was just a normal character, print it and pause for a bit
            else:
                print(char, end="", flush=True)
                freeze(delay)

        # After printing the given argument, pause to indicate a stop
        freeze(end_pause)

        if newline is True:
            print()

    # Basically simulates the print_pause function without having
    # to rewrite everything just to disable the typewrite effect
    else:
        # The two replace methods remove the characters meant for pauses
        # in the typewrite effect (yes, this is the most efficient way...)
        print(text.replace("|", "").replace("~", ""), end=print_end)
        freeze(end_pause)

        if newline is True:
            print()


# Takes a list of options, then lists them to the
# player and ensures the exists in the list
def choice_validation(options, just_validate=False,
                      message="Your choice: ",
                      # Returns the option's number, not the exact
                      # choice the user entered
                      return_num=False,
                      # hide the last n options (for easter eggs...)
                      hide_last=0):

    length = len(options)

    # A bit confusing... This line basically takes the number of the options,
    # makes it a list, then converts the elements of the list to strings
    number_of_options = list(map(str, range(1, length+1)))

    # If true, it skips the listing option step and 'just validates' the input
    if just_validate is False:

        typewrite((f"\n{COLOR['CYAN']}You have"
                   + f" {length - hide_last} options:{COLOR['ENDC']}\n"),
                  end_pause=1.70)
        counter = 1
        # List the options for the player
        for choice in options[:length - hide_last]:
            typewrite(f"{counter}. {choice}", end_pause=1.5, pause=0.75)
            counter += 1

        # The 'length - hide_last' statements hide the last n options.
        # I'll use in some easter eggs (not that much of a waste of time).
        # I'll not make it dynamic, however, since that would
        # be an actual waste of time...

    while True:
        typewrite("\n" + message, 0.02, end_pause=0,
                  pause=0.75, newline=False, print_end="")
        sys.stdout.flush()  # To make input next to the written text,
        # not a new line, while still maintaining the
        # typewriting effect

        choice = input().lower()

        # Make sure all the options are in lowercase
        options_lower = [o.lower() for o in options]

        # Can accept both the choice number and the choice itself in text
        if ((choice not in number_of_options) and
                (choice not in options_lower)):

            # If the choice is incorrect, output a
            # random error message, then try again
            typewrite(random.choice(wrong_choice), delay=0.02,
                      end_pause=1, pause=0.5)

        # If the user entered a correct input:
        else:
            if return_num:
                # If the user entered the option not its number,
                # convert it back to a (stringified) number and return it
                if choice in options_lower:
                    return str(options_lower.index(choice) + 1)

            return choice


# Similar to the choice_validation function, except a bit more
# concise since it only has one purpose (yes or no)
def yn_validation(text, initial=True):

    print()  # Simplest way to add a new line...
    while True:
        typewrite(text, 0.02, end_pause=0, pause=0.75,
                  newline=False, print_end="")
        sys.stdout.flush()
        choice = input().lower()

        if (choice == "y") or (choice == "yes"):
            return initial
        elif (choice == "n") or (choice == "no"):
            return not initial
        else:
            typewrite(random.choice(wrong_choice),
                      delay=0.02, end_pause=1, pause=0.5)


# Open and fetch the text file where all the characters' descriptions are
# stored (Trying to put long paragraphs here is too troublesome,
# _extremely_ troublesome, in fact, that I had to come up with this...)
def fetch_text(description_id, file_path="game_text.txt"):
    try:
        with open(file_path, "r") as file:
            content = file.read()

        # Each description is separated by a '# n ',
        # where n is the ID, So this line uses this
        # fact to separate the file into a list descriptions
        descriptions = content.split("\n# ")
        for description in descriptions:
            if description.startswith(str(description_id)):
                # Remove the '# n ' part, you only need the description
                return description[3:].strip()

        return None

    # If the main text file was not found,
    # print an error message and exit the game
    except FileNotFoundError:
        typewrite((f"\n{COLOR['REDB']}ERROR{COLOR['ENDC']}: Couldn't find"
                   + " the main text file for the game."), end_pause=1)

        typewrite("\nYou can find it at:", end_pause=0.5)
        typewrite((f"{COLOR['CYAN']}https://github.com/Kareem01001011/"
                   + f"Fatebound/blob/main/game_text.txt{COLOR['ENDC']}"),
                  pause_chars=[], end_pause=1)
        typewrite(("\nPlease download it and put it in the same directory as"
                   + " the game's python file to be able to play the game."))
        quit()


# Clear the terminal screen
def clear_terminal():
    if os.name == "nt":  # For Windows
        os.system("cls")
    else:  # For Unix-based operating systems
        os.system("clear")


# This was too complicated...
# The terminal was still accepting inputs and giving them to the input
# statement while the code (time.sleep, specifically) was running, which
# would be extremely annoying if you pressed enter multiple times, you'll have
# to wait until the code is done. The only fix I could think of was to somehow
# freeze the terminal, since nothing could be done about this using time.sleep
def freeze_terminal_unix(duration):
    # Import unix-only modules necessary for this function to work on
    # Unix-based systems (had to be imported inside the function so as to
    # not cause compatibility issues if run on Windows (the same
    # could be found in the windows function))

    # The imports are here instead of the top of the code is because if I
    # tried to put all the unix + windows modules, the code would return
    # an error and won't work on either one of them
    import termios
    import tty

    # Get the terminal settings
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)  # type: ignore

    try:
        # Set the terminal to raw mode
        tty.setraw(fd)  # type: ignore
        # Sleep for the specified duration
        time.sleep(duration)

    except KeyboardInterrupt:  # If the user pressed ctrl+c, restore settings
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)  # type: ignore
    finally:
        # Restore the terminal settings
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)  # type: ignore


# Same function but for Windows (had to be separate because of compatibility)
def freeze_terminal_windows(duration):
    import msvcrt
    start_time = time.time()

    while time.time() - start_time < duration:
        # Clear the buffer
        while msvcrt.kbhit():
            msvcrt.getch()
        # Sleep for a short period to allow CPU to rest
        # time.sleep(0.1)


# The function that decides which one should run (a default)
def freeze(duration, os_name=platform.system()):

    # Enables or disables this freeze function (toggle-able in settings)
    if settings_values[0]:
        if os_name == "Windows":
            freeze_terminal_windows(duration)
        else:
            freeze_terminal_unix(duration)

    # If disabled, just use the normal time.sleep
    else:
        time.sleep(duration)


# Displays the settings
# While I don't recommend switching them off, since the game is designed
# around the current ones, and they're objectively better, at least you can...
def settings():

    typewrite((f"\n{COLOR['BLUE']}==== Settings ===={COLOR['ENDC']}"))
    print()

    # List all the settings. Doesn't need to be dynamic since the settings
    # won't change. This is just much simpler and is a lot easier to use
    typewrite((
        f"1. Typewrite effect: {settings_values[0]}|~\n"
        + f"2. Better pause function: {settings_values[0]}|~\n"

        # An option to exit the settings, or
        # else players will be stuck forever
        + "\n(Enter 3 to exit the settings)"
        ), newline=False)
    print()

    while True:
        # Used just_validate since the options are already listed
        option = choice_validation(["1", "2", "3", "exit", "e"],
                                   just_validate=True)

        if option == "1":

            # Since this is a true/false setting, you don't
            # need options, just 'switch' the setting on or off
            settings_values[0] = yn_validation(
                f"Switch to {not settings_values[0]}? (Y/n): ",
                not settings_values[0])

            # Had to do this to escape the 80 character limit...
            typewrite(
                f"The typewrite effect is now set to: {settings_values[0]}."
                )

        elif option == "2":

            # Same as the typewrite setting
            settings_values[0] = yn_validation(
                f"Switch to {not settings_values[0]}? (Y/n): ",
                not settings_values[0])

            # Had to do this to escape the 80 character limit...
            typewrite(
                f"Better pause is now set to: {settings_values[0]}."
                )
        elif option == "3" or option == "exit":
            typewrite((COLOR["BLUE"] + "\n==== Exiting settings... ===="
                       + COLOR["ENDC"]), pause=0, end_pause=1, pause_chars=[])
            break


# A list of already shown character ID so they don't repeat
shown_characters = []


# Generate a random number which will determine
# which character the player will encounter
# This function ensures the characters shown don't repeat/get shown again.
def random_character_id(hidden_characters=[]):
    id = random.randint(0, 8)

    while id in shown_characters or id in hidden_characters:
        id = random.randint(0, 8)

    # Add the ID to the list so it doesn't repeat
    shown_characters.append(id)
    return id


# Returns a comment about the user's score (sometimes praises, but mostly
# ridicule. Good luck!)
def score_response(score):

    perfect = ["That's impressive!", "Congratulations!!", "Flawless!",
               "Perfect! Nice to see someone skilled every once in a while",
               # A few ridiculing ones because why not?
               "Even a broken clock is right twice a day.",
               "Is this a fluke or are you actually good?",
               "Looks like the stars aligned for you.",
               "Did you cheat? This is surprisingly good.",
               "Impressive! Did you get help?", "Miracles do happen, huh?"]

    good = ["Good. Can be better though. Go on!",
            "Good enough for now. Keep trying!",
            "Not bad, but there's room for improvement.",
            "Decent enough. I expect more from you next time.",
            "You almost looked skilled there.", "Halfway to mediocrity!"]

    mid = ["Are you even trying?", "Just git gud bro...", "Tough luck, bud.",
           "That was painful to watch.", "Wow, that's embarrassingly bad.",
           "Not bad, for an amateur.", "Did you even try?"]

    zero = ["Zero points? Really? Try harder next time!",
            "That's a record! The lowest one, but still a record...",
            "You couldn't even accidentally get a point?",
            "Wow, that's embarrassingly bad.", "Are you even trying?",
            "Did you even try?"]

    negative = [("How? Just how??? It isn't even possible to get"
                 + " less than zero points... How did you do it?")]
    # The ridiculing comments may have come out to be a little bit
    # more than a few... Don't judge me! This is too fun!
    # (By the way, I don't mean it in an offensive way, of course. This is
    # all just for fun and laughs)

    # Perfect score!
    if score >= 50:
        return (f"{COLOR['GREEN']}Your score: {score}{COLOR['ENDC']}"
                + f"\n{COLOR['GREEN']}{random.choice(perfect)}{COLOR['ENDC']}")

    # Good
    elif score < 50 and score >= 25:
        return (f"{COLOR['CYAN']}Your score: {score}{COLOR['ENDC']}"
                + f"\n{COLOR['CYAN']}{random.choice(good)}{COLOR['ENDC']}")

    # Meh...
    elif score < 25 and score > 0:
        return (f"{COLOR['CYAN']}Your score: {score}{COLOR['ENDC']}"
                + f"\n{COLOR['CYAN']}{random.choice(mid)}{COLOR['ENDC']}")

    # Zero, bad
    elif score == 0:
        return (f"{COLOR['RED']}Your score: {score}{COLOR['ENDC']}"
                + f"\n{COLOR['RED']}{random.choice(zero)}{COLOR['ENDC']}")

    # How?
    elif score < 0:
        return (f"{COLOR['REDB']}Your score: {score}{COLOR['ENDC']}"
                + f"\n{COLOR['REDB']}{random.choice(negative)}{COLOR['ENDC']}")


# Display a "you lose" message and show your score when you lose
# Separated into its own function because I kept copying and pasting it
def you_lose(score):
    typewrite(f"\n{COLOR['REDB']}You lose.{COLOR['ENDC']}")
    typewrite(f"\n{score_response(score)}")  # type: ignore


# Since I made a 'you lose' function, why not make a 'you win'?
def you_win(score):
    typewrite(f"\n{COLOR['GB']}You win!{COLOR['ENDC']}")
    typewrite(f"\n{score_response(score)}")  # type: ignore


# Connects and uses every part of this spaghetti-like code...
def main():

    # Reset the score everytime the main
    # function runs (when the game restarts)
    score = 0

    # Randomize the characters everytime the function runs
    character_id = random_character_id()
    character = characters[character_id]
    character_description = fetch_text(character_id)

    # I will not let Amon be the second opponent, I don't want to
    # add another part where you'll die again.
    # (Just pretend that Amon created a bug here and hidden
    # himself for your sake, then go thank him...)
    character2_id = random_character_id(hidden_characters=[0])
    character2 = characters[character2_id]
    character2_description = fetch_text(character2_id)

    # Print the title
    title()

    # Clears the terminal to remove the title and begin the story
    clear_terminal()

    # * Story

    # Introduction

    typewrite((f"\n{fetch_text(10)} "
               + f"{COLOR['REDB']}{fetch_text(11)}{COLOR['ENDC']}"))

    # Mid-game

    typewrite(f"\n\n{COLOR['ITALIC']}{fetch_text(12)}{COLOR['ENDC']}",
              newline_pause=0.5)

    decision1 = choice_validation(["Read the book", "Ignore it"],
                                  return_num=True)

    next = [False]

    if decision1 == "1":
        typewrite(f"{COLOR['GREEN']}Good choice! +10 points{COLOR['ENDC']}")
        score += 10
        next[0] = True

    elif decision1 == "2":
        typewrite(f"\n\n{fetch_text(13)}",
                  newline_pause=0.5)

        decision1_2 = choice_validation(["Read the book", "Keep ignoring it"],
                                        return_num=True)
        if decision1_2 == "1":
            typewrite((f"{COLOR['GREEN']}Finally! Good choice."
                       + " +5 points{COLOR['ENDC']}"))
            score += 5
            next[0] = True

        elif decision1_2 == "2":
            typewrite(f"\n\n{fetch_text(14)}", newline_pause=0.5)

            you_lose(score)

    if next[0]:
        typewrite((f"\n{fetch_text(15)}{COLOR['CYAN']} "
                   + f"{fetch_text(16)}{COLOR['ENDC']}{fetch_text(17)}"),
                  newline_pause=0.5, newline=False)

        typewrite(f"\n\n{COLOR['ITALIC']}{fetch_text(18)}{COLOR['ENDC']}")

        typewrite((f"\n\n{fetch_text(19)} {COLOR['CYAN']}{fetch_text(20)}"
                   + f"{COLOR['ENDC']}."))

        typewrite(f"\n\n{fetch_text(21)}")

        typewrite(f"\n{COLOR['PURPLE']}...{COLOR['ENDC']}")

        typewrite(f"\n{COLOR['ITALIC']}{fetch_text(22)}{COLOR['ENDC']}")
        typewrite(f"\n\n{fetch_text(23)}")

        # Don't ask about this...
        open_doors = ["as you open your door, ", "just as you step outside, ",
                      "as you step outside, ", "just as you open your door, ",
                      "as you open the door, ", "as you step outside, "]
        if character_id in [1, 2, 5, 5, 6, 7]:
            open_door = random.choice(open_doors)
        else:
            open_door = f"{random.choice(open_doors)}you "

        typewrite(f"\n\nBut sure enough, {open_door}{character_description}")

        # EASTER EGG: Hide the last option if the opponent is Amon
        if character_id == "0":
            decision2 = choice_validation(["Talk to him nicely",
                                           ("Immediately close the door and"
                                            + " escape through the window"),
                                           "Attack on sight"],
                                          return_num=True, hide_last=1)
        else:
            decision2 = choice_validation(["Talk to him nicely",
                                           ("Immediately close the door and"
                                            + " escape through the window"),
                                           "Attack on sight"],
                                          return_num=True)

        if decision2 == "1":
            typewrite(f"\n\n  {fetch_text(25)}", end_pause=1)
            typewrite(f"  {character}{fetch_text(26)}", end_pause=1)
            typewrite(f"  {fetch_text(27)}", end_pause=1)
            typewrite(f"  {character}{fetch_text(28)}", end_pause=1)
            typewrite(f"  {fetch_text(29)}", end_pause=1)
            typewrite(f"  {character}{fetch_text(30)}", end_pause=1)

            typewrite(f"\n{fetch_text(31)}", end_pause=1)

            you_lose(score)

        elif decision2 == "2":
            typewrite(f"{COLOR['G']}Good choice! +10 points{COLOR['ENDC']}")
            score += 10

            # Don't ask about this too...
            if character2_id in [1, 2, 5, 5, 6, 7]:
                you_see = "You see "
            else:
                you_see = "You "

            typewrite(f"\n{fetch_text(32)}", end_pause=1)

            typewrite(f"\n{COLOR['PURPLE']}...{COLOR['ENDC']}")

            typewrite(f"\n{fetch_text(33)}", end_pause=1)

            typewrite(f"\n{you_see}{character2_description}")

            decision3 = choice_validation(["Proceed with your plans",
                                           "Ignore him"],
                                          return_num=True)

            if decision3 == "2":
                typewrite(f"\n\n{fetch_text(35)}", end_pause=1.25)
                typewrite(f"\n  {fetch_text(36)}", end_pause=1)
                typewrite(f"  {character2}{fetch_text(37)}", end_pause=1)
                typewrite(f"  {fetch_text(38)}", end_pause=1)
                typewrite(f"  {character2}{fetch_text(39)}", end_pause=1)

                typewrite(f"\n{fetch_text(40)}", end_pause=1)

                you_lose(score)

            elif decision3 == "1":
                typewrite(f"{COLOR['G']}Good choice! +5 points{COLOR['END']}")
                score += 10

                typewrite(f"\n\n{fetch_text(41)}")
                typewrite(f"{COLOR['GB']}+20 points!{COLOR['ENDC']}")
                score += 20

                # Epilogue

                typewrite(f"\n\n{COLOR['PURPLE']}...{COLOR['ENDC']}")

                typewrite((f"\n\n{fetch_text(42)}"
                           + f" {COLOR['GB']}{fetch_text(43)}{COLOR['ENDC']}"),
                          end_pause=0.75)

                you_win(score)

        # EASTER EGG: If the player still chose the last option,
        # they would lose immediately...
        elif decision2 == "3" and character_id == "0":
            typewrite(f"\n\n{COLOR['BLUE']}EASTER EGG!{COLOR['ENDC']}",
                      end_pause=0.75)
            typewrite(f"\n{fetch_text(24)}")

            you_lose(score)

        # You know what, since I don't know what to write to make the player
        # win, I'll make him lose anyway...
        elif decision2 == "3" and character_id != "0":
            typewrite(f"\n\n{fetch_text(44)}", end_pause=1)
            typewrite(f"{COLOR['G']}+5 points{COLOR['ENDC']}")
            score += 5
            typewrite(f"\n{fetch_text(45)}", end_pause=1)

            you_lose(score)

    # Ask the user if they want to play again
    again = yn_validation((f"\n{COLOR['CYAN']}Play again? (Y/n):"
                           + f" {COLOR['ENDC']}"))
    return again


# Run the game
try:

    # Play-again loop
    again = True
    while again:
        shown_characters = []
        again = main()

    # End message, when the user exits the game
    typewrite(end_message, end_pause=1)

# In case users type ctrl+c (I do this all the time when testing and the long,
# annoying error messages I get when I do so are getting on my nerves...)
except KeyboardInterrupt:

    # Another one in case the user was impatient and pressed it twice
    # (Yes, I know this due to personal experience...)
    try:
        typewrite(end_message, end_pause=1)
    except KeyboardInterrupt:
        # Colors would cause a bug if they were not cleared before quitting
        print(COLOR["ENDC"])
        quit()
