---
title: "Git: Control de Versiones"
order: 1390
---

> 😌 **Capítulo relajado.** Después de tanto Python, frenamos un toque para aprender **Git**: la herramienta que usan TODOS los programadores para guardar su trabajo. Es fácil, es útil, y te va a salvar la vida mil veces.

---

## 🎮 Analogía: Git es "guardar la partida"

¿Te acordás cuando jugás Pokémon y **guardás la partida** antes de una pelea difícil? Si perdés, recargás y volvés al punto de guardado. 💾

**Git es exactamente eso, pero para tu código.** Cada vez que hacés un "guardado" (se llama **commit**), Git recuerda cómo estaba TODO tu proyecto en ese momento. ¿Rompiste algo? Volvés a un guardado anterior. ¿Querés probar una idea loca sin arruinar lo que funciona? Creás una **línea temporal alternativa** (una *branch*).

| En Pokémon | En Git |
|------------|--------|
| Guardar la partida | Hacer un **commit** |
| El cartucho/partida | El **repositorio** |
| La PC de Bill (en la nube) | **GitHub** |
| Subir Pokémon a la PC | **push** |
| Bajar Pokémon de la PC | **pull** |
| Copiar la partida de un amigo | **clone** |
| Un universo paralelo (Ultraentes) | Una **branch** (rama) |

---

## ❓ ¿Por qué usar Git?

- 💾 **Nunca más perdés tu trabajo.** Cada commit es un punto seguro.
- ⏪ **Volvés atrás** cuando rompés algo (y vas a romper cosas, es normal).
- 🌿 **Probás ideas** sin miedo, en ramas separadas.
- 👥 **Trabajás con otros** sin pisarse el código.
- ☁️ **Guardás todo en GitHub**, accesible desde cualquier lado.
- 💼 Todo programador lo usa. Saberlo es **obligatorio** en el mundo real.

---

## 🛠️ Configuración inicial (una sola vez)

Antes de usar Git, le decís quién sos (queda en tus commits):

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

Esto se hace **una sola vez** en tu computadora.

---

## 📦 Crear un repositorio: git init

Un **repositorio** (o "repo") es una carpeta que Git está vigilando. Para empezar a vigilar una carpeta:

```bash
cd mi-proyecto
git init
```

Esto crea una carpeta oculta `.git/` donde Git guarda toda la historia. **No la toques**, es la "memoria" de Git.

---

## 👀 Ver el estado: git status

`git status` es tu mejor amigo. Te dice qué cambió, qué está listo para guardar y qué no. **Usalo todo el tiempo.**

```bash
git status
```

Te muestra cosas como:
- **Untracked files**: archivos nuevos que Git todavía no sigue.
- **Changes to be committed**: cambios listos para el próximo commit (en el "staging").
- **Changes not staged**: cambios que hiciste pero todavía no preparaste.

---

## 🎬 Los 3 pasos de un guardado

Guardar en Git tiene 3 zonas, como preparar tu equipo antes de una batalla:

```
  Working Directory  →  Staging Area  →  Repositorio
  (donde trabajás)      (lo que vas        (guardado
                         a guardar)          permanente)
        │                    │                   │
     editás            git add             git commit
```

### 1. `git add` — preparar lo que vas a guardar

```bash
git add pokemon.txt        # prepara un archivo
git add .                  # prepara TODOS los cambios (el punto = "todo")
```

`git add` mueve tus cambios al **staging area**: "esto quiero guardarlo".

### 2. `git commit` — guardar la partida

```bash
git commit -m "Agregué a Pikachu al equipo"
```

`commit` crea el punto de guardado. El `-m` es el **mensaje**: una descripción de QUÉ hiciste. Escribí mensajes claros, tu yo del futuro te lo agradece.

> 💡 Regla de oro: `git add` → `git commit`. Primero preparás, después guardás.

---

## 📜 Ver la historia: git log

`git log` muestra todos tus commits, del más nuevo al más viejo:

```bash
git log
git log --oneline      # versión cortita, una línea por commit
```

Cada commit tiene un código único (un "hash") y tu mensaje. Es la lista de todos tus puntos de guardado. 🗂️

---

## 🌿 Ramas (branches): líneas temporales alternativas

Una **branch** (rama) es una **línea temporal paralela** de tu proyecto. Te deja probar cosas sin tocar lo que ya funciona. Es como entrar a un universo alternativo: si sale mal, volvés al principal y no pasó nada.

