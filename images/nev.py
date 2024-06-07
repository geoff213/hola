import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random   


class Movimiento:
    def __init__(self, nombre, tipo, poder):
        self.nombre = nombre
        self.tipo = tipo
        self.poder = poder

class Pokemon:
    def __init__(self, nombre, tipos, movimientos, Evs, imagen_path, nivel=5, exp=0):
        self.nombre = nombre
        self.tipos = tipos if isinstance(tipos, list) else [tipos]
        self.movimientos = movimientos
        self.ataque = Evs['ataque']
        self.defensa = Evs['defensa']
        self.nivel = nivel
        self.exp = exp
        self.vida = 100 + nivel * 2
        self.max_vida = self.vida
        self.estado = None
        self.imagen_path = imagen_path

    def impresa(self):
        return f"{self.nombre} ({'/'.join(self.tipos)}) - Nivel: {self.nivel}, Ataque: {self.ataque}, Defensa: {self.defensa}, Vida: {self.vida}/{self.max_vida}"

    def calcular_daño(self, movimiento, oponente):
        efectividad = 1
        for tipo in oponente.tipos:
            if (movimiento.tipo == 'agua' and tipo == 'fuego') or \
               (movimiento.tipo == 'fuego' and tipo == 'planta') or \
               (movimiento.tipo == 'planta' and tipo == 'agua'):
                efectividad *= 2
            elif (movimiento.tipo == 'agua' and tipo == 'planta') or \
                 (movimiento.tipo == 'fuego' and tipo == 'agua') or \
                 (movimiento.tipo == 'planta' and tipo == 'fuego'):
                efectividad *= 0.5

        daño = (movimiento.poder + self.ataque) * efectividad - oponente.defensa // 10
        return max(1, int(daño))

    def ganar_experiencia(self, cantidad):
        self.exp += cantidad
        if self.exp >= self.nivel * 10:
            self.subir_nivel()

    def subir_nivel(self):
        self.nivel += 1
        self.ataque += random.randint(1, 3)
        self.defensa += random.randint(1, 3)
        self.max_vida += 10
        self.vida = self.max_vida
        self.exp = 0
        messagebox.showinfo("Subida de Nivel", f"¡{self.nombre} ha subido al nivel {self.nivel}!")

    def aplicar_estado(self, estado):
        self.estado = estado

class BatallaPokemon:
    def __init__(self, root, jugador_pokemon, oponente_pokemon):
        self.jugador_pokemon = jugador_pokemon
        self.oponente_pokemon = oponente_pokemon

        self.root = root
        self.root.title("Batalla Pokémon")

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.canvas = tk.Canvas(self.frame, width=600, height=400)
        self.canvas.pack()

        self.imagen_jugador = Image.open(self.jugador_pokemon.imagen_path)
        self.imagen_jugador = self.imagen_jugador.resize((200, 200), Image.LANCZOS)
        self.imagen_jugador = ImageTk.PhotoImage(self.imagen_jugador)

        self.imagen_oponente = Image.open(self.oponente_pokemon.imagen_path)
        self.imagen_oponente = self.imagen_oponente.resize((200, 200), Image.LANCZOS)
        self.imagen_oponente = ImageTk.PhotoImage(self.imagen_oponente)

        self.canvas.create_image(100, 200, image=self.imagen_jugador, anchor=tk.CENTER)
        self.canvas.create_image(500, 200, image=self.imagen_oponente, anchor=tk.CENTER)

        self.info_jugador = tk.Label(self.frame, text=self.jugador_pokemon.impresa())
        self.info_jugador.pack()

        self.barra_vida_jugador = tk.Canvas(self.frame, width=200, height=20, bg='red')
        self.barra_vida_jugador.pack()

        self.info_oponente = tk.Label(self.frame, text=self.oponente_pokemon.impresa())
        self.info_oponente.pack()

        self.barra_vida_oponente = tk.Canvas(self.frame, width=200, height=20, bg='red')
        self.barra_vida_oponente.pack()

        self.movimiento_1 = tk.Button(self.frame, text=self.jugador_pokemon.movimientos[0].nombre, command=lambda: self.atacar(0))
        self.movimiento_1.pack()

        self.movimiento_2 = tk.Button(self.frame, text=self.jugador_pokemon.movimientos[1].nombre, command=lambda: self.atacar(1))
        self.movimiento_2.pack()

        self.movimiento_3 = tk.Button(self.frame, text=self.jugador_pokemon.movimientos[2].nombre, command=lambda: self.atacar(2))
        self.movimiento_3.pack()

        self.movimiento_4 = tk.Button(self.frame, text=self.jugador_pokemon.movimientos[3].nombre, command=lambda: self.atacar(3))
        self.movimiento_4.pack()

        self.actualizar_barras_vida()

    def actualizar_barras_vida(self):
        self.barra_vida_jugador.coords(self.barra_vida_jugador.create_rectangle(0, 0, self.jugador_pokemon.vida / self.jugador_pokemon.max_vida * 200, 20, fill="green"))
        self.barra_vida_oponente.coords(self.barra_vida_oponente.create_rectangle(0, 0, self.oponente_pokemon.vida / self.oponente_pokemon.max_vida * 200, 20, fill="green"))

    def actualizar_pantalla(self):
        self.info_jugador.config(text=self.jugador_pokemon.impresa())
        self.info_oponente.config(text=self.oponente_pokemon.impresa())
        self.actualizar_barras_vida()

    def atacar(self, movimiento_idx):
        movimiento = self.jugador_pokemon.movimientos[movimiento_idx]
        damage = self.jugador_pokemon.calcular_daño(movimiento, self.oponente_pokemon)
        self.oponente_pokemon.vida -= damage
        if self.oponente_pokemon.vida < 0:
            self.oponente_pokemon.vida = 0

        self.actualizar_pantalla()

        if self.oponente_pokemon.vida <= 0:
            self.jugador_pokemon.ganar_experiencia(10)
            messagebox.showinfo("Batalla Pokémon", f"{self.oponente_pokemon.nombre} se debilitó. ¡Ganaste!")
            self.root.after(1000, self.finalizar_batalla)
        else:
            self.root.after(1000, self.turno_oponente)

    def turno_oponente(self):
        movimiento = random.choice(self.oponente_pokemon.movimientos)
        damage = self.oponente_pokemon.calcular_daño(movimiento, self.jugador_pokemon)
        self.jugador_pokemon.vida -= damage
        if self.jugador_pokemon.vida < 0:
            self.jugador_pokemon.vida = 0

        self.actualizar_pantalla() 

        if self.jugador_pokemon.vida <= 0:
            messagebox.showinfo("Batalla Pokémon", f"{self.jugador_pokemon.nombre} se debilitó. ¡Perdiste!")
            self.root.after(1000, self.finalizar_batalla)

    def finalizar_batalla(self):
        continuar = messagebox.askyesno("Batalla Pokémon", "¿Quieres tener otra batalla?")
        if continuar:
            self.root.destroy()
            iniciar_batalla()
        else:
            self.root.destroy()

