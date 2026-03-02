import pygame
import sys
import math
import array

# --- INICIALIZACIJA ---
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=1)

# --- NASTAVITVE ZASLONA ---
WIDTH, HEIGHT = 750, 850 
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe Neon - Izmenjava začetnika")

# --- BARVE ---
BG_COLOR = (15, 0, 35)
CYAN = (0, 255, 255)         # Igralec X
MAGENTA = (255, 0, 255)      # AI O
YELLOW = (255, 255, 0)       # Status
WHITE = (255, 255, 255)

# --- PISAVE ---
def get_font(size):
    return pygame.font.SysFont("Consolas", size, bold=True)

FONT_TITLE = get_font(55)
FONT_LABEL = get_font(14)
FONT_SCORE = get_font(24)
FONT_STATUS = get_font(18)
FONT_FOOTER = get_font(12)

# --- ZVOK ---
def play_synth_beep(freq, duration=0.08):
    try:
        n_samples = int(44100 * duration)
        buf = array.array('h', [int(16384 * math.sin(2 * math.pi * freq * i / 44100)) for i in range(n_samples)])
        sound = pygame.mixer.Sound(buf)
        sound.set_volume(0.1)
        sound.play()
    except: pass

# --- LOGIKA IGRE ---
board = [None] * 9
scores = {"player": 0, "ai": 0, "draw": 0}
game_over = False
player_turn = True  # Kdo je trenutno na potezi
who_starts_next = "AI" # Logika za menjavo začetnika v naslednji igri

def check_winner(b):
    lines = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    for l in lines:
        if b[l[0]] and b[l[0]] == b[l[1]] == b[l[2]]: return b[l[0]]
    return "DRAW" if None not in b else None

def minimax(b, depth, is_max):
    res = check_winner(b)
    if res == 'O': return 10 - depth
    if res == 'X': return depth - 10
    if res == 'DRAW': return 0
    if is_max:
        best = -100
        for i in range(9):
            if b[i] is None:
                b[i] = 'O'; v = minimax(b, depth+1, False); b[i] = None
                best = max(best, v)
        return best
    else:
        best = 100
        for i in range(9):
            if b[i] is None:
                b[i] = 'X'; v = minimax(b, depth+1, True); b[i] = None
                best = min(best, v)
        return best

def reset_game():
    global board, game_over, player_turn, who_starts_next
    board = [None] * 9
    game_over = False
    
    # Če je who_starts_next "AI", bo player_turn False (začne računalnik)
    if who_starts_next == "AI":
        player_turn = False
        who_starts_next = "PLAYER"
    else:
        player_turn = True
        who_starts_next = "AI"
    
    play_synth_beep(600)

# --- RISANJE ---

