import tkinter as tk
import random
import sys, os
import json
from tkinter import messagebox



def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

from PIL import Image, ImageTk

base_passive = 0
passive_multiplier = 1.0

SAVE_FILE = "save_data.json"

def save_game():
    data= {
        "total_neurotransmitters": total_neurotransmitters,
        "click_multiplier": click_multiplier,
        "nts_per_second": nts_per_second,
        "upgrades": upgrades
        
    }

    with open(SAVE_FILE, "w") as f:
        json.dump(data,f)
    print("Game Saved!")

def load_game():
    global total_neurotransmitters, click_multiplier, nts_per_second
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            total_neurotransmitters = data["total_neurotransmitters"]
            click_multiplier = data["click_multiplier"]
            nts_per_second = data["nts_per_second"]

            for key in upgrades:
                upgrades[key]["level"] = data["upgrades"][key]["level"]
            refresh_ui()
            print("Game_loaded!")
    else:
        print("No saved file found!")

def reset_game():
    global total_neurotransmitters, click_multiplier, nts_per_second
    total_neurotransmitters = 0
    click_multiplier = 1
    nts_per_second = 0
    for key in upgrades:
        upgrades[key]["level"] = 0
    refresh_ui()
    print("Game reset!")



def cycle_fact():
    new_fact = random.choice(facts)
    fact_label.config(text=new_fact)
    root.after(25000, cycle_fact)

#main application window
root = tk.Tk()
neuron_img = Image.open(resource_path("neuron.png")).resize((100, 100))
neuron_photo = ImageTk.PhotoImage(neuron_img)
neuron_img_small = Image.open(resource_path("neuron.png")).resize((95,95))
neuron_photo_small = ImageTk.PhotoImage(neuron_img_small)
root.title("Synapse Clicker")
root.geometry("800x600")
root.configure(bg="#1E1E1E")

milestones = [100, 1000, 10000, 100000, 1000000]
milestones_hit = set()

def check_milestones():
    for m in milestones:
        if total_neurotransmitters >= m and m not in milestones_hit:
            milestones_hit.add(m)
            messagebox.showinfo("Milestone!", f"You've reached {m:,} Neurotransmitters!")

def game_loop():
    global total_neurotransmitters
    total_neurotransmitters += nts_per_second
    refresh_ui()
    check_milestones()
    root.after(1000, game_loop)


#fact bar
fact_bar = tk.Frame(root, bg='#2D2D2D', height=40)
fact_bar.grid(row=0, column=0, columnspan=2, sticky='ew')

#main panel
main_panel = tk.Frame(root, bg='#1E1E1E')
main_panel.grid(row=1, column=0, sticky='nsew')

#shop panel
shop_panel = tk.Frame(root, bg='#2D2D2D')
shop_panel.grid(row=1, column=1, sticky='nsew')

#main content window expands when window resizes
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=3)  # for main panel
root.grid_columnconfigure(1, weight=1)  # for shop panel getting smaller


#VARIABLES
total_neurotransmitters = 0
click_multiplier = 1
nts_per_second = 0

#facts content here
facts = [
    "Did you know that the human brain contains approximately 86 billion neurons? ",
    "Did you know that information in the brain is transmitted at speeds of up to 250 miles per hour? ",
    "Did you know that a single neuron can connect to 10,000 other neurons, forming complex networks? "
]
fact_label = tk.Label(fact_bar, text=facts[0], bg='#2D2D2D', fg='#E0E0E0', font=('helvetica', 14, "bold"))
fact_label.pack(pady=8)

cycle_fact()  # NOW start the calling of the fact: (previous mistake: called the fact inside the function itself lol, causing recursion error)

#main panel content
nt_display = tk.Label(main_panel, text='0', bg='#1E1E1E', fg="#D5E520", font=('helvetica', 40, "bold"))
nt_display.pack(pady=(30, 0))

nt_label = tk.Label(main_panel, text='Neurotransmitters', bg='#1E1E1E', fg='#E0E0E0', font=('helvetica', 14, 'bold'))
nt_label.pack()

rate_label = tk.Label(main_panel, text="(+0.0 NTs/Second)", bg='#1E1E1E', fg="#14C5F1", font=('helvetica', 14, 'bold'))
rate_label.pack(pady=(30, 0))

click_power_label = tk.Label(main_panel, text = "Click power: 1", bg= "#1E1E1E", fg= "#E0E0E0", font=('helvetica', 14, "bold"))
click_power_label.pack()


