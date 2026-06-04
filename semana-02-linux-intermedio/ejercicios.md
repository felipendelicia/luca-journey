# ✏️ Semana 02 — Ejercicios de terminal

> 🎮 Practicá en tu terminal de verdad. Las respuestas están en `soluciones.md`, pero intentá primero.
>
> 💡 Trabajá dentro de una carpeta de práctica para no ensuciar tu home:
> ```bash
> mkdir -p ~/practica-semana02 && cd ~/practica-semana02
> ```

---

## 🥇 Nivel principiante

### Ejercicio 1 — Editar con nano
Abrí nano y creá un archivo `notas.txt` con tres líneas: el nombre de tu Pokémon favorito, su tipo, y su nivel. Guardalo y salí.

### Ejercicio 2 — Ver variables de entorno
Mostrá en pantalla el valor de tu variable `$HOME` y de `$USER`.

### Ejercicio 3 — Crear tu variable
Creá una variable llamada `ENTRENADOR` con tu nombre, y después mostrala con `echo`.

### Ejercicio 4 — Redirección simple
Usá `echo` y `>` para crear un archivo `equipo.txt` con la línea "Pikachu".

### Ejercicio 5 — Agregar sin borrar
Agregá al archivo `equipo.txt` (sin borrar lo anterior) las líneas "Charizard" y "Blastoise", usando `>>`.

---

## 🥈 Nivel intermedio

### Ejercicio 6 — Contar líneas con un pipe
Mostrá cuántas líneas tiene `equipo.txt` combinando `cat` (o `ls`) con `wc -l` usando un pipe.

### Ejercicio 7 — Ordenar
Mostrá el contenido de `equipo.txt` ordenado alfabéticamente (pista: el comando `sort`).

### Ejercicio 8 — Buscar con grep
Creá un archivo `pokedex.txt` con varias líneas tipo `Pikachu - Electrico`, `Charizard - Fuego`, `Squirtle - Agua`. Después usá `grep` para mostrar solo las líneas que contengan "Fuego".

### Ejercicio 9 — grep sin distinguir mayúsculas
Buscá "pikachu" (en minúscula) dentro de `pokedex.txt` pero que igual encuentre "Pikachu". Usá el flag correcto.

### Ejercicio 10 — Encontrar archivos
Usá `find` para listar todos los archivos `.txt` que tengas dentro de `~/practica-semana02`.

---

## 🥉 Nivel avanzado

### Ejercicio 11 — Tu primer script
Creá un script `saludo.sh` que imprima "¡Hola, soy un Entrenador Pokémon!". Dale permisos de ejecución y corrélo.

### Ejercicio 12 — Script con argumento
Modificá `saludo.sh` para que reciba un argumento y diga "Capturaste a: <lo-que-pases>". Probá con `./saludo.sh Snorlax`.

### Ejercicio 13 — Script que organiza Pokémon por tipo ⭐
Escribí un script `organizar.sh` que cree una estructura de carpetas para organizar Pokémon por tipo. Tiene que crear estas carpetas dentro de una carpeta `tipos/`:
```
tipos/
├── fuego/
├── agua/
├── planta/
├── electrico/
└── normal/
```
Y dentro de cada una, crear un archivo `lista.txt` vacío. Usá `mkdir -p` y un bucle `for` si te animás.

### Ejercicio 14 — Ver procesos
Mostrá todos los procesos del sistema y filtralos con un pipe para ver solo los que tengan que ver con `bash`.

### Ejercicio 15 — Permisos numéricos
Cambiá los permisos de `saludo.sh` a `755` usando `chmod` en formato numérico. Después verificá con `ls -l` que quedó como `-rwxr-xr-x`.

---

## 🏆 Desafío extra (opcional)

Escribí un script `capturar.sh` que:
1. Reciba el nombre de un Pokémon como argumento (`$1`).
2. Si no le pasás ningún argumento, imprima "Uso: ./capturar.sh <nombre>" y termine.
3. Si le pasás un nombre, agregue ese nombre a un archivo `capturados.txt` con la fecha actual (pista: el comando `date`).
4. Imprima "¡<nombre> capturado!".

Pista para el punto 2:
```bash
if [ -z "$1" ]; then
    echo "Uso: ./capturar.sh <nombre>"
    exit 1
fi
```
