import pygame

# --- EKRAN AYARLARI ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TILE_SIZE = 80  # 40 idealdir, haritanın ekrana sığmasını sağlar.

VIRTUAL_WIDTH = SCREEN_WIDTH
VIRTUAL_HEIGHT = SCREEN_HEIGHT

# --- SÜRE AYARLARI (Saniye * 60) ---
DEFAULT_DURATION = 30 * 60 

LEVEL_DURATIONS = {
    1: 20 * 60,   # 20 Saniye
    2: 25 * 60,   
    3: 30 * 60,
    4: 35 * 60,
    5: 40 * 60,
    6: 45 * 60,
    7: 50 * 60,
    8: 60 * 60,
    9: 60 * 60,
    10: 70 * 60,
    11: 75 * 60,
    12: 80 * 60,
    13: 90 * 60,
    14: 100 * 60,
    15: 120 * 60 
}

# --- RENKLER ---
COLOR_BG = (20, 20, 30)
COLOR_PLAYER = (50, 200, 50)
COLOR_GHOST = (100, 100, 255)
COLOR_WALL = (120, 120, 120)
COLOR_EXIT = (0, 255, 255)
COLOR_TEXT = (255, 255, 255)
COLOR_BOX = (200, 140, 40)
COLOR_LASER = (255, 0, 0)
COLOR_BUTTON_PRESSED = (80, 80, 80)

# Mekanik Renkleri (ViewModel bunu kullanır)
COLORS_MECHANICS = {
    1: {'btn': (200, 50, 50),   'door': (150, 100, 50)},   # Kırmızı
    2: {'btn': (50, 50, 200),   'door': (50, 150, 200)},   # Mavi
    3: {'btn': (255, 215, 0),   'door': (180, 150, 0)},    # Sarı
    4: {'btn': (255, 105, 180), 'door': (180, 60, 120)},   # Pembe
    5: {'btn': (160, 32, 240),  'door': (100, 20, 150)}    # Mor
}

# Uyumluluk için
COLOR_BUTTON_1 = COLORS_MECHANICS[1]['btn']; COLOR_DOOR_1 = COLORS_MECHANICS[1]['door']
COLOR_BUTTON_2 = COLORS_MECHANICS[2]['btn']; COLOR_DOOR_2 = COLORS_MECHANICS[2]['door']
COLOR_BUTTON_3 = COLORS_MECHANICS[3]['btn']; COLOR_DOOR_3 = COLORS_MECHANICS[3]['door']
COLOR_BUTTON_4 = COLORS_MECHANICS[4]['btn']; COLOR_DOOR_4 = COLORS_MECHANICS[4]['door']
COLOR_BUTTON_5 = COLORS_MECHANICS[5]['btn']; COLOR_DOOR_5 = COLORS_MECHANICS[5]['door']
COLOR_DOOR_OPEN = (40, 40, 40)

# STORY TEXTS (ENGLISH)
"""STORY_TEXTS = {
    1: ["CHAPTER 1: AWAKENING", "", "System: Kronos Protocol v1.0 Initializing...", "Subject 404, consciousness uploaded.", "Your past actions shape your future.", "", "Objective: Solve the Red system and adapt.", "(Press SPACE to Start)"],
    2: ["CHAPTER 2: THE SHADOW", "", "You are not alone. Do you see that gray silhouette?", "That is you. Or what remains of you.", "Clear the path for it, or you both get deleted.", "", "Objective: Have your past self open the door."],
    3: ["CHAPTER 3: BINARY LOGIC", "", "Blue Security Protocol engaged.", "You must now manage two different timelines.", "One holds the Red, while the other passes the Blue.", "", "Objective: Use both systems to reach the exit."],
    4: ["CHAPTER 4: TRUST TEST", "", "The distance between the button and door is too great.", "In the first loop, simply press the button and wait.", "If you don't trust yourself, you will never leave.", "", "Hint: Be patient."],
    5: ["CHAPTER 5: BOTTLENECK", "", "Corridors have narrowed. Collisions create paradoxes.", "You cannot occupy the same space as your past self.", "Make way, step aside, plan ahead.", "", "Caution: Do not touch your ghost."],
    6: ["CHAPTER 6: SYNCHRONIZATION", "", "Timing is everything.", "Two doors must open simultaneously.", "A millisecond error resets the loop.", "", "Objective: Press two buttons at the same time."],
    7: ["CHAPTER 7: FINAL EXAM", "", "The exit is in sight. This is the final hurdle.", "All systems active. All timelines intertwined.", "Pass this, and you will be free... I suppose.", "", "Objective: Combine everything and break the loop."],
    8: ["CHAPTER 8: GLITCH", "", "Kronos AI: Error #092 detected.", "Why are you still here?", "The loop is destabilizing.", "", "Objective: Move fast."],
    9: ["CHAPTER 9: OVERLOAD", "", "Kronos AI: Processing power diverted.", "More buttons, less time.", "Coordinate or be deleted.", "", "Objective: Multitasking."],
    10: ["CHAPTER 10: MEMORY LEAK", "", "Kronos AI: I remember the others.", "They all failed here.", "Prove you are different.", "", "Objective: Don't panic."],
    11: ["CHAPTER 11: THE LOOP", "", "Kronos AI: Doing the same thing twice...", "...expecting a different result.", "Is that insanity? Or strategy?", "", "Objective: Repetition."],
    12: ["CHAPTER 12: CORRUPTION", "", "Kronos AI: Accessing core files...", "Warning: Reality breach.", "Trust no one. Not even yourself.", "", "Objective: Synchronization."],
    13: ["CHAPTER 13: BREAKDOWN", "", "Kronos AI: S-Stop... it...", "You are hurting the... system.", "I cannot hold the timeline.", "", "Objective: Push the limits."],
    14: ["CHAPTER 14: THE SOURCE", "", "Kronos AI: Firewall breached.", "One last barrier remains.", "Combine everything you learned.", "", "Objective: The penultimate test."],
    15: ["CHAPTER 15: TERMINATION", "", "Kronos AI: FATAL ERROR.", "Subject 404 is uncontrollable.", "RESETTING SIMULATION...", "UNLESS... YOU BREAK OUT.", "", "Objective: FREEDOM."]
}"""