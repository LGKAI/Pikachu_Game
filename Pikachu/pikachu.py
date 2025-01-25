import pygame, sys, random, copy, time, collections, os, json
from pygame.locals import *
from datetime import datetime

"""Đặt các cấu hình mặc định"""
FPS = 60
WINDOWWIDTH = 1400
WINDOWHEIGHT = 680
BOXSIZE = 55
BOARDWIDTH = 14
BOARDHEIGHT = 9
NUMHEROES_ONBOARD = 21
NUMSAMEHEROES = 4
TIMEBAR_LENGTH = 300
TIMEBAR_WIDTH = 30
LEVELMAX = 5
LIVES = 10
GAMETIME = 400
GETHINTTIME = 20
SOUND_ON = True 
LEVEL = 1 
XMARGIN = (WINDOWWIDTH - (BOXSIZE * BOARDWIDTH)) // 2
YMARGIN = (WINDOWHEIGHT - (BOXSIZE * BOARDHEIGHT)) // 2
# set up the colors
GRAY = (100, 100, 100)
NAVYBLUE = ( 60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
BOLDGREEN = (0, 175, 0)
BLUE = ( 0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = ( 0, 255, 255)
BLACK = (0, 0, 0)
BGCOLOR = NAVYBLUE
HIGHLIGHTCOLOR = BLUE
BORDERCOLOR = RED
SKIN_COLOR = (255, 228, 196)
# TIMEBAR setup
barPos = (WINDOWWIDTH // 2 - TIMEBAR_LENGTH // 2, YMARGIN // 2 - TIMEBAR_WIDTH // 2)
barSize = (TIMEBAR_LENGTH, TIMEBAR_WIDTH)
borderColor = WHITE
barColor = BOLDGREEN
ACCOUNTS_FILE = "User_data/accounts.json"
# Load pictures
aegis = pygame.image.load('Resources/others/aegis_2.jpg')
aegis = pygame.transform.scale(aegis, (45, 45))
pygame.font.init()
# Load background
startBG = pygame.image.load('Resources/Background/startBG.jpg')
startBG = pygame.transform.scale(startBG, (WINDOWWIDTH, WINDOWHEIGHT))
BG = pygame.image.load('Resources/Background/main.png')
BG = pygame.transform.scale(BG, (WINDOWWIDTH, WINDOWHEIGHT))
# Load sound and musicbbb
pygame.mixer.pre_init()
pygame.mixer.init()
clickSound = pygame.mixer.Sound('Resources/sound_effect/click_selecting.mp3')
getPointSound = pygame.mixer.Sound('Resources/sound_effect/victory.mp3')
WrongSound = pygame.mixer.Sound('Resources/sound_effect/wrong.mp3')
startScreenSound = pygame.mixer.Sound('Resources/sound_effect/warriors-of-the-night-assemble.wav')
listMusicBG = ["Resources/BGmusic/" + i for i in os.listdir("Resources/BGmusic")]


"""Xử lý đăng kí, đăng nhập tài khoản"""

def showLoginScreen():
    """Hiển thị màn hình đăng nhập"""
    login_font = pygame.font.SysFont('comicsansms', 50)
    input_font = pygame.font.SysFont('comicsansms', 40)
    button_font = pygame.font.SysFont('comicsansms', 45)
    username = ""
    password = ""
    active_field = "username"
    error_message = ""
    
    # Kích thước và tọa độ các thành phần
    field_width = 400
    field_height = 50
    label_offset_x = 80
    text_offset_y = -2
    button_width = 250
    button_height = 60
    button_font = pygame.font.SysFont('comicsansms', 45)
    back_button_rect = pygame.Rect(10, 10, 120, 50)
    back_button_text = button_font.render("BACK", True, WHITE)
    back_button_text_rect = back_button_text.get_rect(center=back_button_rect.center)
    while True:
        # Vẽ nền trắng
        DISPLAYSURF.fill(WHITE)

        # Tiêu đề
        title_text = login_font.render("LOGIN", True, (255, 0, 0))  # Chữ đỏ
        title_rect = title_text.get_rect(center=(WINDOWWIDTH // 2, 100))
        DISPLAYSURF.blit(title_text, title_rect)

        # Nhãn và trường nhập
        username_label = input_font.render("Username:", True, (255, 0, 0))  # Chữ đỏ
        username_label_rect = username_label.get_rect(midright=(WINDOWWIDTH // 2 - field_width // 2 - label_offset_x, 200 + field_height // 2))
        username_rect = pygame.Rect(WINDOWWIDTH // 2 - field_width // 2, 200, field_width, field_height)

        password_label = input_font.render("Password:", True, (255, 0, 0))  # Chữ đỏ
        password_label_rect = password_label.get_rect(midright=(WINDOWWIDTH // 2 - field_width // 2 - label_offset_x, 300 + field_height // 2))
        password_rect = pygame.Rect(WINDOWWIDTH // 2 - field_width // 2, 300, field_width, field_height)

        # Vẽ nhãn và trường nhập
        DISPLAYSURF.blit(username_label, username_label_rect)
        pygame.draw.rect(DISPLAYSURF, BLACK, username_rect, 2)
        DISPLAYSURF.blit(input_font.render(username, True, BLACK), (username_rect.x + 10, username_rect.y + text_offset_y))

        DISPLAYSURF.blit(password_label, password_label_rect)
        pygame.draw.rect(DISPLAYSURF, BLACK, password_rect, 2)
        DISPLAYSURF.blit(input_font.render("*" * len(password), True, BLACK), (password_rect.x + 10, password_rect.y + text_offset_y))

        # Nút LOGIN
        login_button_rect = pygame.Rect(WINDOWWIDTH // 2 - button_width // 2, 400, button_width, button_height)
        pygame.draw.rect(DISPLAYSURF, BLACK, login_button_rect)
        login_button_text = button_font.render("LOGIN", True, (255, 0, 0))  # Chữ đỏ
        login_button_text_rect = login_button_text.get_rect(center=login_button_rect.center)
        DISPLAYSURF.blit(login_button_text, login_button_text_rect)

        # Thông báo lỗi (nếu có)
        if error_message:
            error_text = input_font.render(error_message, True, RED)
            error_rect = error_text.get_rect(center=(WINDOWWIDTH // 2, 500))
            DISPLAYSURF.blit(error_text, error_rect)
        pygame.draw.rect(DISPLAYSURF, BLACK, back_button_rect)
        DISPLAYSURF.blit(back_button_text, back_button_text_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if active_field == "username":
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode
                elif active_field == "password":
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    else:
                        password += event.unicode
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if username_rect.collidepoint(mousex, mousey):
                    active_field = "username"
                elif password_rect.collidepoint(mousex, mousey):
                    active_field = "password"
                elif login_button_rect.collidepoint(mousex, mousey):
                    if check_login(username, password):
                        return
                    else:
                        error_message = "Invalid username or password"
                elif back_button_rect.collidepoint(mousex, mousey):
                    return main()





def check_login(username, password):
    """Kiểm tra thông tin đăng nhập"""
    global USER, USER_NAME
    try:
        with open(ACCOUNTS_FILE, "r") as f:
            accounts = json.load(f)

        # Kiểm tra xem `username` có tồn tại trong `accounts` không
        user_data = accounts.get(username.lower())
        if user_data and user_data.get("password") == str(len(username)) + username.lower() + str(len(password)) + password.lower():
            USER = user_data
            USER_NAME = username.lower()
            return True
        else:
            return False
    except FileNotFoundError:
        # File không tồn tại
        print("Error: Accounts file not found.")
        return False
    except json.JSONDecodeError:
        # File JSON không hợp lệ
        print("Error: Invalid JSON format in accounts file.")
        return False
    except Exception as e:
        # Xử lý các lỗi không mong đợi khác
        print(f"Unexpected error: {e}")
        return False

def register_account(username, password):
    """Xử lý đăng ký tài khoản"""
    global USER, USER_NAME
    try:
        with open(ACCOUNTS_FILE, "r") as f:
            accounts = json.load(f)
    except FileNotFoundError:
        accounts = {}

    if username.lower() in accounts:
        return False  # Tên tài khoản đã tồn tại
    accounts[username.lower()] = {"password":str(len(username)) + username.lower() + str(len(password)) + password.lower(), "Board":getRandomizedBoard(), "Score": 0, "Level": 1}
    USER = accounts[username.lower()]
    USER_NAME = username.lower()
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump(accounts, f, indent = 4)
    return True

def showRegisterScreen():
    """Màn hình đăng kí"""
    login_font = pygame.font.SysFont('comicsansms', 50)
    input_font = pygame.font.SysFont('comicsansms', 40)
    button_font = pygame.font.SysFont('comicsansms', 45)
    username = ""
    password = ""
    active_field = "username"
    message = ""

    # Kích thước và tọa độ các thành phần
    field_width = 400
    field_height = 50
    label_offset_x = 80  # Khoảng cách giữa nhãn và khung nhập
    text_offset_y = -5  # Điều chỉnh nhích chữ lên trên khung nhập
    button_width = 250
    button_height = 60
    back_button_rect = pygame.Rect(10, 10, 120, 50)
    back_button_text = button_font.render("BACK", True, WHITE)
    back_button_text_rect = back_button_text.get_rect(center=back_button_rect.center)
    while True:
        DISPLAYSURF.fill(WHITE)

        # Tiêu đề
        title_text = login_font.render("REGISTER", True, BLACK)
        title_rect = title_text.get_rect(center=(WINDOWWIDTH // 2, 100))
        DISPLAYSURF.blit(title_text, title_rect)

        # Nhãn và trường nhập cho Username
        username_label = input_font.render("Username:", True, BLACK)
        username_label_rect = username_label.get_rect(midright=(WINDOWWIDTH // 2 - field_width // 2 - label_offset_x, 200 + field_height // 2))
        username_rect = pygame.Rect(WINDOWWIDTH // 2 - field_width // 2, 200, field_width, field_height)

        # Nhãn và trường nhập cho Password
        password_label = input_font.render("Password:", True, BLACK)
        password_label_rect = password_label.get_rect(midright=(WINDOWWIDTH // 2 - field_width // 2 - label_offset_x, 300 + field_height // 2))
        password_rect = pygame.Rect(WINDOWWIDTH // 2 - field_width // 2, 300, field_width, field_height)

        # Vẽ nhãn và trường nhập
        DISPLAYSURF.blit(username_label, username_label_rect)
        pygame.draw.rect(DISPLAYSURF, BLACK, username_rect, 2)
        DISPLAYSURF.blit(input_font.render(username, True, BLACK), (username_rect.x + 10, username_rect.y + text_offset_y))

        DISPLAYSURF.blit(password_label, password_label_rect)
        pygame.draw.rect(DISPLAYSURF, BLACK, password_rect, 2)
        DISPLAYSURF.blit(input_font.render("*" * len(password), True, BLACK), (password_rect.x + 10, password_rect.y + text_offset_y))

        # Nút REGISTER
        register_button_rect = pygame.Rect(WINDOWWIDTH // 2 - button_width // 2, 400, button_width, button_height)
        pygame.draw.rect(DISPLAYSURF, BLACK, register_button_rect)
        register_button_text = button_font.render("REGISTER", True, WHITE)
        register_button_text_rect = register_button_text.get_rect(center=register_button_rect.center)
        DISPLAYSURF.blit(register_button_text, register_button_text_rect)

        # Thông báo (nếu có)
        if message:
            message_text = input_font.render(message, True, RED)
            message_rect = message_text.get_rect(center=(WINDOWWIDTH // 2, 500))
            DISPLAYSURF.blit(message_text, message_rect)

        # Nút BACK
        pygame.draw.rect(DISPLAYSURF, BLACK, back_button_rect)
        DISPLAYSURF.blit(back_button_text, back_button_text_rect)
        

        pygame.display.update()

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if active_field == "username":
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode
                elif active_field == "password":
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    else:
                        password += event.unicode
            elif event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                if username_rect.collidepoint(mousex, mousey):
                    active_field = "username"
                elif password_rect.collidepoint(mousex, mousey):
                    active_field = "password"
                elif register_button_rect.collidepoint(mousex, mousey):
                    if register_account(username, password):
                        message = "Registration successful!"
                        return
                    else:
                        message = "Username already exists!"
                elif back_button_rect.collidepoint(mousex, mousey):
                    return main()


# Hàm vẽ màn hình đăng nhập
def showMainAuthScreen():
    """Hiển thị màn hình đăng nhập, đăng ký"""
    login_font = pygame.font.SysFont('comicsansms', 50)
    button_font = pygame.font.SysFont('comicsansms', 45)

    while True:
        DISPLAYSURF.fill(WHITE)

        # Hiển thị tiêu đề
        title_text = login_font.render("WELCOME", True, BLACK)
        title_rect = title_text.get_rect(center=(WINDOWWIDTH // 2, 100))
        DISPLAYSURF.blit(title_text, title_rect)

        # Nút Đăng nhập
        login_button = button_font.render("LOGIN", True, WHITE)
        login_button_rect = pygame.Rect(WINDOWWIDTH // 2 - 150, 200, 300, 60)
        pygame.draw.rect(DISPLAYSURF, BLACK, login_button_rect)
        DISPLAYSURF.blit(login_button, login_button_rect.move(80, 5))

        # Nút Đăng ký
        register_button = button_font.render("REGISTER", True, WHITE)
        register_button_rect = pygame.Rect(WINDOWWIDTH // 2 - 150, 300, 300, 60)
        pygame.draw.rect(DISPLAYSURF, BLACK, register_button_rect)
        DISPLAYSURF.blit(register_button, register_button_rect.move(60, 5))

        pygame.display.update()

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                if login_button_rect.collidepoint(mousex, mousey):
                    showLoginScreen()  # Hiển thị màn hình đăng nhập
                elif register_button_rect.collidepoint(mousex, mousey):
                    showRegisterScreen()  # Hiển thị màn hình đăng ký
                return False


"""Màn hình khởi đầu và các nút"""

def showStartScreen():
    startScreenSound.play()
    while True:
        DISPLAYSURF.blit(startBG, (0, 0))
        newGameSurf = BASICFONT.render('NEW GAME', True, YELLOW, BLACK)
        newGameRect = newGameSurf.get_rect()
        newGameRect.center = (WINDOWWIDTH // 2, 4 * WINDOWHEIGHT // 8)
        DISPLAYSURF.blit(newGameSurf, newGameRect)
        pygame.draw.rect(DISPLAYSURF, BLACK, newGameRect, 4)
        SettingSurf = BASICFONT.render('SETTINGS', True, YELLOW, BLACK)
        SettingRect = SettingSurf.get_rect()
        SettingRect.center = (WINDOWWIDTH // 2, 5 * WINDOWHEIGHT // 8)
        DISPLAYSURF.blit(SettingSurf, SettingRect)
        pygame.draw.rect(DISPLAYSURF, BLACK, SettingRect, 4)
        ContinueSurf = BASICFONT.render('CONTINUE', True, YELLOW, BLACK)
        ContinueRect = ContinueSurf.get_rect()
        ContinueRect.center = (WINDOWWIDTH // 2, 3 * WINDOWHEIGHT // 8)
        DISPLAYSURF.blit(ContinueSurf, ContinueRect)
        pygame.draw.rect(DISPLAYSURF, BLACK, ContinueRect, 4)
        # Render "LEADERBOARD" button
        leaderboardSurf = BASICFONT.render('LEADERBOARD', True, YELLOW, BLACK)  # Nội dung nút
        leaderboardRect = leaderboardSurf.get_rect()
        leaderboardRect.center = (WINDOWWIDTH // 2, 6 * WINDOWHEIGHT // 8)  # Vị trí nút
        DISPLAYSURF.blit(leaderboardSurf, leaderboardRect)  # Vẽ text lên màn hình
        pygame.draw.rect(DISPLAYSURF, BLACK, leaderboardRect, 4)
        # Render "EXIT" button
        exitSurf = BASICFONT.render('EXIT', True, YELLOW, BLACK)
        exitRect = exitSurf.get_rect()
        exitRect.center = (WINDOWWIDTH // 2, 7 * WINDOWHEIGHT // 8 )
        DISPLAYSURF.blit(exitSurf, exitRect)
        pygame.draw.rect(DISPLAYSURF, BLACK, ContinueRect, 4)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if newGameRect.collidepoint((mousex, mousey)):
                    return "Newgame"
                elif SettingRect.collidepoint((mousex, mousey)):
                    return "Setting"
                elif ContinueRect.collidepoint((mousex, mousey)):
                    return "Continue"
                elif exitRect.collidepoint((mousex, mousey)):
                    pygame.quit()
                    sys.exit()  # Quit the application
                    # Xử lý click vào nút "LEADERBOARD"
                elif leaderboardRect.collidepoint((mousex, mousey)):
                    showLeaderboard(DISPLAYSURF, BASICFONT, WINDOWWIDTH, WINDOWHEIGHT)
                    return
        pygame.display.update()
        FPSCLOCK.tick(FPS)


"""Bảng Setting"""

# Các nút
buttons = {
    "Board: 12 x 7": {"rect": pygame.Rect(WINDOWWIDTH//2 - 100, WINDOWHEIGHT//2 -100, 200, 50), "text": "Board: 12 x 7", "color": GREEN},
    "Board: 14 x 8": {"rect": pygame.Rect(WINDOWWIDTH//2 - 100, WINDOWHEIGHT//2 -25, 200, 50), "text": "Board: 14 x 8", "color": GRAY},
    "Board: 18 x 10": {"rect": pygame.Rect(WINDOWWIDTH//2 - 100, WINDOWHEIGHT//2 + 50, 200, 50), "text": "Board: 18 x 10", "color": GRAY},
    "sound_toggle": {"rect": pygame.Rect(WINDOWWIDTH//2 - 100, WINDOWHEIGHT//2 + 125, 200, 50), "text": "Sound: ON", "color": GRAY},
    "back": {"rect": pygame.Rect(WINDOWWIDTH//2 - 100, WINDOWHEIGHT//2 + 200, 200, 50), "text": "Back", "color": YELLOW},
}



def draw_background():
    """Vẽ Background"""
    DISPLAYSURF.fill(BLACK)


def draw_settings_box():
    """Vẽ bảng cài đặt."""
    box_rect = pygame.Rect(WINDOWWIDTH//2 - 200, WINDOWHEIGHT//2 - 225, 400, 500)
    pygame.draw.rect(DISPLAYSURF, SKIN_COLOR, box_rect, border_radius=20)
    pygame.draw.rect(DISPLAYSURF, WHITE, box_rect, 3, border_radius=20)


def draw_title():
    """Vẽ tiêu đề bảng settings với viền."""
    title_text = "Settings"
    outline_color = BLACK  # Màu viền
    text_color = YELLOW  # Màu chữ

    # Tạo chữ có viền bằng cách render nhiều lớp xung quanh
    for dx, dy in [(-2, -2), (-2, 2), (2, -2), (2, 2), (0, -2), (0, 2), (-2, 0), (2, 0)]:
        title_outline = title_font.render(title_text, True, outline_color)
        title_rect = title_outline.get_rect(center=(WINDOWWIDTH // 2 + dx,WINDOWHEIGHT//2 - 150 + dy))
        DISPLAYSURF.blit(title_outline, title_rect)

    # Vẽ chữ chính
    title = title_font.render(title_text, True, text_color)
    title_rect = title.get_rect()
    title_rect.center = ((WINDOWWIDTH//2, WINDOWHEIGHT//2 - 150))
    DISPLAYSURF.blit(title, title_rect)

# Các nút tùy chỉnh cài đặt
def draw_buttons():
    """Vẽ các nút."""
    for button in buttons.values():
        pygame.draw.rect(DISPLAYSURF, button["color"], button["rect"], border_radius=15)
        text = font.render(button["text"], True, BLACK)
        text_rect = text.get_rect(center=button["rect"].center)
        DISPLAYSURF.blit(text, text_rect)


# Tùy chỉnh các cài đặt phù hợp       
def handle_click_setting():
    """Tùy chỉnh các cài đặt bằng nhấp chuột"""
    global BOARDWIDTH, BOARDHEIGHT, SOUND_ON, XMARGIN, YMARGIN, BOXSIZE, HEROES_DICT, LEVEL, NUMHEROES_ONBOARD, NUMSAMEHEROES
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONUP:
            mouse_x, mouse_y = event.pos
            for key, button in buttons.items():
                if button["rect"].collidepoint((mouse_x, mouse_y)):
                    if key == "Board: 12 x 7":
                        buttons["Board: 12 x 7"]["color"] = GREEN
                        buttons["Board: 18 x 10"]["color"] = GRAY
                        buttons["Board: 14 x 8"]["color"] = GRAY
                        BOARDHEIGHT = 9
                        BOARDWIDTH = 14
                        BOXSIZE = 55
                        NUMHEROES_ONBOARD = 21
                        NUMSAMEHEROES = 4
                        XMARGIN = (WINDOWWIDTH - (BOXSIZE * BOARDWIDTH)) // 2
                        YMARGIN = (WINDOWHEIGHT - (BOXSIZE * BOARDHEIGHT)) // 2
                        HEROES_DICT = Createheroes()
                    elif key == "Board: 14 x 8":
                        buttons["Board: 12 x 7"]["color"] = GRAY
                        buttons["Board: 18 x 10"]["color"] = GRAY
                        buttons["Board: 14 x 8"]["color"] = GREEN
                        BOARDHEIGHT = 10
                        BOARDWIDTH = 16
                        BOXSIZE = 50
                        NUMHEROES_ONBOARD = 28
                        NUMSAMEHEROES = 4
                        XMARGIN = (WINDOWWIDTH - (BOXSIZE * BOARDWIDTH)) // 2
                        YMARGIN = (WINDOWHEIGHT - (BOXSIZE * BOARDHEIGHT)) // 2
                        HEROES_DICT = Createheroes()
                    elif key == "Board: 18 x 10":
                        buttons["Board: 12 x 7"]["color"] = GRAY
                        buttons["Board: 18 x 10"]["color"] = GREEN
                        buttons["Board: 14 x 8"]["color"] = GRAY
                        BOARDHEIGHT = 12
                        BOARDWIDTH = 20
                        BOXSIZE = 44
                        NUMHEROES_ONBOARD = 45
                        NUMSAMEHEROES = 4
                        XMARGIN = (WINDOWWIDTH - (BOXSIZE * BOARDWIDTH)) // 2
                        YMARGIN = (WINDOWHEIGHT - (BOXSIZE * BOARDHEIGHT)) // 2
                        HEROES_DICT = Createheroes()
                    elif key == "sound_toggle":
                        SOUND_ON = not SOUND_ON  # Đảo trạng thái âm thanh
                        buttons["sound_toggle"]["text"] = f"Sound: {'ON' if SOUND_ON else 'OFF'}"
                        if SOUND_ON:
                            try:
                                pygame.mixer.music.load(listMusicBG[LEVEL - 1])  # Tải nhạc nền
                                pygame.mixer.music.play(-1)  # Phát nhạc nền lặp lại
                            except pygame.error as e:
                                print(f"Error loading music: {e}")
                        else:
                            pygame.mixer.music.stop()  # Dừng nhạc
                    elif key == "back":
                        return "back"
                    
#Hiển thị bảng setting của trò chơi
def showSetting():
    """Hiển thị bảng Settings"""
    while True:
        draw_background()
        draw_settings_box()
        draw_buttons()
        draw_title()
        if handle_click_setting() == "back":
            return
        pygame.display.update()


"""BẢNG XẾP HẠNG"""


def save_leaderboard(leaderboard, filename="User_data/scoreboard.json"):
    """Lưu bảng xếp hạng"""
    with open(filename, "w") as file:
        json.dump(leaderboard, file)


def load_leaderboard(filename="User_data/scoreboard.json"):
    """Load bảng xếp hạng"""
    try:
        with open(filename, "r") as file:
            return json.load(file)  # Trả về danh sách
    except FileNotFoundError:
        return {}
    

# Hiển thị bảng xếp hạng của trò chơi
def showLeaderboard(screen, font, WINDOWWIDTH, WINDOWHEIGHT):
    """Hiển thị bảng xếp hạng"""
    clock = pygame.time.Clock()  # Khởi tạo clock đúng cách
    leaderboard = load_leaderboard()  # Đọc dữ liệu từ file
    sorted_keys = sorted(leaderboard, key = lambda x: leaderboard[x], reverse= True)
    if len(sorted_keys) >= 10:
        sorted_keys =sorted_keys[:10]
    running = True
    while running:
        screen.fill((0, 0, 50))  # Nền xanh đậm
        title = font.render("Leaderboard", True, (255, 255, 0))
        screen.blit(title, (200, 50))

        for i, key in enumerate(sorted_keys):  # Hiển thị top 10
            text = f"{i+1}. {key} - {leaderboard[key]}"
            entry_text = font.render(text, True, (255, 255, 255))
            screen.blit(entry_text, (100, 100 + i * 30))

        # Vẽ nút "Return"
        returnSurf = font.render('RETURN', True, YELLOW, BLACK)
        returnRect = returnSurf.get_rect()
        returnRect.center = (WINDOWWIDTH // 2, 4 * WINDOWHEIGHT // 5)  # Vị trí nút
        screen.blit(returnSurf, returnRect)  # Vẽ nút lên màn hình
        pygame.draw.rect(screen, BLACK, returnRect, 4)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Bấm Enter để quay lại màn hình chính
                    running = False  # Thoát khỏi vòng lặp để quay lại màn hình chính
            elif event.type == pygame.MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if returnRect.collidepoint((mousex, mousey)):  # Kiểm tra click vào nút "RETURN"
                    running = False  # Thoát vòng lặp khi click vào nút "RETURN"

        clock.tick(30)  # Điều chỉnh tốc độ FPS (30 FPS)

    # Sau khi thoát vòng lặp, quay lại màn hình start screen
    return "ReturnToStartScreen"  # Trả về giá trị để quay lại màn hình chính

#

# Make a dict to store scaled images
def Createheroes():
    """Tạo pokemon dựa trên kích cỡ bảng"""
    LISTHEROES = os.listdir("Resources/Pokemon_icons")
    HEROES_DICT = {}

    for i in range(len(LISTHEROES)):
        hero_image = pygame.image.load("Resources/Pokemon_icons/"+ LISTHEROES[i])
        hero_image = pygame.transform.scale(hero_image, (BOXSIZE, BOXSIZE))
        hero_with_border = pygame.Surface((BOXSIZE, BOXSIZE))
        pygame.draw.rect(hero_with_border, BORDERCOLOR, (0, 0, BOXSIZE, BOXSIZE), 3)
        hero_with_border.blit(hero_image, (0, 0))
        HEROES_DICT[i + 1] = hero_with_border
    return HEROES_DICT



"""Màn hình khi dừng trò chơi"""

def showPauseScreen():
    button_font = pygame.font.SysFont('comicsansms', 30)

    # Nút Resume
    resume_button_rect = pygame.Rect(WINDOWWIDTH // 2 - 120, WINDOWHEIGHT // 2 - 70, 240, 50)
    resume_text = button_font.render("RESUME", True, BLACK)

    # Nút Exit
    exit_button_rect = pygame.Rect(WINDOWWIDTH // 2 - 120, WINDOWHEIGHT // 2 + 20, 240, 50)
    exit_text = button_font.render("EXIT", True, BLACK)

    while True:
        DISPLAYSURF.fill(BLACK)  # Màn hình tạm dừng


        # Vẽ nút Resume
        pygame.draw.rect(DISPLAYSURF, WHITE, resume_button_rect)
        DISPLAYSURF.blit(resume_text, resume_button_rect.move(70, 10))

        # Vẽ nút Exit
        pygame.draw.rect(DISPLAYSURF, WHITE, exit_button_rect)
        DISPLAYSURF.blit(exit_text, exit_button_rect.move(90, 10))

        pygame.display.update()

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                if resume_button_rect.collidepoint((mousex, mousey)):
                    return  # Quay lại game
                elif exit_button_rect.collidepoint((mousex, mousey)):
                    return "exit"  # Quay về màn hình chính


"""Lưu lại màn chơi"""

def saveGame(mainBoard):
    USER["Board"] = mainBoard
    USER["Score"] = SCORE
    USER["Level"] = LEVEL
    with open(ACCOUNTS_FILE, "r") as file:
        data = json.load(file)
    data[USER_NAME] = USER
    with open(ACCOUNTS_FILE, "w") as file:
        json.dump(data, file)


def handleHintMatch(mainBoard, boxy1, boxx1, boxy2, boxx2, hint):
    global TIMEBONUS
    mainBoard[boxy1][boxx1] = 0
    mainBoard[boxy2][boxx2] = 0
    TIMEBONUS += 1
    alterBoardWithLevel(mainBoard, boxy1, boxx1, boxy2, boxx2, LEVEL)
    if isGameComplete(mainBoard):
        drawBoard(mainBoard)
        pygame.display.update()
        return
    if not bfs(mainBoard, hint[0][0], hint[0][1], hint[1][0], hint[1][1]):
        hint[:] = getHint(mainBoard)

def handleSelection(mainBoard, firstSelection, secondSelection, clickedBoxes, hint):
    if bfs(mainBoard, firstSelection[1], firstSelection[0], secondSelection[1], secondSelection[0]):
        mainBoard[firstSelection[1]][firstSelection[0]] = 0
        mainBoard[secondSelection[1]][secondSelection[0]] = 0
        drawPath(mainBoard, bfs(mainBoard, firstSelection[1], firstSelection[0], secondSelection[1], secondSelection[0]))
        # Gọi hàm alterBoardWithLevel
        alterBoardWithLevel(mainBoard, firstSelection[1], firstSelection[0], secondSelection[1], secondSelection[0], LEVEL)
        hint = getHint(mainBoard)

def isGameComplete(board):
    """
    Kiểm tra xem bảng đã hoàn thành hay chưa.
    Trả về True nếu tất cả các ô trên bảng đều là 0.
    """
    for row in board:
        if any(cell != 0 for cell in row):  # Nếu còn ô nào khác 0
            return False
    return True  # Tất cả các ô đều là 0
def runGame():
    if USER["Board"] == [[0] * BOARDWIDTH] * BOARDHEIGHT:
        USER["Board"] = getRandomizedBoard()
    mainBoard = USER["Board"]
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR,
                     (XMARGIN - 3, YMARGIN - 3, BOARDWIDTH * BOXSIZE + 6, BOARDHEIGHT * BOXSIZE + 6), 6)
    clickedBoxes = []
    firstSelection = None
    mousex, mousey = 0, 0
    hint = None  # Gợi ý mặc định là None
    hint_visible = False  # Biến cờ để theo dõi trạng thái hiển thị gợi ý
    hint_display_start = 0  # Thời điểm bắt đầu hiển thị gợi ý
    hint_display_time = 1  # Gợi ý sẽ hiển thị trong 3 giây

    global GAMETIME, LIVES, TIMEBONUS, STARTTIME, LEVEL, SCORE, SOUND_ON
    STARTTIME = time.time()
    TIMEBONUS = 0
    randomBG = BG

    # Phát nhạc nền
    pygame.mixer.music.load(listMusicBG[LEVEL - 1])
    if SOUND_ON:
        try:
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Error playing music: {e}")
    else:
        pygame.mixer.music.stop()

    while True:
        DISPLAYSURF.blit(randomBG, (0, 0))
        drawBoard(mainBoard)
        drawTimeBar()
        drawLives()
        display_score(SCORE)

        # Kiểm tra nếu hoàn thành bảng
        if isGameComplete(mainBoard):
            pygame.time.wait(1000)  # Tạm dừng để hiển thị
            return True  # Hoàn thành màn chơi

        # Kiểm tra thời gian hết game
        if time.time() - STARTTIME > GAMETIME + TIMEBONUS:
            LEVEL = LEVELMAX + 1 # Hiển thị màn hình kết thúc
            showGameOverScreen()
            return

        # Ẩn gợi ý sau khoảng thời gian hiển thị
        if hint_visible and time.time() - hint_display_start > hint_display_time:
            hint_visible = False  # Đặt lại cờ, gợi ý sẽ không hiển thị nữa

        if hint_visible:  # Chỉ vẽ gợi ý khi đang ở trạng thái hiển thị
            drawHint(hint)

        mouseClicked = False
        hint = getHint(mainBoard)
        if not hint:
            resetBoard(mainBoard)
        for event in pygame.event.get():
            if event.type == QUIT:
                saveGame(mainBoard)
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                mouseClicked = True
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    result = showPauseScreen()
                    if result == "exit":
                        saveGame(mainBoard)
                        return False  # Chỉ hiển thị gợi ý khi bấm phím N
                hint = getHint(mainBoard)  # Lấy gợi ý
                if event.key == K_n:  # Nếu có gợi ý hợp lệ
                    hint_visible = True  # Bật cờ hiển thị gợi ý
                    hint_display_start = time.time()  # Đặt thời gian bắt đầu hiển thị
                if event.key == K_r:
                    resetBoard(mainBoard)

        # Xử lý lựa chọn trên bảng
        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if firstSelection:
                drawHighlightBox(mainBoard, boxx, boxy, color=YELLOW)
        if boxx is not None and boxy is not None and mainBoard[boxy][boxx] != 0 and mouseClicked:
            clickedBoxes.append((boxx, boxy))
            drawClickedBox(mainBoard, clickedBoxes)
            if firstSelection is None:  # Nếu đây là lựa chọn đầu tiên
                firstSelection = (boxx, boxy)
                clickSound.play()
            else:  # Đã có lựa chọn đầu tiên, kiểm tra cặp ô
                if bfs(mainBoard, firstSelection[1], firstSelection[0], boxy, boxx):  # Nếu hợp lệ
                    handleSelection(mainBoard, firstSelection, (boxx, boxy), clickedBoxes, hint)
                    firstSelection = None
                    pygame.mixer.Sound.play(getPointSound)
                    clickedBoxes.clear()  # Reset danh sách sau khi hoàn thành
                else:  # Không hợp lệ
                    drawHighlightBox(mainBoard, firstSelection[0], firstSelection[1], color=RED)
                    drawHighlightBox(mainBoard, boxx, boxy, color=RED)
                    pygame.mixer.Sound.play(WrongSound)
                    pygame.display.update()
                    pygame.time.wait(300)
                    clickedBoxes.clear()
                    firstSelection = None

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def getRandomizedBoard():
    """"Tạo bảng ngẫu nhiên"""
    list_pokemons = list(range(1, len(Createheroes()) + 1))
    random.shuffle(list_pokemons)
    list_pokemons = list_pokemons[:NUMHEROES_ONBOARD] * NUMSAMEHEROES
    random.shuffle(list_pokemons)
    board = [[0 for _ in range(BOARDWIDTH)] for _ in range(BOARDHEIGHT)]

    # We create a board of images surrounded by 4 arrays of zeroes
    k = 0
    for i in range(1, BOARDHEIGHT - 1):
        for j in range(1, BOARDWIDTH - 1):
            board[i][j] = list_pokemons[k]
            k += 1
            if k == len(list_pokemons):
                k = 0
    return board

def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * BOXSIZE + XMARGIN
    top = boxy * BOXSIZE + YMARGIN
    return left, top

def getBoxAtPixel(x, y):
    if x <= XMARGIN or x >= WINDOWWIDTH - XMARGIN or y <= YMARGIN or y >= WINDOWHEIGHT - YMARGIN:
        return None, None
    return (x - XMARGIN) // BOXSIZE, (y - YMARGIN) // BOXSIZE

def drawBoard(board):
    a = Createheroes()
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            if board[boxy][boxx] != 0:
                left, top = leftTopCoordsOfBox(boxx, boxy)
                boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
                DISPLAYSURF.blit(a[board[boxy][boxx]], boxRect)

def drawHighlightBox(board, boxx, boxy, color=HIGHLIGHTCOLOR):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, color, (left - 2, top - 2, BOXSIZE + 4, BOXSIZE + 4), 2)

def drawClickedBox(board, clickedBoxes):
    a = Createheroes()
    for boxx, boxy in clickedBoxes:
        left, top = leftTopCoordsOfBox(boxx, boxy)
        boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
        image = a[board[boxy][boxx]].copy()

        # Darken the clicked image
        image.fill((60, 60, 60), special_flags=pygame.BLEND_RGB_SUB)
        DISPLAYSURF.blit(image, boxRect)

def bfs(board, boxy1, boxx1, boxy2, boxx2):
    def backtrace(parent, boxy1, boxx1, boxy2, boxx2):
        start = (boxy1, boxx1, 0, 'no_direction')
        end = 0
        for node in parent:
            if node[:2] == (boxy2, boxx2):
                end = node

        path = [end]
        while path[-1] != start:
            path.append(parent[path[-1]])
        path.reverse()

        for i in range(len(path)):
            path[i] = path[i][:2]
        return path

    if board[boxy1][boxx1] != board[boxy2][boxx2]:
        return []

    n = len(board)
    m = len(board[0])

    import collections
    q = collections.deque()
    q.append((boxy1, boxx1, 0, 'no_direction'))
    visited = set()
    visited.add((boxy1, boxx1, 0, 'no_direction'))
    parent = {}

    while len(q) > 0:
        r, c, num_turns, direction = q.popleft()
        if (r, c) != (boxy1, boxx1) and (r, c) == (boxy2, boxx2):
            return backtrace(parent, boxy1, boxx1, boxy2, boxx2)

        dict_directions = {(r + 1, c): 'down', (r - 1, c): 'up', (r, c - 1): 'left',
                           (r, c + 1): 'right'}
        for neiborX, neiborY in dict_directions:
            next_direction = dict_directions[(neiborX, neiborY)]
            if 0 <= neiborX <= n - 1 and 0 <= neiborY <= m - 1 and (
                    board[neiborX][neiborY] == 0 or (neiborX, neiborY) == (boxy2, boxx2)):
                if direction == 'no_direction':
                    q.append((neiborX, neiborY, num_turns, next_direction))
                    visited.add((neiborX, neiborY, num_turns, next_direction))
                    parent[(neiborX, neiborY, num_turns, next_direction)] = (
                    r, c, num_turns, direction)
                elif direction == next_direction and (
                        neiborX, neiborY, num_turns, next_direction) not in visited:
                    q.append((neiborX, neiborY, num_turns, next_direction))
                    visited.add((neiborX, neiborY, num_turns, next_direction))
                    parent[(neiborX, neiborY, num_turns, next_direction)] = (
                    r, c, num_turns, direction)
                elif direction != next_direction and num_turns < 2 and (
                        neiborX, neiborY, num_turns + 1, next_direction) not in visited:
                    q.append((neiborX, neiborY, num_turns + 1, next_direction))
                    visited.add((neiborX, neiborY, num_turns + 1, next_direction))
                    parent[
                        (neiborX, neiborY, num_turns + 1, next_direction)] = (
                    r, c, num_turns, direction)
    return []

def getCenterPos(pos): # pos is coordinate of a box in mainBoard
    left, top = leftTopCoordsOfBox(pos[1], pos[0])
    return tuple([left + BOXSIZE // 2, top + BOXSIZE // 2])

def drawPath(board, path):
    global SCORE
    for i in range(len(path) - 1):
        startPos = getCenterPos(path[i])
        endPos = getCenterPos(path[i + 1])
        pygame.draw.line(DISPLAYSURF, RED, startPos, endPos, 4)
    SCORE += 1
    pygame.display.update()
    pygame.time.wait(300)

def drawTimeBar():
    progress = 1 - ((time.time() - STARTTIME - TIMEBONUS) / GAMETIME)

    pygame.draw.rect(DISPLAYSURF, borderColor, (barPos, barSize), 1)
    innerPos = (barPos[0] + 2, barPos[1] + 2)
    innerSize = ((barSize[0] - 4) * progress, barSize[1] - 4)
    pygame.draw.rect(DISPLAYSURF, barColor, (innerPos, innerSize))

def showGameOverScreen():
    try:
        # Đọc dữ liệu từ tệp, nếu không có thì tạo tệp
        with open("User_data/scoreboard.json", "r") as leaderboard:
            data = json.load(leaderboard)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}  # Nếu không tồn tại, bắt đầu với danh sách trống

    # Xử lý điểm số người chơi
    user_exists = False
    if USER_NAME in data:
        data[USER_NAME] = max(SCORE, data[USER_NAME])
    else:
        data[USER_NAME] = SCORE


    # Ghi lại tệp
    with open("User_data/scoreboard.json", "w") as leaderboard:
        json.dump(data, leaderboard, indent=4)

    # Hiển thị màn hình kết thúc
    playAgainFont = pygame.font.Font('freesansbold.ttf', 50)
    playAgainSurf = playAgainFont.render('EXIT', True, RED)
    playAgainRect = playAgainSurf.get_rect()
    playAgainRect.center = (WINDOWWIDTH // 2, 7 * WINDOWHEIGHT // 8)
    DISPLAYSURF.blit(playAgainSurf, playAgainRect)
    pygame.draw.rect(DISPLAYSURF, RED, playAgainRect, 3)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if playAgainRect.collidepoint((mousex, mousey)):
                    return


def getHint(board):
    boxPokesLocated = collections.defaultdict(list)
    for boxy in range(BOARDHEIGHT):
        for boxx in range(BOARDWIDTH):
            if board[boxy][boxx] != 0:
                boxPokesLocated[board[boxy][boxx]].append((boxy, boxx))
    for boxy in range(BOARDHEIGHT):
        for boxx in range(BOARDWIDTH):
            if board[boxy][boxx] != 0:
                for otherBox in boxPokesLocated[board[boxy][boxx]]:
                    if otherBox != (boxy, boxx) and bfs(board, boxy, boxx, otherBox[0], otherBox[1]):
                        return [(boxy, boxx), otherBox]  # Trả về cặp gợi ý
    return []  # Không có gợi ý nào, trả về danh sách rỗng
def drawHint(hint):
    for boxy, boxx in hint:
        left, top = leftTopCoordsOfBox(boxx, boxy)
        pygame.draw.rect(DISPLAYSURF, GREEN, (left, top, BOXSIZE, BOXSIZE), 4)  # Viền dày hơn để rõ


def resetBoard(board):
    pokesOnBoard = []
    for boxy in range(BOARDHEIGHT):
        for boxx in range(BOARDWIDTH):
            if board[boxy][boxx] != 0:
                pokesOnBoard.append(board[boxy][boxx])
    referencedList = pokesOnBoard[:]
    while referencedList == pokesOnBoard:
        random.shuffle(pokesOnBoard)

    i = 0
    for boxy in range(BOARDHEIGHT):
        for boxx in range(BOARDWIDTH):
            if board[boxy][boxx] != 0:
                board[boxy][boxx] = pokesOnBoard[i]
                i += 1
    return board

def isGameComplete(board):
    for boxy in range(BOARDHEIGHT):
        for boxx in range(BOARDWIDTH):
            if board[boxy][boxx] != 0:
                return False
    return True

def alterBoardWithLevel(board, boxy1, boxx1, boxy2, boxx2, level):

    # Level 2: All the pokemons move up to the top boundary
    if level == 2:
        for boxx in (boxx1, boxx2):
            # rearrange pokes into a current list
            cur_list = [0]
            for i in range(BOARDHEIGHT):
                if board[i][boxx] != 0:
                    cur_list.append(board[i][boxx])
            while len(cur_list) < BOARDHEIGHT:
                cur_list.append(0)

            # add the list into the board
            j = 0
            for num in cur_list:
                board[j][boxx] = num
                j += 1

    # Level 3: All the pokemons move down to the bottom boundary
    if level == 3:
        for boxx in (boxx1, boxx2):
            # rearrange pokes into a current list
            cur_list = []
            for i in range(BOARDHEIGHT):
                if board[i][boxx] != 0:
                    cur_list.append(board[i][boxx])
            cur_list.append(0)
            cur_list = [0] * (BOARDHEIGHT - len(cur_list)) + cur_list

            # add the list into the board
            j = 0
            for num in cur_list:
                board[j][boxx] = num
                j += 1

    # Level 4: All the pokemons move left to the left boundary
    if level == 4:
        for boxy in (boxy1, boxy2):
            # rearrange pokes into a current list
            cur_list = [0]
            for i in range(BOARDWIDTH):
                if board[boxy][i] != 0:
                    cur_list.append(board[boxy][i])
            while len(cur_list) < BOARDWIDTH:
                cur_list.append(0)

            # add the list into the board
            j = 0
            for num in cur_list:
                board[boxy][j] = num
                j += 1

    # Level 5: All the pokemons move right to the right boundary
    if level == 5:
        for boxy in (boxy1, boxy2):
            # rearrange pokes into a current list
            cur_list = []
            for i in range(BOARDWIDTH):
                if board[boxy][i] != 0:
                    cur_list.append(board[boxy][i])
            cur_list.append(0)
            cur_list = [0] * (BOARDWIDTH - len(cur_list)) + cur_list

            # add the list into the board
            j = 0
            for num in cur_list:
                board[boxy][j] = num
                j += 1

    return board

def drawLives():
    aegisRect = pygame.Rect(10, 10, BOXSIZE, BOXSIZE)
    DISPLAYSURF.blit(aegis, aegisRect)
    livesSurf = LIVESFONT.render(str(LIVES), True, WHITE)
    livesRect = livesSurf.get_rect()
    livesRect.topleft = (65, 0)
    DISPLAYSURF.blit(livesSurf, livesRect)







def change_size():
    global XMARGIN, YMARGIN, BOXSIZE
    if BOARDWIDTH == 14:
        BOXSIZE = 55
    elif BOARDWIDTH == 20:
        BOXSIZE = 44
    XMARGIN = (WINDOWWIDTH - (BOXSIZE * BOARDWIDTH)) // 2
    YMARGIN = (WINDOWHEIGHT - (BOXSIZE * BOARDHEIGHT)) // 2


def display_score(score = 0):
    ScoreFont = pygame.font.Font('freesansbold.ttf', 30)
    ScoreSurf = ScoreFont.render(f'Score: {score}', True, YELLOW)
    ScoreRect = ScoreSurf.get_rect()
    ScoreRect.center = (9 * WINDOWWIDTH // 10, WINDOWHEIGHT // 10)
    DISPLAYSURF.blit(ScoreSurf, ScoreRect)
    pygame.draw.rect(DISPLAYSURF, YELLOW, ScoreRect, -1)
    pygame.display.update()


def main():
    """Hàm chính của trò chơi"""
    global FPSCLOCK, DISPLAYSURF, BASICFONT, LIVESFONT, LEVEL, font, title_font, USER, SCORE, BOARDWIDTH, BOARDHEIGHT
    
    # Khởi tạo Pygame
    pygame.init()
    pygame.mixer.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Pikachu')

    # Khởi tạo font
    font = pygame.font.Font(pygame.font.match_font('arial'), 32)
    title_font = pygame.font.Font(pygame.font.match_font('arial'), 50)
    BASICFONT = pygame.font.SysFont('comicsansms', 40)
    LIVESFONT = pygame.font.SysFont('comicsansms', 45)
    
    # Hiển thị màn hình xác thực (đăng nhập/đăng ký)
    while showMainAuthScreen():
        continue

    # Vòng lặp chính của trò chơi
    while True:
        # Hiển thị màn hình bắt đầu và nhận lựa chọn từ người chơi
        choice = showStartScreen()
        
        # Biến cờ để kiểm tra trạng thái chơi
        game_running = True

        # Xử lý các lựa chọn từ màn hình bắt đầu
        if choice == "Newgame" or choice == "Continue":
            if choice == "Newgame":
                LEVEL = 1
                SCORE = 0
                USER["Board"] = getRandomizedBoard()
            else:
                LEVEL = USER["Level"]
                SCORE = USER["Score"]
                BOARDWIDTH = len(USER["Board"][0])
                BOARDHEIGHT = len(USER["Board"])
            
            # Cập nhật kích thước và tài nguyên
            change_size()
            random.shuffle(listMusicBG)
            
            # Vòng lặp cấp độ
            while LEVEL <= LEVELMAX and game_running:
                if not runGame():
                    game_running = False
                    break
                LEVEL += 1
                pygame.time.wait(1000)  # Tạm dừng giữa các cấp độ
            
            # Hiển thị màn hình kết thúc nếu hoàn thành trò chơi
            if game_running:
                showGameOverScreen()
        elif choice == "Setting":
            # Hiển thị cài đặt
            showSetting()


if __name__ == '__main__':
    while True:
        main()  # Chạy lại hàm main khi người chơi nhấn "Play Again"