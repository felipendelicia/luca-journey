---
title: "Linux: Fundamentos"
order: 10
---

> 🎯 **Meta:** moverte por tu computadora usando solo texto, sin mouse. Vas a aprender los comandos básicos de la terminal de Linux.

---

## 🧭 ¿Qué es Linux?

**Linux** es un sistema operativo, igual que Windows o macOS. La diferencia es que es **libre y gratuito**, y lo usan casi todos los servidores del mundo, celulares Android, supercomputadoras... y casi todos los programadores.

Si estás en Windows, podés usar **WSL** (Windows Subsystem for Linux) para tener Linux adentro de Windows. Si estás en Mac, la terminal es muy parecida.

### 🎮 Analogía Pokémon

Pensá en Linux como el **mundo Pokémon** completo: las rutas, las ciudades, los gimnasios. Vos sos el Entrenador que lo recorre.

Y la **terminal** es tu **Pokédex** 📟: una herramienta de texto donde escribís comandos y el sistema te responde. Al principio parece complicada, pero es la herramienta más poderosa que vas a tener.

---

## 📟 La terminal: tu Pokédex del sistema

La terminal (o "consola") es una ventana donde escribís **comandos** y presionás Enter. El sistema ejecuta lo que pediste y te muestra el resultado.

Cuando la abrís, ves algo así:

```
felipe@maquina:~$
```

Eso se llama el **prompt**. Te dice:
- `felipe` → tu usuario (el Entrenador).
- `maquina` → el nombre de la computadora.
- `~` → en qué carpeta estás (`~` significa "tu carpeta personal", tu *home*).
- `$` → "estoy listo, escribí tu comando".

### 🎮 Cada comando es un "ataque"

Así como Pikachu tiene **Impactrueno** o **Ataque Rápido**, vos tenés comandos. Cada uno hace una cosa específica. Aprenderlos es como aprender los movimientos de tu Pokémon: al principio pocos, después un montón.

---

## 🗂️ El sistema de archivos: el mapa del mundo

Todo en Linux está organizado en **carpetas** (también llamadas "directorios"), una adentro de otra, como cajas dentro de cajas. Esto forma un **árbol**.

```
/                        ← la raíz de todo (la región Kanto entera)
├── home/
│   └── felipe/          ← tu carpeta personal (~), tu Pueblo Paleta
│       ├── pokecenter/
│       └── mochila/
├── etc/                 ← configuración del sistema
└── usr/                 ← programas instalados
```

- `/` es la **raíz**: el punto de partida de todo.
- `~` es tu **home**: tu casa, donde guardás tus cosas.

---

## ⚔️ Los comandos básicos (tus primeros ataques)

### `pwd` — ¿Dónde estoy? 📍

`pwd` significa *print working directory*. Te dice en qué carpeta estás parado ahora mismo. Es tu **mapa del pueblo actual**.

```bash
pwd
```
Salida de ejemplo:
```
/home/felipe
```

---

### `ls` — Mirar alrededor 👀

`ls` (*list*) muestra qué hay en la carpeta actual: archivos y otras carpetas. Es como abrir los ojos y ver qué Pokémon hay en el pasto.

```bash
ls
```

Con **flags** (opciones) ves más detalle. Un flag es como un objeto que potencia el ataque:

```bash
ls -l      # formato largo: permisos, tamaño, fecha
ls -a      # muestra TODO, incluso archivos ocultos (empiezan con .)
ls -la     # combinás los dos
```

---

### `cd` — Viajar a otra carpeta 🚶

`cd` (*change directory*) te mueve de una carpeta a otra. Es **viajar por una ruta** del mapa.

```bash
cd pokecenter      # entrás a la carpeta pokecenter
cd ..              # subís un nivel (volvés a la carpeta de arriba)
cd ~               # volvés a tu home (tu Pueblo Paleta)
cd /               # vas a la raíz de todo
cd -               # volvés a la carpeta donde estabas antes
```

---

### `mkdir` — Crear una carpeta 🏗️

`mkdir` (*make directory*) crea una carpeta nueva. Es como **construir un edificio nuevo** en el pueblo.

```bash
mkdir pokecenter           # crea la carpeta pokecenter
mkdir gimnasio pokemart    # crea dos carpetas de una
mkdir -p ruta/larga/nueva  # crea carpetas anidadas de un saque (-p)
```

---

### `touch` y `echo` — Crear archivos ✍️

`touch` crea un archivo vacío. `echo` imprime texto, y con `>` lo podés guardar en un archivo.

```bash
touch pikachu.txt                  # crea un archivo vacío
echo "Pikachu, tipo Eléctrico"     # imprime el texto en pantalla
echo "Pikachu" > pikachu.txt       # escribe el texto DENTRO del archivo
```

---

### `cat` — Leer un archivo 📖

`cat` muestra el contenido de un archivo en pantalla. Es como **leer la entrada de la Pokédex** de un Pokémon.

```bash
cat pikachu.txt
```

---

### `cp` — Copiar 📋

