from ezgraphics import GraphicsWindow
import time
import random

# COSTANTI DI GIOCO
# Queste costanti definiscono la dimensione della griglia del cioccolato e altre misure utili
sizex = 6             # Numero di colonne nella griglia
sizey = 5             # Numero di righe nella griglia
square_size = 50      # Dimensione di ciascun quadrato
offset_y = 50         # Spazio in alto del messaggio di turno in partita

def menu():
    # Funzione per disegnare un bottone con il testo centrato
    def draw_button(canvas, x, y, width, height, text):
        canvas.setTextFont("arial", "bold", 10)
        canvas.setFill("lightblue")
        canvas.drawRect(x, y, width, height)
        text_width = len(text) * 6  # Stima della larghezza del testo
        text_x = x + width/2 - text_width/2 - 7
        text_y = y + height/2 - 8 
        canvas.drawText(text_x, text_y, text)

    win_width = 550   # Larghezza della finestra del menu
    win_height = 600  # Altezza della finestra del menu
    win = GraphicsWindow(win_width, win_height)
    canvas = win.canvas()

    # Imposto le dimensioni e le posizioni dei bottoni
    button_width = 200
    button_height = 50
    vertical_spacing = 30
    x_pos = (win_width - button_width) / 2
    y_pos_start = 200
    y_positions = [
        y_pos_start,
        y_pos_start + button_height + vertical_spacing,
        y_pos_start + 2 * (button_height + vertical_spacing),
        y_pos_start + 3 * (button_height + vertical_spacing)
    ]

    def draw_menu_elements():
        canvas.setFill("white")
        canvas.drawRect(0, 0, win_width, win_height)  # Sfondo bianco
        canvas.setTextFont("arial", "bold", 18)
        canvas.setFill("black")
        canvas.drawText((win_width / 2) - 50, 100, "Chomp!")
        draw_button(canvas, x_pos, y_positions[0], button_width, button_height, "Umano vs Umano")
        draw_button(canvas, x_pos, y_positions[1], button_width, button_height, "Umano vs Computer")
        draw_button(canvas, x_pos, y_positions[2], button_width, button_height, "Computer vs Computer")
        draw_button(canvas, x_pos, y_positions[3], button_width, button_height, "Istruzioni")

    draw_menu_elements()

    # Animazione: una barretta di cioccolato che si "mangia" per rivelare il menu
    chocolate_color = "#8B4513"
    canvas.setFill(chocolate_color)
    canvas.drawRect(0, 0, win_width, win_height)

    step = 155       # Incremento di pixel per ogni frame
    delay = 0.4      # Ritardo tra i frame
    for eaten in range(0, win_height + step, step):
        draw_menu_elements()
        canvas.setFill(chocolate_color)
        canvas.drawRect(0, 0, win_width, win_height - eaten)
        time.sleep(delay)

    # Attesa del click dell'utente per scegliere la modalità
    while True:
        click = win.getMouse()
        if click is not None:
            x, y = click
            if x_pos <= x <= x_pos + button_width:
                if y_positions[0] <= y <= y_positions[0] + button_height:
                    win.close()
                    umano_vs_umano()
                    break
                elif y_positions[1] <= y <= y_positions[1] + button_height:
                    win.close()
                    umano_vs_computer()
                    break
                elif y_positions[2] <= y <= y_positions[2] + button_height:
                    win.close()
                    computer_vs_computer()
                    break
                elif y_positions[3] <= y <= y_positions[3] + button_height:
                    show_instructions(win, canvas)
                    break

def show_instructions(win, canvas):
    canvas.setFill("white")
    canvas.drawRect(50, 50, 450, 400)
    canvas.setFill("black")
    instructions_text = [
        "Benvenuto nel gioco del Chomp!",
        "Ci sono tre modalità di gioco:",
        "",
        "1. Umano vs Umano: due giocatori si alternano a mangiare il",
        "   cioccolato.",
        "2. Umano vs Computer: il giocatore affronta il computer.",
        "3. Computer vs Computer: due computer giocano tra di loro.",
        "",
        "Il gioco termina quando uno dei giocatori mangia il cioccolato",
        "avvelenato.",
        "Chi mangia il cioccolato avvelenato perde!",
        "",
        "Clicca per continuare..."
    ]
    y_position = 70
    for line in instructions_text:
        canvas.drawText(60, y_position, line)
        y_position += 20
    win.getMouse()
    win.close()
    menu()