```bash
git branch                       # muestra las ramas (la actual tiene un *)
git branch nueva-aventura        # crea una rama nueva
git switch nueva-aventura        # te cambiás a esa rama
git switch -c otra-rama          # crea Y se cambia, todo junto
```

> 💡 `git checkout nueva-aventura` hace lo mismo que `git switch`. `switch` es la forma nueva y más clara; vas a ver las dos por ahí.

La rama principal se suele llamar **`main`** (antes se llamaba `master`).

```
        o---o---o  nueva-aventura   ← probás cosas acá
       /
  o---o---o---o  main               ← lo estable queda intacto acá
```

---

## 🔗 Fusionar ramas: git merge

Cuando tu experimento en la rama funcionó, lo **fusionás** de vuelta a `main`:

```bash
git switch main              # te parás en la rama destino
git merge nueva-aventura     # traés los cambios de la otra rama
```

Las dos líneas temporales se unen en una. 🤝

---

## ☁️ GitHub: la PC de Bill en la nube

**GitHub** es un sitio web donde guardás tus repos en internet. Es como subir tus Pokémon a la **PC de Bill**: quedan seguros y los podés bajar desde cualquier computadora.

### Conectar tu repo con GitHub

```bash
git remote add origin https://github.com/usuario/repo.git
```

`origin` es el "apodo" de tu repo en GitHub.

### Subir cambios: git push

```bash
git push -u origin main      # la primera vez (-u recuerda la conexión)
git push                     # las siguientes veces, alcanza con esto
```

### Bajar cambios: git pull

```bash
git pull                     # trae los cambios nuevos de GitHub
```

### Copiar un repo de internet: git clone

```bash
git clone https://github.com/usuario/repo.git
```

`clone` te baja una copia completa de un repo (con toda su historia). Así empezaste vos este curso. 😉

---

## 🙈 .gitignore: lo que Git debe ignorar

A veces hay archivos que **no** querés guardar (datos temporales, contraseñas, el `venv`). Los listás en un archivo llamado `.gitignore` y Git los ignora:

```
# .gitignore
venv/
__pycache__/
*.db
progreso.json
```

> 💡 Este mismo curso tiene un `.gitignore`. Abrilo y mirá qué ignora.

---

## 🔄 El flujo de trabajo típico (memorizalo)

```bash
# 1. Trabajás, editás archivos...
# 2. Ves qué cambió
git status
# 3. Preparás los cambios
git add .
# 4. Guardás con un mensaje
git commit -m "Descripción de lo que hice"
# 5. Subís a GitHub
git push
```

Este ciclo lo vas a repetir **miles** de veces en tu vida de programador. 🔁

---

## 📝 Resumen

| Comando | Qué hace |
|---------|----------|
| `git init` | Empieza a vigilar una carpeta |
| `git status` | Muestra qué cambió |
| `git add <archivo>` | Prepara cambios (staging) |
| `git add .` | Prepara TODOS los cambios |
| `git commit -m "msg"` | Guarda la partida (punto de guardado) |
| `git log` | Muestra la historia de commits |
| `git branch <nombre>` | Crea una rama |
| `git switch <nombre>` | Cambia de rama |
| `git switch -c <nombre>` | Crea y cambia de rama |
| `git merge <rama>` | Fusiona una rama en la actual |
| `git remote add origin <url>` | Conecta con GitHub |
| `git push` | Sube a GitHub |
| `git pull` | Baja de GitHub |
| `git clone <url>` | Copia un repo de internet |

---

## ✅ Comprobá lo que aprendiste

```quiz
P: En la analogía del libro, hacer un `commit` es como…
+ guardar la partida en Pokémon
- apagar la consola sin guardar
- borrar el cartucho
> Cada commit es un punto de guardado al que siempre podés volver.
```

```quiz
P: ¿Qué comando SUBE tus commits a GitHub?
+ git push
- git pull
- git status
> `push` empuja tus cambios a la nube; `pull` los baja. Regla rápida: pu**SH** = su**bir**.
```

```quiz
P: Querés probar una idea sin arruinar lo que ya funciona. ¿Qué creás?
+ una rama (branch) con `git switch -c`
- un commit con `git commit`
- un repositorio nuevo con `git init`
> La rama es una línea temporal alternativa: experimentás ahí y, si funciona, la fusionás (`merge`).
```

---

## ➡️ ¿Y ahora qué?

Probá los comandos vos mismo y seguí con el próximo capítulo para sumar más herramientas a tu Pokédex. 💪

> ⚡ *"Programar sin Git es como jugar Pokémon sin poder guardar la partida. Una vez que lo usás, no querés volver atrás."*
