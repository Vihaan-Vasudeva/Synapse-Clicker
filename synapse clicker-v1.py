import tkinter as tk
import random
import sys, os
import json
from tkinter import messagebox
from tkinter import ttk



def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)  # type: ignore
    return os.path.join(os.path.abspath("."), relative_path)

from PIL import Image, ImageTk

base_passive = 0
passive_multiplier = 1.0



def update_progress_bar():
    next_milestone = next((m for m in milestones if m> total_neurotransmitters), None)
    if next_milestone:
        prev_milestones = 0
        for m in milestones:
            if m<= total_neurotransmitters:
                prev_milestones = m
        progress = (total_neurotransmitters - prev_milestones)/ (next_milestone - prev_milestones) * 100
        progress_bar["value"] = progress
        progress_label.config(text = f"{int(total_neurotransmitters)}/ {next_milestone:,} to next milestone")
    else:
        progress_bar["value"] = 100
        progress_label.config(text = "All milestones reached!!")




SAVE_FILE = "save_data.json"

def save_game():
    data = {
    "total_neurotransmitters": total_neurotransmitters,
    "click_multiplier": click_multiplier,
    "nts_per_second": nts_per_second,
    "crit_chance": crit_chance,
    "base_passive": base_passive,
    "passive_multiplier": passive_multiplier,
    "total_clicks": total_clicks,
    "critical_hits":critical_hits,
    "achievements_unlocked": list(achievements_unlocked), 
    "milestones_hit": list(milestones_hit),
    "upgrades": upgrades,
}

    with open(SAVE_FILE, "w") as f:
        json.dump(data,f)
    print("Game Saved!")

def load_game():
    global total_neurotransmitters, click_multiplier, nts_per_second, crit_chance, base_passive, passive_multiplier, total_clicks, critical_hits, achievements_unlocked, milestones_hit
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            total_neurotransmitters = data["total_neurotransmitters"]
            click_multiplier = data["click_multiplier"]
            nts_per_second = data["nts_per_second"]
            crit_chance = data.get("crit_chance", 0.10)
            base_passive = data.get("base_passive", 0)
            passive_multiplier = data.get("passive_multiplier", 1.0)

            total_clicks = data.get ("total_clicks", 0)
            critical_hits = data.get("critical_hits", 0)

            achievements_unlocked = set(data.get("achievements_unlocked", []))
            milestones_hit = set(data.get("milestones_hit", []))

            for key in upgrades:
                upgrades[key]["level"] = data["upgrades"][key]["level"]
            update_neuron_size()
            refresh_ui()
            print("Game_loaded!")
    else:
        print("No saved file found!")

def reset_game():
    global total_neurotransmitters, click_multiplier, nts_per_second, base_passive, passive_multiplier, crit_chance, total_clicks, critical_hits, achievements_unlocked, milestones_hit
    total_neurotransmitters = 0
    click_multiplier = 1
    nts_per_second = 0
    base_passive = 0
    passive_multiplier = 1.0
    crit_chance = 0.10
    total_clicks = 0
    critical_hits = 0
    achievements_unlocked = set()
    milestones_hit = set()
    for key in upgrades:
        upgrades[key]["level"] = 0
    update_neuron_size()
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
root.geometry("840x640")
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

#main content window expands when window resizes, ai suggestion
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=3)  # for main panel
root.grid_columnconfigure(1, weight=1)  # for shop panel getting smaller


#VARIABLES
crit_chance = 0.10 #base chance fyi
crit_multiplier = 3
total_neurotransmitters = 0
click_multiplier = 1
nts_per_second = 0
total_clicks = 0
critical_hits = 0
achievements_unlocked = set()

