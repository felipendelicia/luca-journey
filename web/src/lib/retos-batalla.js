// retos-batalla.js — pool de micro-retos (opción múltiple) para el SÚPER de la batalla.
// Cada reto tiene 'region': solo se preguntan temas de regiones DESBLOQUEADAS (que el jugador vio).
// q = pregunta, op = opciones, c = índice de la correcta.
export const RETOS = [
  // ── Kanto: fundamentos de Python ──
  { region: 'kanto', q: '¿Qué imprime print(2 + 3)?', op: ['23', '5', 'Error'], c: 1 },
  { region: 'kanto', q: '¿Cuánto da len([1, 2, 3])?', op: ['2', '3', '6'], c: 1 },
  { region: 'kanto', q: '¿Qué da "ab" + "cd"?', op: ['abcd', 'ab cd', 'Error'], c: 0 },
  { region: 'kanto', q: '¿Cuánto da 10 // 3?', op: ['3', '3.33', '1'], c: 0 },
  { region: 'kanto', q: '¿Qué da bool(0)?', op: ['True', 'False', '0'], c: 1 },
  { region: 'kanto', q: '¿Qué da [1, 2, 3][0]?', op: ['1', '2', '3'], c: 0 },
  { region: 'kanto', q: '¿Qué da "hola".upper()?', op: ['hola', 'HOLA', 'Hola'], c: 1 },
  { region: 'kanto', q: '¿Cuánto da 2 ** 3?', op: ['6', '8', '9'], c: 1 },
  { region: 'kanto', q: '¿Cuántas vueltas da for i in range(3)?', op: ['2', '3', '4'], c: 1 },
  { region: 'kanto', q: '¿Qué da 7 % 2?', op: ['0', '1', '3'], c: 1 },
  // ── Johto: numpy / pandas ──
  { region: 'johto', q: '¿Cuánto da np.array([1, 2, 3]).sum()?', op: ['6', '3', '[1 2 3]'], c: 0 },
  { region: 'johto', q: '¿Qué da np.arange(3)?', op: ['[1 2 3]', '[0 1 2]', '[0 1 2 3]'], c: 1 },
  { region: 'johto', q: '¿Qué muestra df.head()?', op: ['las últimas filas', 'las primeras filas', 'las columnas'], c: 1 },
  { region: 'johto', q: '¿Qué hace df["col"]?', op: ['borra la columna', 'selecciona la columna', 'la ordena'], c: 1 },
  // ── Hoenn: Flask / APIs ──
  { region: 'hoenn', q: 'En Flask, @app.route("/") define…', op: ['una ruta', 'una variable', 'un test'], c: 0 },
  { region: 'hoenn', q: '¿Qué hace jsonify(d)?', op: ['borra d', 'devuelve d como JSON', 'imprime d'], c: 1 },
  { region: 'hoenn', q: "methods=['POST'] hace que la ruta…", op: ['acepte POST', 'sea privada', 'devuelva HTML'], c: 0 },
  // ── Sinnoh: SQL ──
  { region: 'sinnoh', q: 'SELECT * FROM pokemon trae…', op: ['solo 1 fila', 'todas las columnas', 'nada'], c: 1 },
  { region: 'sinnoh', q: '¿Qué hace WHERE en una consulta?', op: ['filtra filas', 'ordena', 'borra la tabla'], c: 0 },
  { region: 'sinnoh', q: '¿Qué devuelve COUNT(*)?', op: ['la primera fila', 'la cantidad de filas', 'las columnas'], c: 1 },
  // ── Unova: Machine Learning ──
  { region: 'unova', q: '¿Qué hace train_test_split?', op: ['entrena el modelo', 'separa datos en train/test', 'grafica'], c: 1 },
  { region: 'unova', q: '¿Qué hace model.fit(X, y)?', op: ['predice', 'entrena el modelo', 'borra datos'], c: 1 },
  { region: 'unova', q: '¿Qué devuelve model.predict(X)?', op: ['predicciones', 'el error', 'los datos'], c: 0 },
  // ── Kalos: testing ──
  { region: 'kalos', q: '¿Qué pasa con assert 1 == 1?', op: ['falla', 'pasa (no hace nada)', 'imprime 1'], c: 1 },
  { region: 'kalos', q: 'En pytest, las funciones de test empiezan con…', op: ['def_', 'test_', 'check_'], c: 1 },
  { region: 'kalos', q: '¿Qué hace assert x == 5 si x vale 3?', op: ['pasa', 'lanza AssertionError', 'pone x en 5'], c: 1 },
  // ── Alola: automatizaciones ──
  { region: 'alola', q: 'En un script, ¿qué es sys.argv[0]?', op: ['el primer argumento', 'el nombre del script', 'la cantidad de argumentos'], c: 1 },
  { region: 'alola', q: '¿Con qué armás una ruta sin pelear con las barras?', op: ['pathlib.Path', 'string + "/"', 'os.system'], c: 0 },
  { region: 'alola', q: 'En subprocess, ¿qué returncode significa éxito?', op: ['1', '0', '-1'], c: 1 },
  { region: 'alola', q: '¿De dónde lee una automatización las contraseñas?', op: ['del código', 'del entorno / config', 'de un print'], c: 1 },
  // ── Galar: asincronía y concurrencia ──
  { region: 'galar', q: '¿Cómo se define una función asíncrona?', op: ['def f()', 'async def f()', 'await def f()'], c: 1 },
  { region: 'galar', q: '¿Dónde se puede usar await?', op: ['en cualquier función', 'dentro de async def', 'solo al final del archivo'], c: 1 },
  { region: 'galar', q: 'asyncio.gather(a, b) corre las tareas…', op: ['de a una', 'en paralelo', 'al revés'], c: 1 },
  { region: 'galar', q: 'Una cola FIFO saca primero…', op: ['al último que entró', 'al que entró primero', 'al azar'], c: 1 },
  // ── Paldea: algoritmos y estructuras de datos ──
  { region: 'paldea', q: 'La búsqueda binaria necesita la lista…', op: ['vacía', 'ordenada', 'con repetidos'], c: 1 },
  { region: 'paldea', q: 'Una pila (stack) es…', op: ['FIFO', 'LIFO', 'ordenada'], c: 1 },
  { region: 'paldea', q: 'Buscar x in un set es…', op: ['lento, O(n)', 'casi instantáneo, O(1)', 'imposible'], c: 1 },
  { region: 'paldea', q: 'factorial(0) debe devolver…', op: ['0', '1', 'error'], c: 1 },
];

// reto al azar de las regiones desbloqueadas (Set de strings). Fallback: kanto.
export function retoAlAzar(regionesSet) {
  const pool = RETOS.filter((r) => regionesSet.has(r.region));
  const base = pool.length ? pool : RETOS.filter((r) => r.region === 'kanto');
  return base[Math.floor(Math.random() * base.length)];
}
