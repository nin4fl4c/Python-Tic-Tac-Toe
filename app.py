# Uvozi knjižnico za izdelavo iger Pygame
import pygame
# Uvozi sistemski modul za zapiranje programa
import sys
# Uvozi matematični modul za izračun sinusnih valov zvoka
import math
# Uvozi modul za delo s polji (uporabljeno za zvočni medpomnilnik)
import array

# --- INICIALIZACIJA ---
# Inicializira vse uvožene module Pygame
pygame.init()
# Inicializira mešalnik zvoka z določeno frekvenco in formatom
pygame.mixer.init(frequency=44100, size=-16, channels=1)

# --- NASTAVITVE ZASLONA ---
# Nastavi spremenljivki za širino in višino okna
WIDTH, HEIGHT = 750, 850 
# Ustvari okno aplikacije z določenimi dimenzijami
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
# Nastavi naslovno vrstico okna
pygame.display.set_caption("Tic-Tac-Toe Neon - Izmenjava začetnika")

# --- BARVE ---
# Definira barvo ozadja v RGB formatu (temno modra/vijolična)
BG_COLOR = (15, 0, 35)
# Definira barvo za igralca X (cian modra)
CYAN = (0, 255, 255)         
# Definira barvo za računalnik O (magenta)
MAGENTA = (255, 0, 255)      
# Definira barvo za statusna sporočila (rumena)
YELLOW = (255, 255, 0)       
# Definira belo barvo za besedilo
WHITE = (255, 255, 255)

# --- PISAVE ---
# Funkcija za hitro ustvarjanje objektov pisave določene velikosti
def get_font(size):
    # Vrne sistemsko pisavo Consolas v krepki obliki
    return pygame.font.SysFont("Consolas", size, bold=True)

# Ustvari pisavo za glavni naslov
FONT_TITLE = get_font(55)
# Ustvari pisavo za oznake v okencih
FONT_LABEL = get_font(14)
# Ustvari pisavo za prikaz rezultata
FONT_SCORE = get_font(24)
# Ustvari pisavo za vrstico s statusom igre
FONT_STATUS = get_font(18)
# Ustvari pisavo za besedilo v nogi zaslona
FONT_FOOTER = get_font(12)

# --- ZVOK ---
# Funkcija za generiranje sintetičnega piska z določeno frekvenco
def play_synth_beep(freq, duration=0.08):
    # Uporaba try bloka, da napaka v zvoku ne sesuje celotne igre
    try:
        # Izračuna število vzorcev glede na trajanje in vzorčenje
        n_samples = int(44100 * duration)
        # Ustvari polje 16-bitnih števil na podlagi sinusne funkcije za zvok
        buf = array.array('h', [int(16384 * math.sin(2 * math.pi * freq * i / 44100)) for i in range(n_samples)])
        # Ustvari zvočni objekt iz surovih podatkov v polju
        sound = pygame.mixer.Sound(buf)
        # Nastavi nizko glasnost (10%)
        sound.set_volume(0.1)
        # Predvaja generirani zvok
        sound.play()
    # Če pride do napake pri zvoku, jo tiho prezre
    except: pass

# --- LOGIKA IGRE ---
# Ustvari seznam z 9 polji, ki predstavljajo igralno ploščo
board = [None] * 9
# Slovar za shranjevanje števila zmag in neodločenih izidov
scores = {"player": 0, "ai": 0, "draw": 0}
# Zastavica, ki pove, če se je igra zaključila
game_over = False
# Logična vrednost za določanje, ali je na vrsti človek
player_turn = True  
# Spremenljivka, ki hrani informacijo, kdo bo začel naslednjo rundo
who_starts_next = "AI" 

