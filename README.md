# Pop The Clock
### A fun, practice arcade style reaction game, inspired by Pop The Lock. A needle spins around a 12 numbered clock face, click the spacebar to flip direction Try to land on the highlighted number before it passes, or in Special mode, click the numbers in your code sequentially.

# Game Modes:
### Classic - Hit the highlighted number to advance the clock forward a minute, and when missing, the clock ticks backward (or, in harder difficulties, it's an instant loss). Reach 12:00 to complete the level. Needle speed increases as you progress through harder difficulties. This gamemode is the one that's inspired by Pop The Lock. 
### Special - Instead of  chasing a target, you're given a code, and you must click on the needle at the exact moment it lands on each number, while doing it in sequential order. You start with 3 lives, and with each miss or wrong click, you lose a life. As you progress through harder difficulties, the code gets longer, and so does the needle speed. 

### There are 4 difficulty ties per mode - Noob, Pro, Hacker, and God - each with increasing speed, longer codes for special mode, creating tighter margins for error. 

# Badges 
### Beating each difficulty mode earns  you a unique badge (eight total), which can be equipped to display in the main menu. However, I do plan to add extra features in the future that use these badges. 

# What Pop The Clock is built with: 
- **CustomTkinter**: Main app window, does all rendering, and is done via Canvas drawing, not actual CTk widgets.

- **Image/graphics processing (Pillow, Image, ImageSequence, and ImageTk)**: Used for loading/resizing images, processing GIF frames, alpha blending, and converting to Tk displayable PhotoImage objects.

- **Numpy**: used inside rotatehue() for the hue-changing background. 

- **Standard library**: Includes threading, json, os, sys, random, time, ctypes, colorsys, and math.

# Assets:
- Custom font: Press Start 2P - a retro pixel styled font
-  PNG/ICO images for badges, mode logos, hearts, needle, and app logo.
- GIFS for the background, loading screen, and menu backdrop animation

# Challenges I ran into:
### I ran into many challenges while building this app. At first, I didn't know how to start with, but after many hours brainstorming with AI, I started building, creating the movement for the needle. I then realized realized the window geometry for the game was too small to add any numbers, so I spent many more grueling hours resizing and fixing everything. Also, when I tried adding the hue-changing feature, the switch was too sudden, so I spent many more hours reading docs and researching for ways to fix this, which ended up paying off. In addition to that, adding the text animation feature was a bit annoying, so I asked AI for help, but when that didn't work out well, I asked a friend, who ended up getting the feature working. This app has been a huge roller coaster, but in the end, I managed to pull through and get everything I wanted to get done in the first iteration. 

# Disclaimer:
### Pop the Clock was mainly built on macOS, and downloading the .app version for mac will most likely run smoother than the EXE. Pop The Clock is still in BETA, so there may be bugs that I'm unaware of. 

# Text Animation
### The pulsing text throughout the game was inspired by a text animation effect I saw a YouTuber use in one of their projects. Each letter is drawn individually and offset using a sine wave, giving it that "cool" effect. Getting the timing and math was pretty tricky, so a friend of mine helped me get the feature fully working. 

# Where AI assistance was used:
- AI helped fix hue-changing background
- A bit of AI assistance was used to help fix/debug parts of the code. 
- AI helped with an early attempt of the text animation, though a friend got it working at the end
- AI helped with the number fading, and some of the logic
- For the parts I missed, some areas that use AI are declared in the commits
#### For the most part, the rest of the application logic, UI development, and modes were created by me.



