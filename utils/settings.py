# utils/settings.py

# --- GÜNCELLEME: ZOOM ETKİSİ İÇİN TILE_SIZE = 80 ---
VIRTUAL_WIDTH = 1280
VIRTUAL_HEIGHT = 720
FPS = 60
TILE_SIZE = 80 # <-- BURASI 80 YAPILDI!
LOOP_DURATION = 450

# Renkler (Aynı kalıyor)
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

# --- 7 BÖLÜMLÜK HİKAYE METİNLERİ ---
STORY_TEXTS = {
    1: [
        "SEVIYE 1: BASLANGIC", "", "Denek 404, Kronos Simulasyonuna hos geldin.",
        "Gecmisteki hareketlerin, gelecegini sekillendirir.",
        "", "Gorev: Kirmizi sistemi coz ve alis.",
        "(Baslamak icin SPACE tusuna bas)"
    ],
    2: [
        "SEVIYE 2: GOLGE", "", "Gecmiste yaptigin her hareket kayit altinda.",
        "Ona yol ac, yoksa ikiniz de silinirsiniz.",
        "", "Gorev: Gecmisteki haline kapiyi actir.",
    ],
    3: [
        "SEVIYE 3: IKILI MANTIK", "", "Mavi Guvenlik Protokolu devrede.",
        "Biri kirmiziyi tutarken, digeri maviyi gececek.",
        "", "Gorev: Iki sistemi de kullanarak cikisa ulas.",
    ],
    4: [
        "SEVIYE 4: GUVEN TESTI", "", "Buton ve kapi arasindaki mesafe cok fazla.",
        "Ilk turda sadece butona bas ve bekle. Kendine guven.",
        "", "Ipucu: Sabirli ol.",
    ],
    5: [
        "SEVIYE 5: DARBOGAZ", "", "Koridorlar daraldi. Carpismalar paradoks yaratir.",
        "Gecmisteki halinle ayni karede duramazsin.",
        "", "Dikkat: Hayaletine dokunma.",
    ],
    6: [
        "SEVIYE 6: SENKRON", "", "Zamanlama her seydir. Iki kapi ayni anda acilmak zorunda.",
        "Milisaniyelik bir hata, donguyu basa sarar.",
        "", "Gorev: Ayni anda iki butona bas.",
    ],
    7: [
        "SEVIYE 7: SON SINAV", "", "Cikis kapisi gorundu. Bu son engel.",
        "Tum sistemler aktif. Tum zamanlar ic ice.",
        "Bunu gecersen ozgur kalacaksin... sanirim.",
        "", "Gorev: Hepsini birlestir ve donguyu kir.",
    ]
}