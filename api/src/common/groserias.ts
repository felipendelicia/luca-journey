// Filtro de groserías para nombres públicos (handles) y UGC (desafíos). Lista CURADA y CONSERVADORA: solo
// términos inequívocamente ofensivos e improbables dentro de palabras/nombres inocentes. A propósito NO
// incluimos cortas ambiguas (puta/puto/pija/verga/rape/paragua…) que generan falsos positivos
// (computadora, Vergara, pijama, rapero, paraguas…). Lo que se escape lo limpia el admin. Match por SUBSTRING
// sobre el texto normalizado (sin acentos/símbolos, repeticiones colapsadas).

const BLOCK = [
  // insultos fuertes / combinados (es) — distintivos
  'hijodeputa', 'hijadeputa', 'conchatumadre', 'conchadetumadre', 'reconchatumadre', 'putamadre',
  'malparido', 'chupapija', 'chupaverga', 'comemela', 'violador', 'violacion', 'negrodemierda',
  // slurs (es/en)
  'maricon', 'sudaca', 'faggot', 'nigger', 'nigga', 'retard', 'tranny', 'chink', 'cunt',
  // sexual explícito / NSFW
  'porno', 'pornhub', 'xxx', 'sexo', 'whore', 'slut', 'pussy', 'blowjob', 'handjob',
  // groserías en inglés (raras en handles inocentes en español)
  'fuck', 'shit', 'bitch', 'asshole', 'bastard',
  // odio / símbolos
  'nazi', 'hitler', 'kkk', 'heil',
];

// normaliza: minúsculas, sin acentos, solo a-z0-9, repeticiones (3+) colapsadas (puuuta → puuta → puta-ish).
export function normaliza(s: string): string {
  return (s || '')
    .toLowerCase()
    .normalize('NFD').replace(/[̀-ͯ]/g, '')
    .replace(/[^a-z0-9]/g, '')
    .replace(/(.)\1{2,}/g, '$1$1');
}

export function contieneGroseria(s: string): boolean {
  const n = normaliza(s);
  if (!n) return false;
  return BLOCK.some((w) => n.includes(w));
}