def start_game(title):
    # Questa funzione crea la finestra di gioco e disegna la griglia del cioccolato
    win = GraphicsWindow(800, 600)
    win.setTitle(title)
    canvas = win.canvas()
    chocolate = []
    chocolate_color = "#8B4513"   # Colore normale del cioccolato
    poisoned_color = "#3b1904"    # Colore del cioccolato avvelenato

    for y in range(sizey):
        row = []
        for x in range(sizex):
            rect_x = x * square_size
            rect_y = y * square_size + offset_y
            # Scelgo i colori: se il quadrato è quello avvelenato, uso colori differenti
            if x == 0 and y == 0:
                outer_color = poisoned_color
                inner_color = "#5E2A12"  # Colore interno per il pezzo avvelenato
            else:
                outer_color = chocolate_color
                inner_color = "#A0522D"  # Colore interno per i pezzi normali

            # Disegno il quadrato esterno
            canvas.setFill(outer_color)
            canvas.drawRect(rect_x, rect_y, square_size, square_size)
            # Disegno un quadrato più piccolo all'interno per rendere il cioccolato più bello
            margin = 5
            inner_size = square_size - 2 * margin
            canvas.setFill(inner_color)
            canvas.drawRect(rect_x + margin, rect_y + margin, inner_size, inner_size)
            
            row.append((rect_x, rect_y, square_size))
        chocolate.append(row)
    return win, canvas, chocolate

def update_turn_message(canvas, player, mode):
    canvas.setTextFont("arial", "bold", 14)
    canvas.setFill("white")
    canvas.drawRect(0, 0, 800, offset_y)  # Cancello l'area dei messaggi
    canvas.setFill("black")
    if mode == "umano_vs_umano":
        message = "Turno Giocatore 1" if player == 1 else "Turno Giocatore 2"
    elif mode == "umano_vs_computer":
        message = "Turno Giocatore" if player == 1 else "Turno Computer"
    elif mode == "computer_vs_computer":
        message = "Turno Computer 1" if player == 1 else "Turno Computer 2"
    text_width = len(message) * 10
    text_x = (800 - text_width) // 2
    text_y = offset_y // 2 
    canvas.drawText(text_x, text_y, message)

def eat_chocolate(quadrat, chocolate, grid_x, grid_y):
    sizex_local, sizey_local = len(chocolate[0]), len(chocolate)
    for i in range(grid_y, sizey_local):
        for j in range(grid_x, sizex_local):
            if chocolate[i][j] is not None:
                rect_x, rect_y, _ = chocolate[i][j]
                chocolate[i][j] = None
                quadrat.setFill("white")
                quadrat.setOutline("white")
                quadrat.drawRect(rect_x, rect_y, square_size, square_size)
                quadrat.setOutline("black")
                num_breadcrumbs = random.randint(1, 4)
                for _ in range(num_breadcrumbs):
                    breadcrumb_x = rect_x + random.randint(5, square_size - 5)
                    breadcrumb_y = rect_y + random.randint(5, square_size - 5)
                    quadrat.setFill("#8B4513")
                    quadrat.drawOval(breadcrumb_x - 3, breadcrumb_y - 3, 4, 4)

def computer_move(canvas, chocolate):
    # Il computer sceglie un quadrato disponibile evitando (0,0) se possibile.
    sizex_local, sizey_local = len(chocolate[0]), len(chocolate)
    available_moves = []
    for y in range(sizey_local):
        for x in range(sizex_local):
            if chocolate[y][x] is not None:
                available_moves.append((x, y))
    if len(available_moves) > 1 and (0, 0) in available_moves:
        available_moves.remove((0, 0))
    grid_x, grid_y = random.choice(available_moves)
    eat_chocolate(canvas, chocolate, grid_x, grid_y)
    return grid_x, grid_y

def draw_end_game_screen(canvas, win, modalita, victory_msg):
    canvas.setFill("white")
    canvas.drawRect(0, 0, 800, 600)
    
    canvas.setFill("black")
    canvas.setTextFont("arial", "bold", 22)
    text_width = len(victory_msg) * 14
    text_x = (450 - text_width) // 2 + 10
    text_y = 300
    canvas.drawText(text_x, text_y, victory_msg)
    canvas.setTextFont("arial", "normal", 12)
    
    button_width = 200
    button_height = 50
    vertical_spacing = 40
    x_pos = 500
    y_pos_start = 200
    
    def draw_end_button(x, y, width, height, text):
        canvas.setFill("lightblue")
        canvas.drawRect(x, y, width, height)
        text_width = len(text) * 6
        text_x = x + (width - text_width) // 2 - 8
        text_y = y + (height - 12) // 2
        canvas.drawText(text_x, text_y, text)
    
    draw_end_button(x_pos, y_pos_start, button_width, button_height, "Torna al menù")
    draw_end_button(x_pos, y_pos_start + button_height + vertical_spacing, button_width, button_height, "Rigioca")
    draw_end_button(x_pos, y_pos_start + 2 * (button_height + vertical_spacing), button_width, button_height, "Chiudi il gioco")
    
    while True:
        click = win.getMouse()
        if click is not None:
            x, y = click
            if x_pos <= x <= x_pos + button_width:
                if y_pos_start <= y <= y_pos_start + button_height:
                    win.close()
                    menu()
                    break
                elif y_pos_start + button_height + vertical_spacing <= y <= y_pos_start + 2 * button_height + vertical_spacing:
                    win.close()
                    if modalita == "umano_vs_umano":
                        umano_vs_umano()
                    elif modalita == "umano_vs_computer":
                        umano_vs_computer()
                    elif modalita == "computer_vs_computer":
                        computer_vs_computer()
                    break
                elif y_pos_start + 2 * (button_height + vertical_spacing) <= y <= y_pos_start + 3 * button_height + 2 * vertical_spacing:
                    win.close()
                    break

