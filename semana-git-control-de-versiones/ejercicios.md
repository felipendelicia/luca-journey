# ✏️ Semana de Git — Ejercicios de terminal

> 🎮 Practicá con **Git de verdad** en tu terminal. Las respuestas están en `soluciones.md`, pero intentá primero.
>
> 💡 Empezá creando una carpeta de práctica:
> ```bash
> mkdir -p ~/practica-git && cd ~/practica-git
> ```

---

## 🥇 Nivel principiante

### Ejercicio 1 — Presentate ante Git
Configurá tu nombre y tu email en Git (solo si nunca lo hiciste). Usá tu nombre y un email cualquiera.

### Ejercicio 2 — Crear el repositorio
Dentro de `~/practica-git`, iniciá un repositorio de Git.

### Ejercicio 3 — Ver el estado
Pedile a Git que te muestre el estado actual del repo. (Debería decir que no hay commits todavía.)

### Ejercicio 4 — Tu primer archivo
Creá un archivo llamado `equipo.txt` y escribí adentro el nombre de tu Pokémon favorito (podés usar `echo "Pikachu" > equipo.txt`).

### Ejercicio 5 — Ver el estado de nuevo
Volvé a mirar el estado. Ahora `equipo.txt` debería aparecer como archivo "untracked" (sin seguir).

---

## 🥈 Nivel intermedio

### Ejercicio 6 — Preparar el archivo
Prepará `equipo.txt` para guardarlo (agregalo al staging).

### Ejercicio 7 — Tu primer commit
Guardá la partida con el mensaje "Mi primer commit: agregué a mi Pokémon favorito".

### Ejercicio 8 — Ver la historia
Mostrá la historia de commits. Deberías ver tu commit. Probá también la versión de una sola línea.

### Ejercicio 9 — Segundo guardado
Agregá una línea más a `equipo.txt` (otro Pokémon), preparalo y hacé un segundo commit con un mensaje descriptivo.

### Ejercicio 10 — Preparar todo de una
Creá dos archivos nuevos (`pokedex.txt` y `mochila.txt`), y preparalos a **los dos juntos** con un solo comando.

---

## 🥉 Nivel avanzado

### Ejercicio 11 — Crear una rama
Creá una rama nueva llamada `nueva-aventura`.

### Ejercicio 12 — Cambiarte a la rama
Cambiate a la rama `nueva-aventura`. Confirmá con un comando que estás parado en ella.

### Ejercicio 13 — Commitear en la rama
Estando en `nueva-aventura`, creá un archivo `secreto.txt`, preparalo y commiteá. Este cambio vive solo en esta rama.

### Ejercicio 14 — Volver a main y fusionar
Volvé a la rama `main`. Fijate que `secreto.txt` no está (¡está en la otra línea temporal!). Después fusioná `nueva-aventura` en `main` y volvé a mirar: ahora sí aparece.

### Ejercicio 15 — Ignorar archivos
Creá un archivo `.gitignore` que ignore una carpeta llamada `temporal/`. Después creá la carpeta `temporal/` con un archivo adentro y verificá con `git status` que Git la ignora.

---

## 🏆 Desafío extra (opcional, con GitHub)

Si tenés una cuenta de GitHub:

1. Creá un repositorio **vacío** en GitHub (sin README).
2. Conectá tu repo local con el de GitHub (`git remote add origin ...`).
3. Subí tu trabajo con `git push -u origin main`.
4. Entrá a tu repo en GitHub desde el navegador y mirá tus archivos ahí arriba. ☁️

> 💡 ¡Felicitaciones! Acabás de hacer exactamente lo que hacen los programadores todos los días.
