# Synapse Clicker

An idle/incremental clicker game themed around growing a neural network, building just as a skill-developing project, to recover my python skills I lost from basically no coding for 2 years. 
This is basically Cookie Clicker but with neurons. You click to generate neurotransmitters, then spend them on upgrades that make you generate more automatically.

## What it does

- Click the neuron button to earn neurotransmitters (NTs)
- Spend NTs on three upgrades:
  - **Dendrite Branching** – boosts how much you earn per click
  - **Glial Cell Support** – adds passive NT/sec income
  - **Myelin Sheath** – multiplies your passive income
- Upgrade prices go up every time you buy one (1.15x per level, so it doesn't get too easy)
- Random neuroscience facts rotate at the top every 30 seconds
- Save/load your progress so you don't lose everything on restart

## Built with

- Python
- Tkinter (GUI)
- JSON (save files)
- `root.after()` for the loopfact rotation, so nothing should freeze the window while it runs

## Notes

This was my first time really working with Tkinter, so a decent chunk of the build was debugging stuff like grid layout weirdness, `mainloop()` needing to go at the very end, closures inside loops not capturing values the way I expected, and getting the passive tick loop to run without blocking the UI. Learned a lot doing it.
I've written some notes in the code for what i did wrong along the way so i can keep a note

Screenshot of gameplay:
<img width="833" height="638" alt="Screenshot 2026-08-12 at 12 40 50 PM" src="https://github.com/user-attachments/assets/0b83ec1f-3239-4e82-b1b4-e782ba6e446a" />

## Setup

**Requirements:** Python 3.10+ and pip

1. Clone the repo:
```bash
   git clone https://github.com/Vihaan-Vasudeva/Synapse-Clicker.git
   cd Synapse-Clicker
```

2. Install dependencies:
```bash
   pip install pillow
```
(`tkinter` ships with most Python installs — if you get a `No module named tkinter` error on Linux, run `sudo apt install python3-tk`. On macOS/Windows it's included by default.)

3. Run the game:
```bash
   python3 "synapse clicker-v1.py"
```
(or just click the run button in your IDE)

Alternatively, download the pre-built macOS app from the [Releases page](https://github.com/Vihaan-Vasudeva/Synapse-Clicker/releases) — no Python install required.

## Notes

- **macOS Gatekeeper:** the compiled `.app` isn't notarized by an Apple Developer account, so macOS may flag it as from an "unidentified developer" on first launch. Right-click the app → Open, then confirm, to bypass this.
- **Save data:** progress is stored in `save_data.json` in the same folder as the app. Delete this file to force a fresh start (or use the in-game Reset button).
- **neuron.png must stay in the same folder** as the script/app — it's the source image for the clickable neuron and resizes dynamically as you buy upgrades.
- Built and tested on macOS (Apple Silicon). Should run cross-platform from source via Python, but the compiled binary is macOS-only(sorry!)

HAVE FUN PLAYING AND V2 COMING SOON