#facts content here
facts = [
    "Did you know that the human brain contains approximately 86 billion neurons? ",
    "Did you know that information in the brain is transmitted at speeds of up to 250 miles per hour? ",
    "Did you know that the neurons communicate using both electricaland chemical signals?",
    "Did you know that a single neuron can connect to 10,000 other neurons, forming complex networks? ",
    "Did you know that glial cells outnumber neurons in the brain and support, protect and nourish them?",
    "Did you know that action potentials, the electrical signals neurons fire, follow a all or nothing rule?",
    "Did you know that a resting neuron maintains a electrical charge across its membrane, ready to fire at any moment?",
    "Did you know that the brain continues forming new neurons in adulthood, a process called neurogenesis?",
    #idts anyone will play long enough to see all of em lmao
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

crit_label_stat = tk.Label(main_panel, text = "Crit Chance: 10%", bg = "#1E1E1E", fg = "#FF6B6B", font = ("helvetica", 14, "bold"))
crit_label_stat.pack()

progress_bar = ttk.Progressbar(main_panel, length = 200, mode="determinate", maximum = 100)
progress_bar.pack(pady=(10,0))

progress_label = tk.Label(main_panel, text="", bg = "#1E1E1E", fg = "#8A8A8A", font = ("Helvetica", 12, "bold"))
progress_label.pack()

def check_achievements():
    for name, condition in achievements.items():
        if name not in achievements_unlocked and condition():
            achievements_unlocked.add(name)
            messagebox.showinfo(
                "Achievement Unlocked!", f" {name}"
            )
def show_achievements():
    print(achievements)
    window = tk.Toplevel(root)
    window.title("Achievements")
    window.geometry("410x250")
    window.configure(bg="#1E1E1E")

    title = tk.Label(
        window,
        text="Achievements", bg="#1E1E1E", fg = "#D5E520", font=("Helvetica", 18, "bold")
    )
    title.pack(pady=15)

    for name in achievements:
        unlocked = name in achievements_unlocked

        label = tk.Label(
            window,
            text=("✓ " if unlocked else "⬜ ") + name,
            bg = "#1E1E1E", fg = "#E0E0E0" if unlocked else "#777777", anchor = "w", font=("Helvetica", 14, "bold")
        )
        label.pack(fill = "x", padx=25, pady=4)





def refresh_ui():
    nt_display.config(text=f"{int(total_neurotransmitters)}")
    rate_label.config(text=f"(+{nts_per_second:.1f} NTs/Second)")
    click_power_label.config(text=f"Click power: {click_multiplier}")
    crit_label_stat.config(text=f"Crit Chance: {int(crit_chance*100)}%")
    for key, widgets in upgrade_widgets.items():
        widgets["level_label"].config(text=f"Level: {upgrades[key]['level']}")
        widgets["cost_label"].config(text=f"Cost: {get_cost(key)} NTs  ")

        cost=get_cost(key)
        if total_neurotransmitters >= cost:
            widgets["buy_button"].config(bg="#00ADB5", fg="#1E1E1E", state="normal")
        else:
            widgets["buy_button"].config(bg="#4A4A4A" , fg = "#8A8A8A", state="disabled") #ts looks so trippy 
    update_progress_bar()

def show_floating_number(amount, is_crit):
    color = "#FF6B6B" if is_crit else "#00ADB5"
    label = tk.Label(main_panel, text=f"+ {amount}", bg= "#1E1E1E", fg = color, font=("Helvetica", 14, "bold"))
    label.place(relx=0.5, rely = 0.60, anchor= "center")

    def animate(step=0):
        if step < 15:
            label.place(relx = 0.5, rely = 0.60 - (step*0.01), anchor = "center")
            root.after(30, lambda: animate(step+1))
        else:
            label.destroy()

    animate()
    
def show_crit_feedback():
    crit_label = tk.Label(main_panel, text = "Critical Hit!", bg="#1E1E1E", fg = "#FF6B6B", font=("Helvetica", 16, "bold"))
    crit_label.place(relx=0.5, rely=0.47, anchor="center")
    root.after(500, crit_label.destroy)

def update_neuron_size():
    global neuron_photo, neuron_photo_small
    total_levels = sum(upgrades[key]["level"] for key in upgrades)
    base_size = 100 + min(total_levels*3, 60) #ive set max to 60 px
    small_size = base_size - 5

    resized = Image.open(resource_path("neuron.png")). resize((base_size, base_size))
    neuron_photo = ImageTk.PhotoImage(resized)
    resized_small = Image.open(resource_path("neuron.png")). resize((small_size, small_size))
    neuron_photo_small = ImageTk.PhotoImage(resized_small)

    neuron_button.config(image = neuron_photo)
    neuron_button.image = neuron_photo  # type: ignore

def fire_neuron():
    global total_neurotransmitters, total_clicks, critical_hits
    is_crit = random.random() < crit_chance
    total_clicks +=1

    if is_crit:
        critical_hits += 1
    gain = click_multiplier * crit_multiplier if is_crit else click_multiplier

    total_neurotransmitters += gain
    refresh_ui()
    check_milestones()
    show_floating_number(gain, is_crit)
    if is_crit:
        show_crit_feedback()

    check_achievements()
        

def on_press(e):
    neuron_button.config(image=neuron_photo_small)
    neuron_button.image = neuron_photo_small  # type: ignore

def on_release(e):
    neuron_button.config(image= neuron_photo)
    neuron_button.image = neuron_photo  # type: ignore
    fire_neuron()

neuron_button = tk.Label(
    main_panel, image=neuron_photo, bg="#1E1E1E", cursor="hand2" 
)
neuron_button.image = neuron_photo  # type: ignore
neuron_button.pack(pady=(45, 17))
neuron_button.bind("<ButtonPress-1>", on_press)
neuron_button.bind("<ButtonRelease-1>", on_release)


def buy_upgrade(key):
    global total_neurotransmitters, click_multiplier, nts_per_second, base_passive, passive_multiplier, crit_chance
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
        elif upgrades[key]["effect"] == "crit_chance":
            crit_chance += 0.05

        nts_per_second = base_passive * passive_multiplier

        refresh_ui()
        update_neuron_size()
        check_achievements()
        


#shop content here
shop_title = tk.Label(shop_panel, text="SHOP", bg="#2D2D2D", fg="#E0E0E0", font=("Helvetica", 20, "bold"))
shop_title.pack(pady=15)

#shop data
upgrades = {
    "dendrites": {"name": "Dendrite Branching", "level": 0, "base_cost": 15, "effect": "click"},
    "glial": {"name": "Glial Cell Support", "level": 0, "base_cost": 100, "effect": "passive"},
    "myelin": {"name": "Myelin Sheath", "level": 0, "base_cost": 500, "effect": "multiplier"},
    "plasticity":{"name":"Synaptic Plasticity", "level": 0, "base_cost": 250, "effect": "crit_chance"},
}

achievements = {
    "First Clicks": lambda: total_clicks >= 5,
    "Click Frenzy- Get 500 Clicks": lambda: total_clicks >= 500,
    "Critical Thinker- Get 50 Critical hits": lambda:critical_hits >= 50,
    "Growing Netwrok- Get 25 Upgrades": lambda:sum(upgrades[k]["level"] for k in upgrades) >= 25,
    "Millionaire Brain- Get 1 million Neurotransmitters": lambda:total_neurotransmitters >= 1000000,
}

#pricing in shop
def get_cost(key):
    data = upgrades[key]
    return int(data["base_cost"] * (1.15 ** data["level"]))

#buy logic
upgrade_widgets = {}


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

achievements_button= tk.Button(
    footer, text = "Achievements", command = show_achievements, bg = "#393E46", fg="#E0E0E0", relief = "flat", borderwidth=0
    )
achievements_button.pack(side="left", padx=10, pady=8)

load_button = tk.Button(footer, text = "Load Game", command = load_game, bg = "#393E46", fg="#E0E0E0", relief = "flat", borderwidth = 0)
load_button.pack(side = "right", padx = 10, pady = 8)

game_loop()

def on_closing():
    save_game()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)


root.mainloop()  # lesson learnt: mainloop should always be las