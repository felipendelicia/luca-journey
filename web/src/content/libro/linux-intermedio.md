---
title: "Linux: Intermedio"
order: 20
---

> 🎯 **Meta de la semana:** dejar de ser un Entrenador novato y convertirte en uno que **configura su propia base de operaciones**. Vas a editar archivos, escribir tus primeros scripts, encadenar comandos y manejar procesos.

---

## 🎮 Analogía: tu base de operaciones

En la semana 1 aprendiste a caminar por el mundo Pokémon. Esta semana **construís tu base**: automatizás tareas, organizás tu información y le das poder a tu Pokédex.

Un Entrenador avanzado no captura Pokémon uno por uno a mano: arma **máquinas** (scripts) que hacen el trabajo repetitivo por él. Eso es lo que vas a aprender.

---

## ✍️ El editor nano

Hasta ahora creabas archivos con `touch` y `echo`. Para escribir texto largo, usás un **editor**. El más fácil es **nano**.

```bash
nano captura.txt
```

Esto abre el editor. Escribís lo que quieras, y abajo ves los atajos:
- `^O` (Ctrl+O) → guardar (*write Out*). Te pide confirmar el nombre, apretás Enter.
- `^X` (Ctrl+X) → salir.
- `^K` → cortar una línea, `^U` → pegar.
- `^W` → buscar texto.

> 💡 El `^` significa la tecla **Ctrl**. Así que `^X` = Ctrl + X.

---

## 🌍 Variables de entorno

Una **variable de entorno** es un dato que el sistema guarda con un nombre, disponible para todos los programas. Es como tener **objetos clave guardados en tu mochila** que cualquier programa puede consultar.

```bash
echo $HOME          # muestra la ruta de tu home
echo $USER          # tu nombre de usuario
echo $PATH          # las carpetas donde el sistema busca comandos
```

Crear tu propia variable:

```bash
ENTRENADOR="Ash"          # creamos la variable (¡sin espacios alrededor del =!)
echo $ENTRENADOR          # la usamos con $ adelante
export ENTRENADOR         # la hacemos visible para otros programas
```

---

## 📜 Scripts bash básicos

Un **script** es un archivo de texto con una lista de comandos que se ejecutan en orden. Es tu **máquina automática**.

Creá un archivo `hola.sh`:

```bash
#!/usr/bin/env bash
# La primera línea (el "shebang") dice qué programa ejecuta el script.

echo "¡Hola, Entrenador!"
echo "Hoy es un buen día para atrapar Pokémon."
```

Para correrlo, primero le das permiso de ejecución y después lo ejecutás:

```bash
chmod +x hola.sh      # +x = agregar permiso de ejecución
./hola.sh             # ./ significa "ejecutá este archivo de acá"
```

### Variables y argumentos en scripts

```bash
#!/usr/bin/env bash
NOMBRE="Pikachu"
echo "Mi Pokémon es $NOMBRE"

# $1 es el primer argumento que le pasás al script.
echo "Capturaste a: $1"
```

Lo ejecutás así: `./script.sh Charizard` → imprime "Capturaste a: Charizard".

---

## ➡️ Redirección: `>` y `>>`

La **redirección** manda la salida de un comando a un archivo en vez de a la pantalla.

```bash
echo "Pikachu" > equipo.txt      # > CREA o REEMPLAZA el archivo
echo "Charizard" >> equipo.txt   # >> AGREGA al final (no borra lo anterior)
```

> ⚠️ Cuidado: `>` pisa todo lo que había. `>>` suma. Confundirlos borra datos.

---

## 🔗 Pipes: `|`

Un **pipe** (tubería) conecta la salida de un comando con la entrada de otro. Es como hacer que **dos Pokémon combinen ataques**.

```bash
ls | wc -l         # ls lista archivos, wc -l cuenta cuántas líneas → cuántos archivos hay
cat equipo.txt | sort   # muestra el equipo ordenado alfabéticamente
```

---

## 🔍 grep: buscar texto

`grep` busca un texto dentro de archivos o de lo que le llega por pipe. Es tu **detector de Pokémon**.

```bash
grep "Pikachu" equipo.txt          # muestra las líneas que contienen "Pikachu"
grep -i "pikachu" equipo.txt       # -i = ignora mayúsculas/minúsculas
grep -r "Fuego" carpeta/           # -r = busca recursivamente en una carpeta
cat pokedex.txt | grep "Electrico" # buscar combinando con un pipe
```

