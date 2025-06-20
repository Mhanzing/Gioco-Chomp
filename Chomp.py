from ezgraphics import GraphicsWindow
import time
import random

# Costanti per la dimensione del campo di gioco
SIZEX = 6
SIZEY = 5

# Funzione per disegnare il menu iniziale
def menu():
    def draw_button(canvas, x, y, width, height, text):
        canvas.setFill("lightblue")
        canvas.drawRect(x, y, width, height)
        canvas.setTextAlignment("center")
        canvas.drawText(x + width / 2, y + height / 2, text)

    win = GraphicsWindow(400, 400)
    canvas = win.canvas()

    # Disegno dei pulsanti
    draw_button(canvas, 100, 50, 200, 50, "Umano vs Umano")
    draw_button(canvas, 100, 150, 200, 50, "Umano vs Computer")
    draw_button(canvas, 100, 250, 200, 50, "Computer vs Computer")

    # Loop per catturare la selezione
    while True:
        click = win.getMouse()
        if click is not None:
            x, y = click
            if 100 <= x <= 300:
                if 50 <= y <= 100:
                    win.close()
                    umano_vs_umano()
                    break
                elif 150 <= y <= 200:
                    win.close()
                    umano_vs_computer()
                    break
                elif 250 <= y <= 300:
                    win.close()
                    computer_vs_computer()
                    break

# Funzione per iniziare il gioco con la grafica della barretta di cioccolato
def start_game(title):
    win = GraphicsWindow(800, 600)
    win.setTitle(title)
    canvas = win.canvas()

    # Disegno del campo di gioco
    chocolate = []
    square_size = 40

    for y in range(SIZEY):
        row = []
        for x in range(SIZEX):
            rect = canvas.drawRect(x * square_size, y * square_size, square_size, square_size)
            row.append(rect)
        chocolate.append(row)

    return win, canvas, chocolate

# Modalità di gioco

def umano_vs_umano():
    win, canvas, chocolate = start_game("Umano vs Umano")
    
    # Logica di gioco per "Umano vs Umano"
    player = 1
    while True:
        click = win.getMouse()
        if click is not None:
            x, y = click
            # Calcolo della posizione nella griglia
            grid_x = x // 40
            grid_y = y // 40

            # Controllo se il click è valido
            if 0 <= grid_x < SIZEX and 0 <= grid_y < SIZEY and chocolate[grid_y][grid_x] is not None:
                # "Mangia" la parte di cioccolato selezionata
                for i in range(grid_y, SIZEY):
                    for j in range(grid_x, SIZEX):
                        if chocolate[i][j] is not None:
                            canvas.setFill("white")
                            canvas.drawRect(j * 40, i * 40, 40, 40)
                            chocolate[i][j] = None

                # Controllo se è stato mangiato il quadrato avvelenato (0, 0)
                if grid_x == 0 and grid_y == 0:
                    canvas.drawText(200, 500, f"Giocatore {player} ha perso!")
                    break

                # Passa il turno all'altro giocatore
                player = 2 if player == 1 else 1
                canvas.drawText(200, 450, f"Turno del giocatore {player}")

    win.wait()

def umano_vs_computer():
    win, canvas, chocolate = start_game("Umano vs Computer")

    # Logica del gioco "Umano vs Computer"
    player = 1
    while True:
        if player == 1:  # Turno dell'umano
            click = win.getMouse()
            if click is not None:
                x, y = click
                grid_x = x // 40
                grid_y = y // 40
                if 0 <= grid_x < SIZEX and 0 <= grid_y < SIZEY and chocolate[grid_y][grid_x] is not None:
                    for i in range(grid_y, SIZEY):
                        for j in range(grid_x, SIZEX):
                            if chocolate[i][j] is not None:
                                canvas.setFill("white")
                                canvas.drawRect(j * 40, i * 40, 40, 40)
                                chocolate[i][j] = None
                    if grid_x == 0 and grid_y == 0:
                        canvas.drawText(200, 500, "Hai perso!")
                        break
                    player = 2
        else:  # Turno del computer
            time.sleep(0.5)
            grid_y = random.randint(0, SIZEY - 1)
            grid_x = random.randint(0, SIZEX - 1)
            if chocolate[grid_y][grid_x] is not None:
                for i in range(grid_y, SIZEY):
                    for j in range(grid_x, SIZEX):
                        if chocolate[i][j] is not None:
                            canvas.setFill("white")
                            canvas.drawRect(j * 40, i * 40, 40, 40)
                            chocolate[i][j] = None
                if grid_x == 0 and grid_y == 0:
                    canvas.drawText(200, 500, "Computer ha perso!")
                    break
                player = 1

    win.wait()

def computer_vs_computer():
    win, canvas, chocolate = start_game("Computer vs Computer")

    # Logica del gioco "Computer vs Computer"
    player = 1
    while True:
        time.sleep(0.5)
        grid_y = random.randint(0, SIZEY - 1)
        grid_x = random.randint(0, SIZEX - 1)
        if chocolate[grid_y][grid_x] is not None:
            for i in range(grid_y, SIZEY):
                for j in range(grid_x, SIZEX):
                    if chocolate[i][j] is not None:
                        canvas.setFill("white")
                        canvas.drawRect(j * 40, i * 40, 40, 40)
                        chocolate[i][j] = None
            if grid_x == 0 and grid_y == 0:
                canvas.drawText(200, 500, f"Giocatore {player} ha perso!")
                break
            player = 2 if player == 1 else 1

    win.wait()

# Avvio del menu
menu()