# Funkcija za preverjanje, ali imamo zmagovalca na plošči
def check_winner(b):
    # Seznam vseh možnih zmagovalnih kombinacij (vrstice, stolpci, diagonale)
    lines = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    # Gre skozi vse linije in preveri, če so vsa tri polja enaka in niso prazna
    for l in lines:
        # Če so tri polja enaka, vrne znak zmagovalca ('X' ali 'O')
        if b[l[0]] and b[l[0]] == b[l[1]] == b[l[2]]: return b[l[0]]
    # Če ni zmagovalca in ni več praznih polj, vrne "DRAW", sicer None
    return "DRAW" if None not in b else None

# Rekurzivni algoritem za iskanje optimalne poteze računalnika
def minimax(b, depth, is_max):
    # Preveri trenutno stanje plošče
    res = check_winner(b)
    # Če zmaga AI, vrne pozitivno vrednost (minus globina za čim hitrejšo zmago)
    if res == 'O': return 10 - depth
    # Če zmaga igralec, vrne negativno vrednost
    if res == 'X': return depth - 10
    # Če je neodločeno, vrne 0
    if res == 'DRAW': return 0
    # Če je na vrsti maksimizator (AI)
    if is_max:
        # Nastavi začetno najslabšo vrednost
        best = -100
        # Preizkusi vse možne poteze na praznih poljih
        for i in range(9):
            if b[i] is None:
                # Postavi simbol, izračunaj vrednost rekurzivno in odstrani simbol
                b[i] = 'O'; v = minimax(b, depth+1, False); b[i] = None
                # Izbere največjo možno vrednost
                best = max(best, v)
        return best
    # Če je na vrsti minimizator (človek)
    else:
        # Nastavi začetno najslabšo vrednost za igralca
        best = 100
        # Preizkusi vse možne poteze igralca
        for i in range(9):
            if b[i] is None:
                # Postavi simbol, izračunaj vrednost rekurzivno in odstrani simbol
                b[i] = 'X'; v = minimax(b, depth+1, True); b[i] = None
                # Izbere najmanjšo možno vrednost
                best = min(best, v)
        return best

# Funkcija za ponastavitev stanja ob začetku nove runde
def reset_game():
    # Uporabi globalne spremenljivke, da jih lahko spreminja znotraj funkcije
    global board, game_over, player_turn, who_starts_next
    # Izprazni igralno ploščo
    board = [None] * 9
    # Ponastavi status konca igre
    game_over = False
    
    # Preklopi začetnika: če je bil nastavljen AI, začne AI in se zamenja status za naslednjič
    if who_starts_next == "AI":
        player_turn = False
        who_starts_next = "PLAYER"
    # Sicer začne igralec in se nastavi AI za naslednji začetek
    else:
        player_turn = True
        who_starts_next = "AI"
    
    # Predvaja zvok ob ponastavitvi
    play_synth_beep(600)

# --- RISANJE ---

