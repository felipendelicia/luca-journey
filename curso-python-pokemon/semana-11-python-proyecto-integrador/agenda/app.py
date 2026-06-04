"""
agenda.app — La aplicación que orquesta todos los módulos.

Mantiene el estado (capturados, equipo, historial), lo persiste con storage y
muestra todo con ui. La lógica está separada de la entrada/salida para testear.
"""

import os

from .pokemon import Pokemon
from .equipo import Equipo
from .batallas import Batalla, Historial, GANO, PERDIO
from . import estadisticas, storage, ui

# Archivo por defecto, al lado del paquete.
ARCHIVO = os.path.join(os.path.dirname(os.path.dirname(__file__)), "agenda_datos.json")


class App:
    """Estado de la agenda + orquestación de los módulos."""

    def __init__(self, ruta=ARCHIVO):
        self.ruta = ruta
        self.capturados = []        # lista de Pokemon
        self.equipo = Equipo()
        self.historial = Historial()
        self.cargar()

    # ------------------------------------------------------------------
    #  Persistencia: objetos <-> diccionarios.
    # ------------------------------------------------------------------
    def cargar(self):
        estado = storage.cargar(self.ruta)
        self.capturados = [Pokemon.from_dict(d) for d in estado["capturados"]]
        self.equipo = Equipo()
        for nombre in estado["equipo"]:
            p = self._buscar_capturado(nombre)
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

    def _buscar_capturado(self, nombre):
        for p in self.capturados:
            if p.nombre.lower() == nombre.lower():
                return p
        return None

    # ------------------------------------------------------------------
    #  Acciones (lógica pura, sin input/print).
    # ------------------------------------------------------------------
    def registrar_captura(self, nombre, tipo, nivel):
        if self._buscar_capturado(nombre):
            return f"{nombre} ya estaba registrado."
        self.capturados.append(Pokemon(nombre, tipo, nivel))
        return f"✅ {nombre} registrado como capturado."

    def registrar_batalla(self, rival, gano, pokemon_usado):
        resultado = GANO if gano else PERDIO
        self.historial.registrar(Batalla(rival, resultado, pokemon_usado))
        return "✅ Batalla registrada."

    # ------------------------------------------------------------------
    #  Bucle interactivo.
    # ------------------------------------------------------------------
    def run(self):
        print(ui.titulo())
        print(f"📂 Cargados: {len(self.capturados)} capturados, "
              f"{self.equipo.cantidad()} en el equipo, "
              f"{self.historial.total()} batallas.")

        while True:
            print(ui.menu_principal())
            try:
                opcion = input("Opción > ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n¡Chau, Entrenador! 👋")
                return

            if opcion == "1":
                self._ui_registrar_captura()
            elif opcion == "2":
                print(ui.formatear_lista_capturados(self.capturados))
            elif opcion == "3":
                self._ui_gestionar_equipo()
            elif opcion == "4":
                self._ui_registrar_batalla()
            elif opcion == "5":
                self._ui_ver_historial()
            elif opcion == "6":
                resumen = estadisticas.resumen(self.capturados, self.historial)
                print(ui.formatear_estadisticas(resumen))
            elif opcion == "7":
                self.guardar()
                print("💾 Guardado.")
            elif opcion == "8":
                self.guardar()
                print("💾 Guardado. ¡Hasta la próxima, Entrenador! 👋")
                return
            else:
                print("⚠️ Opción no válida.")

    def _ui_registrar_captura(self):
        nombre = input("  Nombre: ").strip()
        tipo = input("  Tipo: ").strip()
        nivel_txt = input("  Nivel: ").strip()
        nivel = int(nivel_txt) if nivel_txt.isdigit() else 1
        print("  " + self.registrar_captura(nombre, tipo, nivel))

    def _ui_gestionar_equipo(self):
        print(f"\n  Equipo actual ({self.equipo.cantidad()}/6): "
              f"{', '.join(self.equipo.nombres()) or '(vacío)'}")
        print("  a) Agregar al equipo   q) Quitar del equipo")
        sub = input("  Opción > ").strip().lower()
        if sub == "a":
            nombre = input("  Nombre (debe estar capturado): ").strip()
            p = self._buscar_capturado(nombre)
            if p is None:
                print("  ❌ Ese Pokémon no está capturado. Registralo primero.")
                return
            ok, msg = self.equipo.agregar(p)
            print("  " + msg)
        elif sub == "q":
            nombre = input("  Nombre a quitar: ").strip()
            ok, msg = self.equipo.quitar(nombre)
            print("  " + msg)

    def _ui_registrar_batalla(self):
        rival = input("  ¿Contra quién peleaste? ").strip()
        resultado = input("  ¿Ganaste? (s/n): ").strip().lower()
        gano = resultado.startswith("s")
        pokemon = input("  ¿Qué Pokémon usaste? ").strip()
        print("  " + self.registrar_batalla(rival, gano, pokemon))

    def _ui_ver_historial(self):
        if self.historial.total() == 0:
            print("  (no hay batallas registradas)")
            return
        print("\n  --- HISTORIAL DE BATALLAS ---")
        for b in self.historial.batallas:
            print("  " + ui.formatear_batalla(b))