def show_start(player, mode):
    win = GraphicsWindow(400, 400)
    canvas = win.canvas()
    
    if player == 1:
        canvas.setFill("cyan")
    else:
        canvas.setFill("lime")
    canvas.drawRect(0, 0, 400, 400)
    
    button_width = 180
    button_height = 50
    x_button = (400 - button_width) // 2
    y_button = 200
    button_color = "lightblue" if player == 1 else "green"
    
    canvas.setFill(button_color)
    canvas.drawRect(x_button, y_button, button_width, button_height)
    canvas.setTextFont("arial", "bold", 12)
    canvas.setFill("white")
    text_x = x_button + (button_width - len("Inizia la partita") * 6) / 2
    text_y = y_button + (button_height - 12) / 2
    canvas.drawText(text_x, text_y, "Inizia la partita")
    canvas.setTextFont("arial", "bold", 24)
    canvas.setFill("black")
    
    if mode == "umano_vs_umano":
        message = "Inizia Giocatore 1" if player == 1 else "Inizia Giocatore 2"
    elif mode == "umano_vs_computer":
        message = "Inizia Giocatore" if player == 1 else "Inizia Computer"
    elif mode == "computer_vs_computer":
        message = "Inizia Computer 1" if player == 1 else "Inizia Computer 2"
    canvas.drawText(70, 140, message)
    
    while True:
        click = win.getMouse()
        if click is not None:
            x, y = click
            if (x_button <= x <= x_button + button_width and
                y_button <= y <= y_button + button_height):
                win.close()
                break

def umano_vs_umano():
    player = random.choice([1, 2])
    mode = "umano_vs_umano"
    show_start(player, mode)
    win, canvas, chocolate = start_game("Umano vs Umano")
    update_turn_message(canvas, player, mode)

    while True:
        click = win.getMouse()
        if click is not None:
            x, y = click
            grid_x = x // square_size
            grid_y = (y - offset_y) // square_size
            if 0 <= grid_x < sizex and 0 <= grid_y < sizey and chocolate[grid_y][grid_x] is not None:
                eat_chocolate(canvas, chocolate, grid_x, grid_y)
                if grid_x == 0 and grid_y == 0:
                    victory_msg = f"Giocatore {player} ha perso!"
                    draw_end_game_screen(canvas, win, mode, victory_msg)
                    break
                player = 2 if player == 1 else 1
                update_turn_message(canvas, player, mode)
    win.wait()

def umano_vs_computer():
    player = random.choice([1, 2])
    mode = "umano_vs_computer"
    show_start(player, mode)
    win, canvas, chocolate = start_game("Umano vs Computer")
    update_turn_message(canvas, player, mode)
    
    while True:
        if player == 1:
            click = win.getMouse()
            if click is not None:
                x, y = click
                grid_x = x // square_size
                grid_y = (y - offset_y) // square_size
                if 0 <= grid_x < sizex and 0 <= grid_y < sizey and chocolate[grid_y][grid_x] is not None:
                    eat_chocolate(canvas, chocolate, grid_x, grid_y)
                    player = 2
                    if grid_x == 0 and grid_y == 0:
                        victory_msg = "Il computer ha vinto!"
                        draw_end_game_screen(canvas, win, mode, victory_msg)
                        break
            update_turn_message(canvas, player, mode)
        else:
            time.sleep(0.8)
            grid_x, grid_y = computer_move(canvas, chocolate)
            if grid_x == 0 and grid_y == 0:
                victory_msg = "Hai vinto!"
                draw_end_game_screen(canvas, win, mode, victory_msg)
                break
            player = 1
            update_turn_message(canvas, player, mode)
    win.wait()

def computer_vs_computer():
    player = random.choice([1, 2])
    mode = "computer_vs_computer"
    show_start(player, mode)
    win, canvas, chocolate = start_game("Computer vs Computer")
    update_turn_message(canvas, player, mode)
    
    while True:
        time.sleep(1)
        grid_x, grid_y = computer_move(canvas, chocolate)
        if grid_x == 0 and grid_y == 0:
            victory_msg = f"Giocatore {player} (Computer) ha perso!"
            draw_end_game_screen(canvas, win, mode, victory_msg)
            break
        player = 2 if player == 1 else 1
        update_turn_message(canvas, player, mode)
    win.wait()

if __name__ == "__main__":
    menu()
