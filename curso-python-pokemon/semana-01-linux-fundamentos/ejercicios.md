# ✏️ Semana 01 — Ejercicios de terminal

> 🎮 Hacé estos ejercicios en tu **terminal de verdad**. Escribí cada comando vos mismo, no copies y pegues. Si te trabás, las respuestas están en `soluciones.md`.
>
> 💡 Todos arrancan desde tu carpeta home. Para volver ahí en cualquier momento, escribí `cd ~` y Enter.

---

## 🥇 Nivel principiante

### Ejercicio 1 — ¿Dónde estoy?
Averiguá en qué carpeta estás parado ahora mismo.

### Ejercicio 2 — Mirar alrededor
Listá todo lo que hay en tu carpeta actual.

### Ejercicio 3 — Mirar con detalle
Listá lo que hay en tu carpeta actual, pero en **formato largo** (con permisos, tamaño y fecha).

### Ejercicio 4 — Ver lo oculto
Listá **todos** los archivos de tu carpeta, incluso los ocultos (los que empiezan con un punto).

### Ejercicio 5 — Construir el Centro Pokémon
Creá una carpeta llamada `pokecenter` dentro de tu home (`~`).

---

## 🥈 Nivel intermedio

### Ejercicio 6 — Entrar al Centro
Navegá **dentro** de la carpeta `pokecenter` que acabás de crear. Después confirmá con un comando que efectivamente estás adentro.

### Ejercicio 7 — Tu equipo favorito
Estando dentro de `pokecenter`, creá 3 archivos vacíos con los nombres de tus 3 Pokémon favoritos. Por ejemplo: `pikachu.txt`, `charizard.txt`, `gengar.txt`.

### Ejercicio 8 — Pasar lista
Listá el contenido de `pokecenter` para confirmar que tus 3 archivos están ahí.

### Ejercicio 9 — Escribir en la Pokédex
Escribí dentro del archivo de tu Pokémon favorito su tipo. Por ejemplo, que `pikachu.txt` contenga el texto `Tipo: Electrico`.

### Ejercicio 10 — Leer la Pokédex
Mostrá en pantalla el contenido del archivo que acabás de escribir.

---

## 🥉 Nivel avanzado

### Ejercicio 11 — Sala de curación
Dentro de `pokecenter`, creá una subcarpeta llamada `sala-de-curacion`. Luego, en **un solo comando**, creá la ruta anidada `pokecenter/gimnasio/sala-de-batalla` (pista: necesitás un flag de `mkdir`).

### Ejercicio 12 — Mudanza
Mové uno de tus archivos de Pokémon (por ejemplo `pikachu.txt`) dentro de la carpeta `sala-de-curacion`.

### Ejercicio 13 — Evolución
Renombrá uno de tus archivos para simular una evolución. Por ejemplo, convertí `pikachu.txt` en `raichu.txt`.

### Ejercicio 14 — Backup del Centro
Hacé una copia completa de toda la carpeta `pokecenter` con el nombre `pokecenter-backup` (pista: copiar una carpeta entera necesita un flag).

### Ejercicio 15 — Limpieza final
Borrá el archivo que renombraste en el ejercicio 13. Después, volvé a tu home y borrá **toda** la carpeta `pokecenter-backup` con su contenido.

> ⚠️ Recordá: en Linux **no hay papelera**. Cuando borres, asegurate de que es lo que querés borrar. ¡Acá estás practicando, así que no pasa nada, pero agarrá el hábito de mirar dos veces!

---

## 🏆 Desafío extra (opcional)

Sin mirar la solución, armá esta estructura completa desde cero usando los comandos que aprendiste:

```
~/region-kanto/
├── pueblo-paleta/
│   ├── casa-ash.txt
│   └── laboratorio-oak.txt
├── ciudad-verde/
│   └── gimnasio.txt
└── bosque-verde/
    └── pokemon-salvajes.txt
```

Cuando termines, verificá la estructura con `ls -R ~/region-kanto` (el flag `-R` lista recursivamente todo el árbol).
