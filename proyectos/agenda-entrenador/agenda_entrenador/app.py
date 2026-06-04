"""agenda_entrenador.app — La aplicación que orquesta los módulos."""

import os

from .pokemon import Pokemon
from .equipo import Equipo
from .batallas import Batalla, Historial, GANO, PERDIO
from . import estadisticas, storage, ui

ARCHIVO = os.path.join(os.path.dirname(os.path.dirname(__file__)), "agenda_datos.json")


class App:
    def __init__(self, ruta=ARCHIVO):
        self.ruta = ruta
        self.capturados = []
        self.equipo = Equipo()
        self.historial = Historial()
        self.cargar()

    # ----- persistencia -----
    def cargar(self):
        estado = storage.cargar(self.ruta)
        self.capturados = [Pokemon.from_dict(d) for d in estado["capturados"]]
        self.equipo = Equipo()
        for nombre in estado["equipo"]:
            p = self.buscar_capturado(nombre)
            if p:
                self.equipo.agregar(p)
        self.historial = Historial()
        for d in estado["batallas"]:
            self.historial.registrar(Batalla.from_dict(d))

    def guardar(self):
        estado = {
            "capturados": [p.to_dict() for p in self.capturados],
            "equipo": self.equipo.to_list(),
            "batallas": self.historial.to_list(),
        }
        storage.guardar(estado, self.ruta)

    # ----- lógica -----
    def buscar_capturado(self, nombre):
        for p in self.capturados:
            if p.nombre.lower() == nombre.lower():
                return p
        return None

    def registrar_captura(self, nombre, tipo, nivel):
        if self.buscar_capturado(nombre):
            return f"{nombre} ya estaba registrado."
        self.capturados.append(Pokemon(nombre, tipo, nivel))
        return f"✅ {nombre} registrado como capturado."

    def registrar_batalla(self, rival, gano, pokemon_usado):
        resultado = GANO if gano else PERDIO
        self.historial.registrar(Batalla(rival, resultado, pokemon_usado))
        return "✅ Batalla registrada."

    def capturados_ordenados(self):
        return estadisticas.capturados_ordenados(self.capturados)

    # ----- interacción -----
    def run(self):
        print(ui.titulo())
        print(f"📂 {len(self.capturados)} capturados, {self.equipo.cantidad()} en equipo, "
              f"{self.historial.total()} batallas.")
        while True:
            print(ui.menu_principal())
            try:
                opcion = input("Opción > ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n¡Chau! 👋")
                return

            if opcion == "1":
                self._ui_captura()
            elif opcion == "2":
                print(ui.formatear_lista(self.capturados_ordenados()))
            elif opcion == "3":
                self._ui_buscar()
            elif opcion == "4":
                self._ui_equipo()
            elif opcion == "5":
                self._ui_batalla()
            elif opcion == "6":
                self._ui_historial()
            elif opcion == "7":
                print(ui.formatear_estadisticas(
                    estadisticas.resumen(self.capturados, self.historial)))
            elif opcion == "8":
                self.guardar()
                print("💾 Guardado.")
            elif opcion == "9":
                self.guardar()
                print("💾 Guardado. ¡Hasta la próxima! 👋")
                return
            else:
                print("⚠️ Opción no válida.")

    def _ui_captura(self):
        nombre = input("  Nombre: ").strip()
        tipo = input("  Tipo: ").strip()
        nivel_txt = input("  Nivel: ").strip()
        nivel = int(nivel_txt) if nivel_txt.isdigit() else 1
        print("  " + self.registrar_captura(nombre, tipo, nivel))

    def _ui_buscar(self):
        nombre = input("  Nombre a buscar: ").strip()
        p = self.buscar_capturado(nombre)
        print("  " + (ui.formatear_pokemon(p) if p else f"{nombre} no está capturado."))

    def _ui_equipo(self):
        print(f"\n  Equipo ({self.equipo.cantidad()}/6): "
              f"{', '.join(self.equipo.nombres()) or '(vacío)'}")
        print("  a) Agregar   q) Quitar")
        sub = input("  Opción > ").strip().lower()
        if sub == "a":
            nombre = input("  Nombre (debe estar capturado): ").strip()
            p = self.buscar_capturado(nombre)
            if p is None:
                print("  ❌ Registralo como capturado primero.")
                return
            print("  " + self.equipo.agregar(p)[1])
        elif sub == "q":
            nombre = input("  Nombre a quitar: ").strip()
            print("  " + self.equipo.quitar(nombre)[1])

    def _ui_batalla(self):
        rival = input("  ¿Contra quién? ").strip()
        gano = input("  ¿Ganaste? (s/n): ").strip().lower().startswith("s")
        pokemon = input("  ¿Qué Pokémon usaste? ").strip()
        print("  " + self.registrar_batalla(rival, gano, pokemon))

    def _ui_historial(self):
        if self.historial.total() == 0:
            print("  (no hay batallas registradas)")
            return
        for b in self.historial.batallas:
            print("  " + ui.formatear_batalla(b))