def seleccionar_pokemon():
    movimientos = [
        Movimiento('Lanzallamas', 'fuego', 90),
        Movimiento('Hidrobomba', 'agua', 110),
        Movimiento('Latigazo', 'planta', 70),
        Movimiento('Impactrueno', 'eléctrico', 60),
        Movimiento('Bola Sombra', 'fantasma', 80),
        Movimiento('Lengüetazo', 'fantasma', 40),
        Movimiento('Esfera Aural', 'lucha', 80),
        Movimiento('Golpe Roca', 'lucha', 50),
        Movimiento('Shuriken de Agua', 'agua', 75),
        Movimiento('Hidro Pulso', 'agua', 60),
        Movimiento('Lariat Oscuro', 'fuego', 90),
        Movimiento('Colmillo Ígneo', 'fuego', 85),
        Movimiento('Canto', 'agua', 70),
        Movimiento('Voz Cautivadora', 'agua', 60),
        Movimiento('Latigazo', 'planta', 70),
        Movimiento('Tambor', 'planta', 85),
    ]

    pokemones = [
        Pokemon('Charizard', ['fuego', 'volador'], movimientos[:4], {'ataque': 84, 'defensa': 78},'images/charizard.png'),
        Pokemon('Blastoise', 'agua', movimientos[:4], {'ataque': 83, 'defensa': 100}, 'images/blastoise.png'),
        Pokemon('Venusaur', ['planta', 'veneno'], movimientos[:4], {'ataque': 82, 'defensa': 83}, 'images/venusaur.png'),
        Pokemon('Pikachu', 'eléctrico', movimientos[:4], {'ataque': 55, 'defensa': 40}, 'images/pikachu.png'),
        Pokemon('Gengar', 'fantasma', movimientos[4:6], {'ataque': 65, 'defensa': 60}, 'images/gengar.png'),
        Pokemon('Lucario', ['lucha', 'acero'], movimientos[6:8], {'ataque': 110, 'defensa': 70}, 'images/lucario.png'),
        Pokemon('Greninja', ['agua', 'siniestro'], movimientos[8:10], {'ataque': 95, 'defensa': 67}, 'images/greninja.png'),
        Pokemon('Incineroar', ['fuego', 'siniestro'], movimientos[10:12], {'ataque': 115, 'defensa': 90}, 'images/incineroar.png'),
        Pokemon('Primarina', ['agua', 'hada'], movimientos[12:14], {'ataque': 74, 'defensa': 74}, 'images/primarina.png'),
        Pokemon('Rillaboom', ['planta'], movimientos[14:16], {'ataque': 125, 'defensa': 90}, 'images/rillaboom.png'),
    ]

    return random.choice(pokemones)

def iniciar_batalla():
    root = tk.Tk()

    jugador_pokemon = seleccionar_pokemon()
    oponente_pokemon = seleccionar_pokemon()

    while oponente_pokemon == jugador_pokemon:
        oponente_pokemon = seleccionar_pokemon()

    app = BatallaPokemon(root, jugador_pokemon, oponente_pokemon)
    root.mainloop()

if __name__ == "__main__":
    iniciar_batalla()