`cp` (*copy*) hace una copia de un archivo o carpeta. Como usar una **Pokéball para duplicar** (bueno, casi).

```bash
cp pikachu.txt pikachu-copia.txt        # copia un archivo
cp -r pokecenter pokecenter-backup      # copia una carpeta entera (-r = recursivo)
```

---

### `mv` — Mover o renombrar 🚚

`mv` (*move*) mueve un archivo de lugar, o lo renombra si le das un nombre nuevo.

```bash
mv pikachu.txt mochila/        # mueve el archivo a la carpeta mochila
mv pikachu.txt raichu.txt      # lo renombra (Pikachu evolucionó a Raichu ⚡)
```

---

### `rm` — Borrar 🗑️ (¡CUIDADO!)

`rm` (*remove*) borra archivos. **En Linux NO hay papelera de reciclaje**: lo que borrás, se va para siempre. Es como liberar un Pokémon: no vuelve.

```bash
rm pikachu.txt           # borra un archivo
rm -r pokecenter         # borra una carpeta y todo su contenido (-r)
```

> ⚠️ **Nunca, jamás** corras `rm -rf /`. Eso intenta borrar TODO el sistema. Es el "Autodestrucción" definitivo. No lo hagas nunca.

---

```quiz
P: Estás en `/home/felipe` y querés ir a `/home/felipe/pokecenter`. ¿Qué comando usás?
- `cd /pokecenter`
- `cd ~pokecenter`
+ `cd pokecenter`
> Como ya estás en `/home/felipe`, podés usar la ruta relativa `pokecenter` directamente. La ruta absoluta `/home/felipe/pokecenter` también funciona, pero es más larga.
```

---

## 🛣️ Rutas absolutas vs relativas

Una **ruta** es la dirección de un archivo o carpeta. Hay dos formas de escribirla:

### Ruta absoluta — la dirección completa
Empieza desde la raíz `/`. Funciona desde cualquier lugar, como dar tu dirección completa con código postal.

```bash
cd /home/felipe/pokecenter
```

### Ruta relativa — desde donde estás parado
No empieza con `/`. Es relativa a tu posición actual, como decir "doblá a la izquierda en la esquina".

```bash
cd pokecenter        # entra a pokecenter que está acá
cd ../mochila        # sube uno y entra a mochila
```

Símbolos clave:
- `.` → la carpeta actual (acá mismo).
- `..` → la carpeta de arriba (el nivel anterior).
- `~` → tu home.
- `/` → la raíz.

---

```quiz
P: ¿Qué hace `mv pikachu.txt raichu.txt`?
- Crea una copia de `pikachu.txt` con el nombre `raichu.txt`
- Borra `pikachu.txt` y crea `raichu.txt` vacío
+ Renombra `pikachu.txt` a `raichu.txt`
> `mv` mueve archivos, pero si el destino es un nombre en la misma carpeta, simplemente renombra. No crea copia: el archivo original desaparece con el nombre viejo.
```

---

## 🔐 Permisos básicos

En Linux, cada archivo tiene **permisos** que dicen quién puede leerlo, escribirlo o ejecutarlo. Es como decidir quién puede entrar a tu gimnasio.

Cuando corrés `ls -l`, ves algo así:

```
-rwxr-xr--  1 felipe felipe  220 jun  4 10:00 pikachu.txt
```

Esa primera columna `-rwxr-xr--` son los permisos:
- Primer carácter: `-` archivo, `d` directorio.
- Después, en grupos de 3: **dueño**, **grupo**, **otros**.
- `r` = leer (*read*), `w` = escribir (*write*), `x` = ejecutar (*execute*).

Por ahora solo necesitás **reconocerlos**. Más adelante vas a aprender a cambiarlos con `chmod`.

---

## 📝 Resumen

| Comando | Qué hace | Analogía Pokémon |
|---------|----------|------------------|
| `pwd` | Dice dónde estás | Mirar el mapa |
| `ls` | Lista archivos y carpetas | Ver qué hay alrededor |
| `cd` | Cambia de carpeta | Viajar por una ruta |
| `mkdir` | Crea una carpeta | Construir un edificio |
| `touch` | Crea un archivo vacío | Conseguir un objeto nuevo |
| `echo` | Imprime texto | Hablar |
| `cat` | Muestra un archivo | Leer la Pokédex |
| `cp` | Copia | Duplicar |
| `mv` | Mueve o renombra | Mudarse / evolucionar |
| `rm` | Borra (¡sin papelera!) | Liberar (no vuelve) |

**Rutas:** absoluta empieza con `/`, relativa desde donde estás. `.` = acá, `..` = arriba, `~` = home.

**Permisos:** `r` leer, `w` escribir, `x` ejecutar.

---

## ➡️ ¿Y ahora qué?

Probá los comandos vos mismo y seguí con el próximo capítulo para sumar más herramientas a tu Pokédex. 💪

> ⚡ *"Todo gran Entrenador empezó sin saber usar la Pokédex. Vos ya diste el primer paso."*