---

## 🗺️ find: encontrar archivos

`grep` busca **dentro** de archivos. `find` busca **los archivos en sí**.

```bash
find . -name "*.txt"           # busca todos los .txt desde la carpeta actual
find ~ -name "pikachu*"        # busca en tu home archivos que empiecen con pikachu
find . -type d                 # busca solo carpetas (type d = directory)
```

---

## ⚙️ Procesos: ps y kill

Un **proceso** es un programa corriendo. Como un Pokémon activo en batalla.

```bash
ps                  # muestra tus procesos
ps aux              # muestra TODOS los procesos del sistema (mucha info)
ps aux | grep python   # filtra para ver solo los de python
```

Si un programa se cuelga, lo "debilitás" con `kill`:

```bash
kill 1234           # 1234 es el PID (número de proceso). Pedido amable de cerrar.
kill -9 1234        # -9 = cierre forzado. El "golpe crítico". Usar solo si hace falta.
```

---

## 🔐 chmod: cambiar permisos

En la semana 1 aprendiste a **leer** los permisos. Ahora los **cambiás** con `chmod`.

```bash
chmod +x script.sh      # agrega permiso de ejecución (la forma más común)
chmod -x script.sh      # quita el permiso de ejecución
chmod 755 script.sh     # forma numérica (avanzada): dueño rwx, grupo y otros r-x
```

La forma numérica: cada dígito es la suma de `r`=4, `w`=2, `x`=1.
- `7` = 4+2+1 = rwx (todo)
- `5` = 4+0+1 = r-x (leer y ejecutar)
- `6` = 4+2+0 = rw- (leer y escribir)

---

## 👥 Usuarios y permisos: sudo

Linux es **multiusuario**. El usuario todopoderoso se llama **root** (el Profesor Oak del sistema: tiene acceso a todo).

`sudo` ejecuta UN comando como root. Te pide tu contraseña.

```bash
sudo apt update     # actualizar la lista de programas (necesita permisos de root)
```

> ⚠️ `sudo` es poderoso. Con gran poder viene gran responsabilidad. No corras comandos con `sudo` que no entiendas.

---

## 📦 apt: instalar programas

En Ubuntu/Debian, `apt` es el **PokéMart**: ahí instalás programas.

```bash
sudo apt update              # actualiza la lista de programas disponibles
sudo apt install cowsay      # instala un programa (en este caso, una vaca que habla)
sudo apt remove cowsay       # lo desinstala
```

---

## 🔌 SSH: conectarte a otra máquina

**SSH** (*Secure Shell*) te deja controlar **otra computadora** por la terminal, de forma segura. Es como usar tu Pokédex para conectarte a un **gimnasio remoto**.

```bash
ssh entrenador@192.168.1.50      # te conectás a esa máquina con ese usuario
```

Te va a pedir contraseña, y después tenés una terminal en la máquina remota. Esto es la base de cómo se administran los servidores del mundo.

> 💡 Por ahora solo necesitás saber **qué es**. Cuando tengas un servidor (o una Raspberry Pi), lo vas a usar todo el tiempo.

---

## 📝 Resumen de la semana

| Comando | Qué hace |
|---------|----------|
| `nano archivo` | Edita un archivo de texto |
| `$VARIABLE` / `export` | Variables de entorno |
| `chmod +x` | Da permiso de ejecución |
| `./script.sh` | Ejecuta un script |
| `>` / `>>` | Redirige salida (reemplaza / agrega) |
| `\|` (pipe) | Conecta salida de un comando con otro |
| `grep` | Busca texto dentro de archivos |
| `find` | Busca archivos por nombre/tipo |
| `ps` / `kill` | Ver y cerrar procesos |
| `sudo` | Ejecuta como root |
| `apt` | Instala/desinstala programas |
| `ssh` | Te conecta a otra máquina |

---

## ➡️ ¿Y ahora qué?

1. Hacé los ejercicios de `ejercicios.md` en tu terminal.
2. Jugá el `interactivo.py`: te guía a escribir tu **primer script bash real**.
   ```bash
   python interactivo.py
   ```
3. Poné a prueba lo aprendido con el quiz:
   ```bash
   python quiz.py
   ```

> ⚡ *"Un Entrenador que automatiza su trabajo tiene más tiempo para entrenar. Trabajá inteligente, no solo duro."*
