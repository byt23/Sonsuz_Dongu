# utils/settings.py

# --- EKRAN AYARLARI ---
VIRTUAL_WIDTH = 1280
VIRTUAL_HEIGHT = 720

FPS = 60
TILE_SIZE = 80 
LOOP_DURATION = 300

# Renkler (Aynı)
COLOR_BG = (20, 20, 30)
COLOR_PLAYER = (50, 200, 50)
COLOR_GHOST = (150, 150, 150)
COLOR_WALL = (80, 80, 100)
COLOR_EXIT = (0, 255, 255)
COLOR_TEXT = (255, 255, 255)

COLOR_BUTTON_1 = (200, 50, 50)
COLOR_DOOR_1   = (150, 100, 50)
COLOR_BUTTON_2 = (50, 50, 200)
COLOR_DOOR_2   = (50, 150, 200)
COLOR_DOOR_OPEN = (40, 40, 40)
COLOR_BUTTON_PRESSED = (0, 200, 0)

# --- ENGLISH STORY TEXTS ---
STORY_TEXTS = {
    1: [
        "CHAPTER 1: AWAKENING",
        "",
        "System: Kronos Protocol v1.0 Initializing...",
        "Subject 404, consciousness uploaded.",
        "Your past actions shape your future.",
        "",
        "Objective: Solve the Red system and adapt.",
        "(Press SPACE to Start)"
    ],
    2: [
        "CHAPTER 2: THE SHADOW",
        "",
        "You are not alone. Do you see that gray silhouette?",
        "That is you. Or what remains of you.",
        "Clear the path for it, or you both get deleted.",
        "",
        "Objective: Have your past self open the door.",
    ],
    3: [
        "CHAPTER 3: BINARY LOGIC",
        "",
        "Blue Security Protocol engaged.",
        "You must now manage two different timelines.",
        "One holds the Red, while the other passes the Blue.",
        "",
        "Objective: Use both systems to reach the exit.",
    ],
    4: [
        "CHAPTER 4: TRUST TEST",
        "",
        "The distance between the button and door is too great.",
        "In the first loop, simply press the button and wait.",
        "If you don't trust yourself, you will never leave.",
        "",
        "Hint: Be patient.",
    ],
    5: [
        "CHAPTER 5: BOTTLENECK",
        "",
        "Corridors have narrowed. Collisions create paradoxes.",
        "You cannot occupy the same space as your past self.",
        "Make way, step aside, plan ahead.",
        "",
        "Caution: Do not touch your ghost.",
    ],
    6: [
        "CHAPTER 6: SYNCHRONIZATION",
        "",
        "Timing is everything.",
        "Two doors must open simultaneously.",
        "A millisecond error resets the loop.",
        "",
        "Objective: Press two buttons at the same time.",
    ],
    7: [
        "CHAPTER 7: FINAL EXAM (PART 1 END)",
        "",
        "The exit is in sight. This is the final hurdle.",
        "All systems active. All timelines intertwined.",
        "Pass this, and you will be free... I suppose.",
        "",
        "Objective: Combine everything and break the loop.",
    ]
}