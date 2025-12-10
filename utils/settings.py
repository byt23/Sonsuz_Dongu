# utils/settings.py

# --- EKRAN AYARLARI ---
VIRTUAL_WIDTH = 1280
VIRTUAL_HEIGHT = 720
FPS = 60
TILE_SIZE = 80 

# --- SÜRE AYARLARI (YENİ) ---
# Eğer listede olmayan bir level gelirse bu varsayılan süre kullanılır
DEFAULT_DURATION = 10 * 60  # 10 Saniye

# Her Level İçin Özel Süre (Saniye x 60)
LEVEL_DURATIONS = {
    1: 15 * 60,  # Level 1: 15 Saniye (Alışma)
    2: 10 * 60,  # Level 2: 10 Saniye (Hızlı olmalı)
    3: 20 * 60,  # Level 3: 20 Saniye (Daha karmaşık)
    4: 12 * 60,  # Level 4: 12 Saniye
    5: 15 * 60,  # Level 5: 15 Saniye
    6: 25 * 60,  # Level 6: 25 Saniye
    7: 30 * 60   # Level 7: 30 Saniye (Final)
}

# Renkler
COLOR_BG = (20, 20, 30)
COLOR_PLAYER = (50, 200, 50)
COLOR_GHOST = (150, 150, 150)
COLOR_WALL = (80, 80, 100)
COLOR_EXIT = (0, 255, 255)
COLOR_TEXT = (255, 255, 255)

# ID: 1 (Kırmızı)
COLOR_BUTTON_1 = (200, 50, 50)
COLOR_DOOR_1   = (150, 100, 50)

# ID: 2 (Mavi)
COLOR_BUTTON_2 = (50, 50, 200)
COLOR_DOOR_2   = (50, 150, 200)

# ID: 3 (Yeşil)
COLOR_BUTTON_3 = (50, 200, 50)
COLOR_DOOR_3   = (20, 100, 20)

COLOR_DOOR_OPEN = (40, 40, 40)
COLOR_BUTTON_PRESSED = (0, 200, 0)

# STORY TEXTS (ENGLISH)
STORY_TEXTS = {
    1: ["CHAPTER 1: AWAKENING", "", "System: Kronos Protocol v1.0 Initializing...", "Subject 404, consciousness uploaded.", "Your past actions shape your future.", "", "Objective: Solve the Red system and adapt.", "(Press SPACE to Start)"],
    2: ["CHAPTER 2: THE SHADOW", "", "You are not alone. Do you see that gray silhouette?", "That is you. Or what remains of you.", "Clear the path for it, or you both get deleted.", "", "Objective: Have your past self open the door."],
    3: ["CHAPTER 3: BINARY LOGIC", "", "Blue Security Protocol engaged.", "You must now manage two different timelines.", "One holds the Red, while the other passes the Blue.", "", "Objective: Use both systems to reach the exit."],
    4: ["CHAPTER 4: TRUST TEST", "", "The distance between the button and door is too great.", "In the first loop, simply press the button and wait.", "If you don't trust yourself, you will never leave.", "", "Hint: Be patient."],
    5: ["CHAPTER 5: BOTTLENECK", "", "Corridors have narrowed. Collisions create paradoxes.", "You cannot occupy the same space as your past self.", "Make way, step aside, plan ahead.", "", "Caution: Do not touch your ghost."],
    6: ["CHAPTER 6: SYNCHRONIZATION", "", "Timing is everything.", "Two doors must open simultaneously.", "A millisecond error resets the loop.", "", "Objective: Press two buttons at the same time."],
    7: ["CHAPTER 7: FINAL EXAM", "", "The exit is in sight. This is the final hurdle.", "All systems active. All timelines intertwined.", "Pass this, and you will be free... I suppose.", "", "Objective: Combine everything and break the loop."]
}