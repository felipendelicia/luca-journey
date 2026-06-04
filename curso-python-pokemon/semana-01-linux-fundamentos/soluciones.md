# ✅ Semana 01 — Soluciones

> Acá están los comandos exactos, con explicación de cada flag. **Intentá hacer los ejercicios primero vos.** Mirar la solución sin intentar es como usar un código de trucos: ganás, pero no aprendés. 😉

---

## 🥇 Nivel principiante

### Ejercicio 1 — ¿Dónde estoy?
```bash
pwd
```
- `pwd` = *print working directory*. Muestra la ruta absoluta de tu carpeta actual.

### Ejercicio 2 — Mirar alrededor
```bash
ls
```
- `ls` = *list*. Lista archivos y carpetas de donde estás.

### Ejercicio 3 — Mirar con detalle
```bash
ls -l
```
- `-l` = *long format*. Muestra una línea por archivo con permisos, dueño, tamaño y fecha.

### Ejercicio 4 — Ver lo oculto
```bash
ls -a
```
- `-a` = *all*. Incluye los archivos ocultos, que en Linux son los que empiezan con un punto (`.bashrc`, `.config`, etc.).
- También sirve combinarlo: `ls -la` (oculto + formato largo).

### Ejercicio 5 — Construir el Centro Pokémon
```bash
cd ~
mkdir pokecenter
```
- `cd ~` te asegura estar en tu home antes de crear la carpeta.
- `mkdir pokecenter` = *make directory*. Crea la carpeta.

---

## 🥈 Nivel intermedio

### Ejercicio 6 — Entrar al Centro
```bash
cd pokecenter
pwd
```
- `cd pokecenter` te mete dentro de la carpeta (ruta relativa).
- `pwd` confirma que ahora la ruta termina en `/pokecenter`.

### Ejercicio 7 — Tu equipo favorito
```bash
touch pikachu.txt charizard.txt gengar.txt
```
- `touch` crea archivos vacíos. Podés pasarle varios nombres separados por espacios y los crea todos juntos.

### Ejercicio 8 — Pasar lista
```bash
ls
```
- Deberías ver tus 3 archivos `.txt`.

### Ejercicio 9 — Escribir en la Pokédex
```bash
echo "Tipo: Electrico" > pikachu.txt
```
- `echo "texto"` imprime el texto.
- `>` redirige esa salida hacia el archivo, **reemplazando** su contenido.
- ⚠️ Si usaras `>>` en vez de `>`, en lugar de reemplazar, **agregaría** al final.

### Ejercicio 10 — Leer la Pokédex
```bash
cat pikachu.txt
```
- `cat` muestra el contenido. Deberías ver `Tipo: Electrico`.

---

## 🥉 Nivel avanzado

### Ejercicio 11 — Sala de curación
```bash
mkdir sala-de-curacion
mkdir -p gimnasio/sala-de-batalla
```
- La primera línea crea una carpeta simple.
- `-p` = *parents*. Crea todas las carpetas intermedias que falten. Sin `-p`, si `gimnasio` no existe, daría error.

### Ejercicio 12 — Mudanza
```bash
mv pikachu.txt sala-de-curacion/
```
- `mv origen destino`. Como el destino es una carpeta, el archivo se mueve adentro.

### Ejercicio 13 — Evolución
```bash
mv charizard.txt charizard-mega.txt
```
- Cuando el destino **no es** una carpeta existente, `mv` renombra el archivo.
- (Usé `charizard` porque `pikachu` ya lo moviste en el ejercicio 12, pero podés usar el que quieras.)

### Ejercicio 14 — Backup del Centro
```bash
cd ~
cp -r pokecenter pokecenter-backup
```
- `cp -r origen destino`. El flag `-r` = *recursive*. Sin él, `cp` no copia carpetas, solo archivos sueltos.

### Ejercicio 15 — Limpieza final
```bash
rm pokecenter/charizard-mega.txt
cd ~
rm -r pokecenter-backup
```
- `rm archivo` borra un archivo.
- `rm -r carpeta` borra una carpeta entera con todo adentro.
- ⚠️ No hay papelera: revisá siempre qué estás borrando.

---

## 🏆 Desafío extra — Una forma de resolverlo

```bash
cd ~
mkdir -p region-kanto/pueblo-paleta
mkdir -p region-kanto/ciudad-verde
mkdir -p region-kanto/bosque-verde

touch region-kanto/pueblo-paleta/casa-ash.txt
touch region-kanto/pueblo-paleta/laboratorio-oak.txt
touch region-kanto/ciudad-verde/gimnasio.txt
touch region-kanto/bosque-verde/pokemon-salvajes.txt

ls -R ~/region-kanto
```

- `mkdir -p` crea las carpetas con sus padres de un saque.
- `ls -R` lista **recursivamente**: muestra el árbol completo, carpeta por carpeta.

> 🎉 ¡Si llegaste hasta acá, ya sabés navegar Linux mejor que mucha gente! En la semana 2 le sumamos superpoderes: scripts, pipes y más.
