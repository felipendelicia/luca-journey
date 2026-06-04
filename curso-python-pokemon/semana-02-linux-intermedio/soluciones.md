# ✅ Semana 02 — Soluciones

> Comandos exactos con explicación. Intentá primero, mirá después. 😉

---

## 🥇 Nivel principiante

### Ejercicio 1 — Editar con nano
```bash
nano notas.txt
```
Adentro escribís:
```
Gengar
Fantasma
Nivel 45
```
Guardás con **Ctrl+O** (Enter para confirmar) y salís con **Ctrl+X**.

### Ejercicio 2 — Ver variables de entorno
```bash
echo $HOME
echo $USER
```
- `$HOME` es la ruta de tu carpeta personal; `$USER` tu nombre de usuario.

### Ejercicio 3 — Crear tu variable
```bash
ENTRENADOR="Ash"
echo $ENTRENADOR
```
- ⚠️ No pongas espacios alrededor del `=`. `ENTRENADOR = "Ash"` daría error.

### Ejercicio 4 — Redirección simple
```bash
echo "Pikachu" > equipo.txt
```
- `>` crea el archivo (o lo reemplaza si existía).

### Ejercicio 5 — Agregar sin borrar
```bash
echo "Charizard" >> equipo.txt
echo "Blastoise" >> equipo.txt
```
- `>>` agrega al final, sin pisar "Pikachu".

---

## 🥈 Nivel intermedio

### Ejercicio 6 — Contar líneas con un pipe
```bash
cat equipo.txt | wc -l
```
- `wc -l` cuenta líneas. El pipe `|` le pasa el contenido del archivo.
- (También vale directo: `wc -l equipo.txt`.)

### Ejercicio 7 — Ordenar
```bash
sort equipo.txt
```
- `sort` ordena las líneas alfabéticamente.

### Ejercicio 8 — Buscar con grep
```bash
nano pokedex.txt   # escribí las líneas de ejemplo y guardá
grep "Fuego" pokedex.txt
```
- `grep "texto" archivo` muestra solo las líneas que contienen ese texto.

### Ejercicio 9 — grep sin distinguir mayúsculas
```bash
grep -i "pikachu" pokedex.txt
```
- `-i` = *ignore case*. Encuentra "Pikachu", "PIKACHU", "pikachu", etc.

### Ejercicio 10 — Encontrar archivos
```bash
find ~/practica-semana02 -name "*.txt"
```
- `-name "*.txt"` filtra por nombre; el `*` es comodín (cualquier cosa).

---

## 🥉 Nivel avanzado

### Ejercicio 11 — Tu primer script
```bash
nano saludo.sh
```
Contenido:
```bash
#!/usr/bin/env bash
echo "¡Hola, soy un Entrenador Pokémon!"
```
Después:
```bash
chmod +x saludo.sh
./saludo.sh
```
- `chmod +x` da permiso de ejecución; `./` ejecuta el archivo local.

### Ejercicio 12 — Script con argumento
```bash
#!/usr/bin/env bash
echo "Capturaste a: $1"
```
- `$1` es el primer argumento. Lo corrés con `./saludo.sh Snorlax`.

### Ejercicio 13 — Script que organiza Pokémon por tipo ⭐
```bash
nano organizar.sh
```
Contenido:
```bash
#!/usr/bin/env bash
# Organiza Pokémon por tipo creando una carpeta para cada uno.

# Lista de tipos. En bash, un array se escribe así.
for TIPO in fuego agua planta electrico normal; do
    # Creamos la carpeta del tipo (con -p no falla si ya existe).
    mkdir -p "tipos/$TIPO"
    # Creamos un archivo lista.txt vacío adentro.
    touch "tipos/$TIPO/lista.txt"
    echo "Carpeta creada para el tipo: $TIPO"
done
```
Después:
```bash
chmod +x organizar.sh
./organizar.sh
ls -R tipos    # verificá la estructura
```
- El bucle `for VARIABLE in lista; do ... done` repite los comandos por cada elemento.

### Ejercicio 14 — Ver procesos
```bash
ps aux | grep bash
```
- `ps aux` lista todos los procesos; el pipe a `grep bash` filtra los relevantes.

### Ejercicio 15 — Permisos numéricos
```bash
chmod 755 saludo.sh
ls -l saludo.sh
```
- `755` = dueño `rwx` (7), grupo `r-x` (5), otros `r-x` (5).

---

## 🏆 Desafío extra — Solución

```bash
nano capturar.sh
```
Contenido:
```bash
#!/usr/bin/env bash
# Captura un Pokémon y lo registra con fecha.

# Si $1 está vacío (-z = cadena de longitud cero), mostramos el uso y salimos.
if [ -z "$1" ]; then
    echo "Uso: ./capturar.sh <nombre>"
    exit 1
fi

# Guardamos el nombre en una variable para que se lea mejor.
NOMBRE="$1"

# date imprime la fecha y hora actual. La metemos con $(...).
echo "$NOMBRE - capturado el $(date)" >> capturados.txt

echo "¡$NOMBRE capturado!"
```
Después:
```bash
chmod +x capturar.sh
./capturar.sh Mewtwo
cat capturados.txt
```
- `$(...)` ejecuta un comando y mete su resultado ahí (se llama *command substitution*).
- `exit 1` corta el script con código de error 1 (algo salió mal).

> 🎉 ¡Ya escribís scripts bash de verdad! En la semana 3 arrancamos con **Python**. ⚡