# Funkcija za risanje stiliziranega neon okvirja s podatki
def draw_neon_box(rect, color, label_text, value_text, text_color):
    # Nariše pravokotnik z obrobo in zaobljenimi robovi
    pygame.draw.rect(SCREEN, color, rect, 2, border_radius=8)
    # Pripravi sliko besedila za oznako (npr. "IGRALEC")
    lbl = FONT_LABEL.render(label_text, True, WHITE)
    # Postavi oznako na sredino zgornjega dela okvirja
    SCREEN.blit(lbl, (rect.centerx - lbl.get_width() // 2, rect.y + 10))
    # Pripravi sliko besedila za vrednost (rezultat)
    val = FONT_SCORE.render(str(value_text), True, text_color)
    # Postavi rezultat na sredino okvirja
    SCREEN.blit(val, (rect.centerx - val.get_width() // 2, rect.y + 35))

# Funkcija za izris igralne mreže in simbolov
def draw_grid():
    # Definira območje glavne mreže na zaslonu
    grid_rect = pygame.Rect((WIDTH-500)//2, 300, 500, 380)
    # Nariše zunanji okvir mreže
    pygame.draw.rect(SCREEN, MAGENTA, grid_rect, 3, border_radius=12)
    # Nastavi velikost posamezne celice
    cell_w, cell_h = 150, 110
    # Zanko ponovi 9-krat za vsako celico na plošči
    for i in range(9):
        # Izračuna vrstico in stolpec iz indeksa
        r, c = i // 3, i % 3
        # Izračuna točen pravokotnik za posamezno celico
        cell_rect = pygame.Rect(grid_rect.x + 15 + c*160, grid_rect.y + 15 + r*120, cell_w, cell_h)
        # Nariše obrobo posamezne celice
        pygame.draw.rect(SCREEN, CYAN, cell_rect, 2, border_radius=6)
        # Če je v polju X, ga izriše v cian barvi
        if board[i] == 'X':
            s = FONT_TITLE.render("X", True, CYAN)
            SCREEN.blit(s, s.get_rect(center=cell_rect.center))
        # Če je v polju O, ga izriše v magenta barvi
        elif board[i] == 'O':
            s = FONT_TITLE.render("O", True, MAGENTA)
            SCREEN.blit(s, s.get_rect(center=cell_rect.center))
    # Vrne pravokotnik mreže za morebitno nadaljnjo uporabo
    return grid_rect

# Funkcija za izris celotnega uporabniškega vmesnika
def draw_ui():
    # Pofarba celotno ozadje z osnovno barvo
    SCREEN.fill(BG_COLOR)
    # Nariše okrasne linije v ozadju za učinek globine/perspektive
    for i in range(-10, 11):
        pygame.draw.line(SCREEN, (30, 0, 60), (WIDTH//2 + i*20, 500), (WIDTH//2 + i*80, HEIGHT), 1)
        
    # Pripravi in izriše glavni naslov igre
    title = FONT_TITLE.render("TIC-TAC-TOE", True, MAGENTA)
    SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, 30))

    # Definira velikost okenc za rezultate
    box_w, box_h = 160, 75
    # Izriše okenca za rezultate igralca, računalnika in neodločenih iger
    draw_neon_box(pygame.Rect(WIDTH//2 - 255, 120, box_w, box_h), CYAN, "IGRALEC", scores["player"], CYAN)
    draw_neon_box(pygame.Rect(WIDTH//2 - 80, 120, box_w, box_h), MAGENTA, "AI", scores["ai"], MAGENTA)
    draw_neon_box(pygame.Rect(WIDTH//2 + 95, 120, box_w, box_h), YELLOW, "NEODLOČENO", scores["draw"], YELLOW)

    # Definira in nariše pravokotnik za statusno vrstico
    status_rect = pygame.Rect(WIDTH//2 - 250, 225, 500, 40)
    pygame.draw.rect(SCREEN, YELLOW, status_rect, 2, border_radius=5)
    
    # Določi besedilo statusa glede na stanje igre
    if game_over:
        txt = "IGRA KONČANA!"
    else:
        txt = "TVOJA POTEZA (X)" if player_turn else "AI RAZMIŠLJA (O)..."
    
    # Izriše besedilo statusa v sredino statusnega pravokotnika
    st_surf = FONT_STATUS.render(txt, True, YELLOW)
    SCREEN.blit(st_surf, (status_rect.centerx - st_surf.get_width()//2, status_rect.centery - st_surf.get_height()//2))

# Funkcija za izris gumba za ponastavitev
def draw_reset_button():
    # Nastavi položaj in velikost gumba
    btn_rect = pygame.Rect(WIDTH//2 - 100, 710, 200, 50)
    # Nariše zapolnjen pravokotnik gumba
    pygame.draw.rect(SCREEN, MAGENTA, btn_rect, border_radius=10)
    # Pripravi besedilo na gumbu
    btn_txt = FONT_LABEL.render("NOVA IGRA", True, WHITE)
    # Postavi besedilo na sredino gumba
    SCREEN.blit(btn_txt, (btn_rect.centerx - btn_txt.get_width()//2, btn_rect.centery - btn_txt.get_height()//2))
    # Izriše informativno nogo na dnu zaslona
    footer = FONT_FOOTER.render("MINIMAX ALGORITAM | GLOBINA: 9 POTEZ | ALFA-BETA OBREZOVANJE", True, (100, 80, 130))
    SCREEN.blit(footer, (WIDTH//2 - footer.get_width()//2, 790))
    # Vrne pravokotnik gumba za zaznavo klikov
    return btn_rect

# --- MAIN LOOP ---
# Ustvari objekt za nadzor hitrosti osveževanja (FPS)
clock = pygame.time.Clock()
# Glavna zanka programa, ki teče do izhoda
while True:
    # Izriše celoten uporabniški vmesnik
    draw_ui()
    # Izriše mrežo in shrani njen pravokotnik
    grid_rect = draw_grid()
    # Izriše gumb za ponastavitev in shrani njegov pravokotnik
    reset_btn = draw_reset_button()
    
    # Pridobi trenutne koordinate miške
    mx, my = pygame.mouse.get_pos()
    # Pregleda vse dogodke, ki so se zgodili (kliki, tipkovnica...)
    for event in pygame.event.get():
        # Če uporabnik klikne na X, zapre igro
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        # Preveri, če je bila pritisnjena tipka na miški
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Če je uporabnik kliknil na gumb za novo igro
            if reset_btn.collidepoint(mx, my):
                reset_game()
            # Če je na vrsti igralec in igra še ni končana
            elif player_turn and not game_over:
                # Preveri vsako od 9 celic
                for i in range(9):
                    r, c = i // 3, i % 3
                    # Izračuna območje posamezne celice za zaznavo klika
                    cell_r = pygame.Rect((WIDTH-500)//2 + 15 + c*160, 300 + 15 + r*120, 150, 110)
                    # Če je klik v celici in je ta prazna
                    if cell_r.collidepoint(mx, my) and board[i] is None:
                        # Postavi X na ploščo
                        board[i] = 'X'
                        # Predvaja visok pisk
                        play_synth_beep(880)
                        # Preveri, če je ta poteza prinesla zmago ali konec
                        res = check_winner(board)
                        if res:
                            game_over = True
                            # Posodobi rezultat glede na izid
                            if res == 'X': scores["player"] += 1
                            elif res == 'DRAW': scores["draw"] += 1
                        # Če igre ni konec, preda vrsto računalniku
                        else: player_turn = False

    # AI poteza: če je na vrsti računalnik in igra še traja
    if not player_turn and not game_over:
        # Osveži zaslon, da igralec vidi svojo zadnjo potezo pred premislekom AI
        pygame.display.flip()
        # Doda majhen zamik za bolj naraven občutek "razmišljanja"
        pygame.time.delay(600)
        # Inicializira iskanje najboljše vrednosti in poteze
        best_v = -100; move = -1
        # Preveri vse možne poteze na plošči
        for i in range(9):
            if board[i] is None:
                # Za vsako prazno polje izračuna vrednost z Minimaxom
                board[i] = 'O'; v = minimax(board, 0, False); board[i] = None
                # Če je vrednost boljša od trenutno najboljše, si zapomni to potezo
                if v > best_v: best_v = v; move = i
        # Če je AI našel veljavno potezo
        if move != -1:
            # Izvede potezo na plošči
            board[move] = 'O'
            # Predvaja nižji pisk
            play_synth_beep(440)
            # Preveri rezultat po potezi AI
            res = check_winner(board)
            if res:
                game_over = True
                # Posodobi rezultat glede na izid
                if res == 'O': scores["ai"] += 1
                elif res == 'DRAW': scores["draw"] += 1
            # Preda vrsto nazaj igralcu
            player_turn = True

    # Osveži celotno vsebino zaslona
    pygame.display.flip()
    # Omeji število sličic na sekundo na 60
    clock.tick(60) 
