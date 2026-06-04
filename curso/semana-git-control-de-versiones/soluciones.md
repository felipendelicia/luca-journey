# ✅ Semana de Git — Soluciones

> Comandos exactos con explicación. Intentá primero, mirá después. 😉

---

## 🥇 Nivel principiante

### Ejercicio 1 — Presentate ante Git
```bash
git config --global user.name "Ash Ketchum"
git config --global user.email "ash@pueblopaleta.com"
```
- `--global` lo configura para todos tus proyectos. Se hace una sola vez.

### Ejercicio 2 — Crear el repositorio
```bash
git init
```
- Crea la carpeta oculta `.git/` donde Git guarda la historia.

### Ejercicio 3 — Ver el estado
```bash
git status
```
- Te dice en qué rama estás y que todavía no hay commits.

### Ejercicio 4 — Tu primer archivo
```bash
echo "Pikachu" > equipo.txt
```
- `>` crea el archivo con ese contenido.

### Ejercicio 5 — Ver el estado de nuevo
```bash
git status
```
- Ahora `equipo.txt` aparece en rojo como **Untracked files**: Git lo ve pero todavía no lo sigue.

---

## 🥈 Nivel intermedio

### Ejercicio 6 — Preparar el archivo
```bash
git add equipo.txt
```
- Mueve el archivo al **staging area**: "esto quiero guardarlo".

### Ejercicio 7 — Tu primer commit
```bash
git commit -m "Mi primer commit: agregué a mi Pokémon favorito"
```
- Crea el punto de guardado. El `-m` es el mensaje.

### Ejercicio 8 — Ver la historia
```bash
git log
git log --oneline
```
- `git log` muestra los commits completos; `--oneline` los muestra cortitos.

### Ejercicio 9 — Segundo guardado
```bash
echo "Charizard" >> equipo.txt
git add equipo.txt
git commit -m "Agregué a Charizard al equipo"
```
- `>>` agrega sin borrar. Después: preparar (`add`) y guardar (`commit`).

### Ejercicio 10 — Preparar todo de una
```bash
touch pokedex.txt mochila.txt
git add .
```
- El `.` significa "todos los cambios". `git add .` prepara los dos archivos juntos.
- (Después podrías commitearlos: `git commit -m "Agregué pokedex y mochila"`.)

---

## 🥉 Nivel avanzado

### Ejercicio 11 — Crear una rama
```bash
git branch nueva-aventura
```
- Crea la rama, pero NO te cambia a ella todavía.

### Ejercicio 12 — Cambiarte a la rama
```bash
git switch nueva-aventura
git status            # confirma: "On branch nueva-aventura"
```
- `git switch` te mueve a la rama. (`git checkout nueva-aventura` hace lo mismo.)

### Ejercicio 13 — Commitear en la rama
```bash
echo "informacion clasificada" > secreto.txt
git add secreto.txt
git commit -m "Agregué un archivo secreto en la rama"
```
- Este commit vive solo en `nueva-aventura`.

### Ejercicio 14 — Volver a main y fusionar
```bash
git switch main
ls                    # secreto.txt NO está acá
git merge nueva-aventura
ls                    # ahora secreto.txt SÍ aparece
```
- Al fusionar, los cambios de `nueva-aventura` entran en `main`.

### Ejercicio 15 — Ignorar archivos
```bash
echo "temporal/" > .gitignore
mkdir temporal
echo "basura" > temporal/cosa.txt
git status            # Git NO muestra temporal/, lo ignora
```
- Lo que listás en `.gitignore`, Git lo ignora por completo.

---

## 🏆 Desafío extra — Solución

```bash
# (Después de crear el repo vacío en GitHub)
git remote add origin https://github.com/TU-USUARIO/TU-REPO.git
git branch -M main
git push -u origin main
```
- `remote add origin` conecta tu repo local con GitHub.
- `git branch -M main` asegura que tu rama se llame `main`.
- `git push -u origin main` sube todo. El `-u` recuerda la conexión para los próximos `git push`.

> 🎉 ¡Ya sabés Git! Esta habilidad te va a acompañar toda tu carrera. Ahora, de vuelta a Python. 🐍
