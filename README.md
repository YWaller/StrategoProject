# StrategoProject
Hello everyone, or more likely the odd person every few months or years!

If you like Stratego, and know how to code python, I could probably use your help making this better.

Anyways, what it can do right now... you have a full graphical interface, and an AI player to play against.
The game is functional in that regard. You can also play with two people.


# How to Run
To run the game, you of course need all the files here. Open up mainwithai.py and run it. It may take a moment (more like several moments), the AI goes first. You can change that somewhere in mainwithai.

# File Structure
As you've read, mainwithai is how you start the game. That file contains the actual game engine, written with pygame. It handles all the movement and such.

The next important file is SAI.py. This file contains the AI class. 

The meat and potatoes of the AI is done in getboards.py. This file contains the code for the tree search algorithm, and is where the neural network scores various boards.

The images, setups, etc. are all generally in the resources file. Of particular note is default.map. Open this in notepad++ and you'll see the default setups the game currently uses for testing. sandbox.py contains the code to make a new one.

Build_setups.py, which makes use of the gurobi optimizer to find setups that meet criteria for say, defensiveness of a setup, is also included. The last file of note is xmlparse, which I used to build my six million boards from a database of Stratego games.

neuralstrategoALL is my convolutional neural network trained on six million boards, and who won that game. The file strategoneural is included, and this shows the architecture of that cnn. 

Sandbox is my testbed for various things, and temp has random odd bits. Both can be safely ignored. Sandbox, as of the "massive update" commit, contains code for building out setups, and in the next update that code may be integrated. Note, this is not graphical, it works through the console, and is not connected to the game as of now.


# Issues/Options for Contributors
First, if you'd like to contribute, thank you! I don't have a ton of time to give to this, but I want it to be awesome.

Things of high priority are: 
1. Graphical interface for making your own setup, and assigning the enemy a random or pre-generated one.

1a. Connecting the current setup code to the game itself. Some hooks and logic are built into mainwithai, but are unused right now.

1b. Making the setup builder more powerful; being able to automatically build a "fortress" for the flag and the like.

2. Speeding up the tree search. This is the most important, in my mind. 

3. Programming some domain knowledge into the AI. I've started this with terminal state counts, but if you know a lot about stratego, then I could really use your help in determining which moves are the most useful from a programmatic standpoint, instead of just the neural network. I'd like a hybrid system eventually. 

3a. The AI right now gets to see your pieces. This is cheating per the rules of Stratego :P but honestly I don't really care if it cheats if it plays well. I plan to at some point develop a second neural network, or something else, to predict what pieces you have where, so there is a "non cheating" mode.

4. Letting the AI learn more by playing itself, and using the resulting games. 

5. Cleaning the code up. There's a lot of unnecessary stuff in SAI in particular. 

6. Calculating the various move strengths in parallel. I'm currently working on this; it would save a ton of time.

# Miscellaneous notes
If you'd like to hide the opponent's pieces, then there's a line in mainwithai.py that has the switch. I have this feature off right now while I figure things out and do testing. CTRL+F "hidden" and it should be in about line 328, just uncomment out that line, and the same one about 9 lines later also needs to be uncommented. The lines directly after them then need to be commented out. It'll make sense when you see it (I hope).

I've commented things as best I've had time for/cared to, but if you feel something is unclear, then just ask. I'd be more than happy to help explain it.

About me, I'm 23 years old (as of massive update), I'm a data scientist at some random tech company no one cares about, and I got both my undergrad and master's in data science. I love boardgames, specifically stratego, so this is a great melding of my likes.

If you'd like to contact me about this, I'm most reachable at ylwaller [at] email.wm.edu