def refresh_ui():
    nt_display.config(text=f"{int(total_neurotransmitters)}")
    rate_label.config(text=f"(+{nts_per_second:.1f} NTs/Second)")
    click_power_label.config(text=f"Click power: {click_multiplier}")
    for key, widgets in upgrade_widgets.items():
        widgets["level_label"].config(text=f"Level: {upgrades[key]['level']}")
        widgets["cost_label"].config(text=f"Cost: {get_cost(key)} NTs  ")

        cost=get_cost(key)
        if total_neurotransmitters >= cost:
            widgets["buy_button"].config(bg="#00ADB5", fg="#1E1E1E", state="normal")
        else:
            widgets["buy_button"].config(bg="#4A4A4A" , fg = "#8A8A8A", state="disabled") #ts looks so trippy 

def fire_neuron():
    global total_neurotransmitters
    total_neurotransmitters += click_multiplier
    refresh_ui()
    check_milestones()

def on_press(e):
    neuron_button.config(image=neuron_photo_small)
    neuron_button.image = neuron_photo_small

def on_release(e):
    neuron_button.config(image= neuron_photo)
    neuron_button.image = neuron_photo
    fire_neuron()

neuron_button = tk.Label(
    main_panel, image=neuron_photo, bg="#1E1E1E", cursor="hand2" 
)
neuron_button.image = neuron_photo
neuron_button.pack(pady=17)
neuron_button.bind("<ButtonPress-1>", on_press)
neuron_button.bind("<ButtonRelease-1>", on_release)

#i want to make the button darken when it is pressed- because otherwise it looks like it isnt being pressed




#shop content here
shop_title = tk.Label(shop_panel, text="SHOP", bg="#2D2D2D", fg="#E0E0E0", font=("Helvetica", 20, "bold"))
shop_title.pack(pady=15)

#shop data
upgrades = {
    "dendrites": {"name": "Dendrite Branching", "level": 0, "base_cost": 15, "effect": "click"},
    "glial": {"name": "Glial Cell Support", "level": 0, "base_cost": 100, "effect": "passive"},
    "myelin": {"name": "Myelin Sheath", "level": 0, "base_cost": 500, "effect": "multiplier"},
}

#pricing in shop
def get_cost(key):
    data = upgrades[key]
    return int(data["base_cost"] * (1.15 ** data["level"]))

#buy logic
upgrade_widgets = {}

def buy_upgrade(key):
    global total_neurotransmitters, click_multiplier, nts_per_second, base_passive, passive_multiplier
    cost = get_cost(key)
    if total_neurotransmitters >= cost:
        total_neurotransmitters -= cost
        upgrades[key]["level"] += 1

        if upgrades[key]["effect"] == "click":
            click_multiplier += 1
        elif upgrades[key]["effect"] == "passive":
            base_passive += 1
        elif upgrades[key]["effect"] == "multiplier":
            passive_multiplier *= 1.5

        nts_per_second = base_passive * passive_multiplier

        refresh_ui()

for key in upgrades:
    row = tk.Frame(shop_panel, bg="#2D2D2D")
    row.pack(pady=10, padx=10, fill='x')

    name_label = tk.Label(row, text=upgrades[key]["name"], bg="#2D2D2D", fg="#E0E0E0", font=("Helvetica", 16, "bold"))
    name_label.pack(anchor="w")

    level_label = tk.Label(row, text=f"Level: {upgrades[key]['level']}", bg="#2D2D2D", fg="#E0E0E0", font=("Helvetica", 16))
    level_label.pack(anchor="w")

    cost_label = tk.Label(row, text=f"Cost: {get_cost(key)} NTs", bg="#2D2D2D", fg="#E0E0E0", font=("Helvetica", 16))
    cost_label.pack(anchor="w")

    buy_button = tk.Button(row, text="Buy", command=lambda k=key: buy_upgrade(k), bg="#393E46", fg="#E0E0E0")
    buy_button.pack(anchor="w", pady=(4, 0))

    upgrade_widgets[key] = {"level_label": level_label, "cost_label": cost_label, "buy_button": buy_button}

footer = tk.Frame(root, bg="#2D2D2D")
footer.grid(row = 2, column = 0, columnspan = 2, sticky="ew")

save_button = tk.Button(footer, text= "Save Game", command = save_game, bg="#393E46", fg="#E0E0E0", relief="flat", borderwidth=0)
save_button.pack(side="left", padx=10, pady=8)

reset_button = tk.Button(footer, text="Reset", command= reset_game, bg = "#393E46", fg="#E0E0E0", relief="flat", borderwidth = 0)
reset_button.pack(side = "left", padx = 10, pady = 8)

load_button = tk.Button(footer, text = "Load Game", command = load_game, bg = "#393E46", fg="#E0E0E0", relief = "flat", borderwidth = 0)
load_button.pack(side = "right", padx = 10, pady = 8)

game_loop()

def on_closing():
    save_game()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()  # lesson learnt: mainloop should always be last