def draw_neon_box(rect, color, label_text, value_text, text_color):
    pygame.draw.rect(SCREEN, color, rect, 2, border_radius=8)
    lbl = FONT_LABEL.render(label_text, True, WHITE)
    SCREEN.blit(lbl, (rect.centerx - lbl.get_width() // 2, rect.y + 10))
    val = FONT_SCORE.render(str(value_text), True, text_color)
    SCREEN.blit(val, (rect.centerx - val.get_width() // 2, rect.y + 35))

def draw_grid():
    grid_rect = pygame.Rect((WIDTH-500)//2, 300, 500, 380)
    pygame.draw.rect(SCREEN, MAGENTA, grid_rect, 3, border_radius=12)
    cell_w, cell_h = 150, 110
    for i in range(9):
        r, c = i // 3, i % 3
        cell_rect = pygame.Rect(grid_rect.x + 15 + c*160, grid_rect.y + 15 + r*120, cell_w, cell_h)
        pygame.draw.rect(SCREEN, CYAN, cell_rect, 2, border_radius=6)
        if board[i] == 'X':
            s = FONT_TITLE.render("X", True, CYAN)
            SCREEN.blit(s, s.get_rect(center=cell_rect.center))
        elif board[i] == 'O':
            s = FONT_TITLE.render("O", True, MAGENTA)
            SCREEN.blit(s, s.get_rect(center=cell_rect.center))
    return grid_rect

def draw_ui():
    SCREEN.fill(BG_COLOR)
    # Ozadje mreža
    for i in range(-10, 11):
        pygame.draw.line(SCREEN, (30, 0, 60), (WIDTH//2 + i*20, 500), (WIDTH//2 + i*80, HEIGHT), 1)
        
    title = FONT_TITLE.render("TIC-TAC-TOE", True, MAGENTA)
    SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, 30))

    box_w, box_h = 160, 75
    draw_neon_box(pygame.Rect(WIDTH//2 - 255, 120, box_w, box_h), CYAN, "IGRALEC", scores["player"], CYAN)
    draw_neon_box(pygame.Rect(WIDTH//2 - 80, 120, box_w, box_h), MAGENTA, "AI", scores["ai"], MAGENTA)
    draw_neon_box(pygame.Rect(WIDTH//2 + 95, 120, box_w, box_h), YELLOW, "NEODLOČENO", scores["draw"], YELLOW)

    status_rect = pygame.Rect(WIDTH//2 - 250, 225, 500, 40)
    pygame.draw.rect(SCREEN, YELLOW, status_rect, 2, border_radius=5)
    
    if game_over:
        txt = "IGRA KONČANA!"
    else:
        txt = "TVOJA POTEZA (X)" if player_turn else "AI RAZMIŠLJA (O)..."
    
    st_surf = FONT_STATUS.render(txt, True, YELLOW)
    SCREEN.blit(st_surf, (status_rect.centerx - st_surf.get_width()//2, status_rect.centery - st_surf.get_height()//2))

def draw_reset_button():
    btn_rect = pygame.Rect(WIDTH//2 - 100, 710, 200, 50)
    pygame.draw.rect(SCREEN, MAGENTA, btn_rect, border_radius=10)
    btn_txt = FONT_LABEL.render("NOVA IGRA", True, WHITE)
    SCREEN.blit(btn_txt, (btn_rect.centerx - btn_txt.get_width()//2, btn_rect.centery - btn_txt.get_height()//2))
    footer = FONT_FOOTER.render("MINIMAX ALGORITAM | GLOBINA: 9 POTEZ | ALFA-BETA OBREZOVANJE", True, (100, 80, 130))
    SCREEN.blit(footer, (WIDTH//2 - footer.get_width()//2, 790))
    return btn_rect

# --- MAIN LOOP ---
clock = pygame.time.Clock()
while True:
    draw_ui()
    grid_rect = draw_grid()
    reset_btn = draw_reset_button()
    
    mx, my = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if reset_btn.collidepoint(mx, my):
                reset_game()
            elif player_turn and not game_over:
                for i in range(9):
                    r, c = i // 3, i % 3
                    cell_r = pygame.Rect((WIDTH-500)//2 + 15 + c*160, 300 + 15 + r*120, 150, 110)
                    if cell_r.collidepoint(mx, my) and board[i] is None:
                        board[i] = 'X'
                        play_synth_beep(880)
                        res = check_winner(board)
                        if res:
                            game_over = True
                            if res == 'X': scores["player"] += 1
                            elif res == 'DRAW': scores["draw"] += 1
                        else: player_turn = False

    # AI poteza, če ni na vrsti igralec
    if not player_turn and not game_over:
        pygame.display.flip()
        pygame.time.delay(600)
        best_v = -100; move = -1
        for i in range(9):
            if board[i] is None:
                board[i] = 'O'; v = minimax(board, 0, False); board[i] = None
                if v > best_v: best_v = v; move = i
        if move != -1:
            board[move] = 'O'
            play_synth_beep(440)
            res = check_winner(board)
            if res:
                game_over = True
                if res == 'O': scores["ai"] += 1
                elif res == 'DRAW': scores["draw"] += 1
            player_turn = True

    pygame.display.flip()
    clock.tick(60)
    