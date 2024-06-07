import tkinter as tk
from PIL import Image, ImageTk

class Pokemon:
    def __init__(self, nombre, tipos, imagen):
        self.nombre = nombre
        self.tipos = tipos
        self.imagen = imagen

# Lista de Pokémon con enlaces a las imágenes
pokemones = [
    Pokemon('Charizard', ['fuego', 'volador'], 'images/charizard.png'),
    Pokemon('Blastoise', ['agua'], 'images/blastoise.png'),
    Pokemon('Primarina', ['agua', 'hada'], 'images/primarina.png'),
    # Otros Pokémon con sus respectivas rutas de imágenes
]

class SeleccionPokemonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Selección de Pokémon")

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.label = tk.Label(self.frame, text="Selecciona un Pokémon:")
        self.label.pack()

        self.pokemon_buttons = []
        for pokemon in pokemones:
            image = Image.open(pokemon.imagen)
            image = image.resize((100, 100), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)

            button = tk.Button(self.frame, text=pokemon.nombre, image=photo, compound=tk.TOP, command=lambda p=pokemon: self.mostrar_pokemon(p))
            button.photo = photo
            button.pack(side=tk.LEFT, padx=10, pady=10)
            self.pokemon_buttons.append(button)

        self.info_label = tk.Label(self.root, text="")
        self.info_label.pack()

    def mostrar_pokemon(self, pokemon):
        self.info_label.config(text=f"Has seleccionado a {pokemon.nombre} de tipo {', '.join(pokemon.tipos)}.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SeleccionPokemonApp(root)
    root.mainloop()
