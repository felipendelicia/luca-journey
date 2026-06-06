import { Traverse } from 'neotraverse/modern';
import pLimit from 'p-limit';
import { removeBase, prependForwardSlash } from '@astrojs/internal-helpers/path';
import { i as isCoreRemotePath, V as VALID_INPUT_FORMATS } from './astro/assets-service_lzFWa4op.mjs';
import { A as AstroError, U as UnknownContentCollectionError, c as createComponent, e as renderUniqueStylesheet, f as renderScriptElement, g as createHeadAndContent, r as renderComponent, a as renderTemplate, u as unescapeHTML } from './astro/server_Cc6JC6ec.mjs';
import 'kleur/colors';
import * as devalue from 'devalue';

const CONTENT_IMAGE_FLAG = "astroContentImageFlag";
const IMAGE_IMPORT_PREFIX = "__ASTRO_IMAGE_";

function imageSrcToImportId(imageSrc, filePath) {
  imageSrc = removeBase(imageSrc, IMAGE_IMPORT_PREFIX);
  if (isCoreRemotePath(imageSrc)) {
    return;
  }
  const ext = imageSrc.split(".").at(-1);
  if (!ext || !VALID_INPUT_FORMATS.includes(ext)) {
    return;
  }
  const params = new URLSearchParams(CONTENT_IMAGE_FLAG);
  if (filePath) {
    params.set("importer", filePath);
  }
  return `${imageSrc}?${params.toString()}`;
}

class DataStore {
  _collections = /* @__PURE__ */ new Map();
  constructor() {
    this._collections = /* @__PURE__ */ new Map();
  }
  get(collectionName, key) {
    return this._collections.get(collectionName)?.get(String(key));
  }
  entries(collectionName) {
    const collection = this._collections.get(collectionName) ?? /* @__PURE__ */ new Map();
    return [...collection.entries()];
  }
  values(collectionName) {
    const collection = this._collections.get(collectionName) ?? /* @__PURE__ */ new Map();
    return [...collection.values()];
  }
  keys(collectionName) {
    const collection = this._collections.get(collectionName) ?? /* @__PURE__ */ new Map();
    return [...collection.keys()];
  }
  has(collectionName, key) {
    const collection = this._collections.get(collectionName);
    if (collection) {
      return collection.has(String(key));
    }
    return false;
  }
  hasCollection(collectionName) {
    return this._collections.has(collectionName);
  }
  collections() {
    return this._collections;
  }
  /**
   * Attempts to load a DataStore from the virtual module.
   * This only works in Vite.
   */
  static async fromModule() {
    try {
      const data = await import('./_astro_data-layer-content_BcEe_9wP.mjs');
      if (data.default instanceof Map) {
        return DataStore.fromMap(data.default);
      }
      const map = devalue.unflatten(data.default);
      return DataStore.fromMap(map);
    } catch {
    }
    return new DataStore();
  }
  static async fromMap(data) {
    const store = new DataStore();
    store._collections = data;
    return store;
  }
}
function dataStoreSingleton() {
  let instance = void 0;
  return {
    get: async () => {
      if (!instance) {
        instance = DataStore.fromModule();
      }
      return instance;
    },
    set: (store) => {
      instance = store;
    }
  };
}
const globalDataStore = dataStoreSingleton();

const __vite_import_meta_env__ = {"ASSETS_PREFIX": undefined, "BASE_URL": "/luca-journey", "DEV": false, "MODE": "production", "PROD": true, "PUBLIC_API_URL": "https://poke.servegame.com", "SITE": "https://felipendelicia.github.io", "SSR": true};
function createCollectionToGlobResultMap({
  globResult,
  contentDir
}) {
  const collectionToGlobResultMap = {};
  for (const key in globResult) {
    const keyRelativeToContentDir = key.replace(new RegExp(`^${contentDir}`), "");
    const segments = keyRelativeToContentDir.split("/");
    if (segments.length <= 1) continue;
    const collection = segments[0];
    collectionToGlobResultMap[collection] ??= {};
    collectionToGlobResultMap[collection][key] = globResult[key];
  }
  return collectionToGlobResultMap;
}
function createGetCollection({
  contentCollectionToEntryMap,
  dataCollectionToEntryMap,
  getRenderEntryImport,
  cacheEntriesByCollection
}) {
  return async function getCollection(collection, filter) {
    const hasFilter = typeof filter === "function";
    const store = await globalDataStore.get();
    let type;
    if (collection in contentCollectionToEntryMap) {
      type = "content";
    } else if (collection in dataCollectionToEntryMap) {
      type = "data";
    } else if (store.hasCollection(collection)) {
      const { default: imageAssetMap } = await import('./_astro_asset-imports_D9aVaOQr.mjs');
      const result = [];
      for (const rawEntry of store.values(collection)) {
        const data = updateImageReferencesInData(rawEntry.data, rawEntry.filePath, imageAssetMap);
        const entry = {
          ...rawEntry,
          data,
          collection
        };
        if (hasFilter && !filter(entry)) {
          continue;
        }
        result.push(entry);
      }
      return result;
    } else {
      console.warn(
        `The collection ${JSON.stringify(
          collection
        )} does not exist or is empty. Ensure a collection directory with this name exists.`
      );
      return [];
    }
    const lazyImports = Object.values(
      type === "content" ? contentCollectionToEntryMap[collection] : dataCollectionToEntryMap[collection]
    );
    let entries = [];
    if (!Object.assign(__vite_import_meta_env__, { _: process.env._ })?.DEV && cacheEntriesByCollection.has(collection)) {
      entries = cacheEntriesByCollection.get(collection);
    } else {
      const limit = pLimit(10);
      entries = await Promise.all(
        lazyImports.map(
          (lazyImport) => limit(async () => {
            const entry = await lazyImport();
            return type === "content" ? {
              id: entry.id,
              slug: entry.slug,
              body: entry.body,
              collection: entry.collection,
              data: entry.data,
              async render() {
                return render({
                  collection: entry.collection,
                  id: entry.id,
                  renderEntryImport: await getRenderEntryImport(collection, entry.slug)
                });
              }
            } : {
              id: entry.id,
              collection: entry.collection,
              data: entry.data
            };
          })
        )
      );
      cacheEntriesByCollection.set(collection, entries);
    }
    if (hasFilter) {
      return entries.filter(filter);
    } else {
      return entries.slice();
    }
  };
}
function updateImageReferencesInData(data, fileName, imageAssetMap) {
  return new Traverse(data).map(function(ctx, val) {
    if (typeof val === "string" && val.startsWith(IMAGE_IMPORT_PREFIX)) {
      const src = val.replace(IMAGE_IMPORT_PREFIX, "");
      const id = imageSrcToImportId(src, fileName);
      if (!id) {
        ctx.update(src);
        return;
      }
      const imported = imageAssetMap?.get(id);
      if (imported) {
        ctx.update(imported);
      } else {
        ctx.update(src);
      }
    }
  });
}
async function render({
  collection,
  id,
  renderEntryImport
}) {
  const UnexpectedRenderError = new AstroError({
    ...UnknownContentCollectionError,
    message: `Unexpected error while rendering ${String(collection)} → ${String(id)}.`
  });
  if (typeof renderEntryImport !== "function") throw UnexpectedRenderError;
  const baseMod = await renderEntryImport();
  if (baseMod == null || typeof baseMod !== "object") throw UnexpectedRenderError;
  const { default: defaultMod } = baseMod;
  if (isPropagatedAssetsModule(defaultMod)) {
    const { collectedStyles, collectedLinks, collectedScripts, getMod } = defaultMod;
    if (typeof getMod !== "function") throw UnexpectedRenderError;
    const propagationMod = await getMod();
    if (propagationMod == null || typeof propagationMod !== "object") throw UnexpectedRenderError;
    const Content = createComponent({
      factory(result, baseProps, slots) {
        let styles = "", links = "", scripts = "";
        if (Array.isArray(collectedStyles)) {
          styles = collectedStyles.map((style) => {
            return renderUniqueStylesheet(result, {
              type: "inline",
              content: style
            });
          }).join("");
        }
        if (Array.isArray(collectedLinks)) {
          links = collectedLinks.map((link) => {
            return renderUniqueStylesheet(result, {
              type: "external",
              src: prependForwardSlash(link)
            });
          }).join("");
        }
        if (Array.isArray(collectedScripts)) {
          scripts = collectedScripts.map((script) => renderScriptElement(script)).join("");
        }
        let props = baseProps;
        if (id.endsWith("mdx")) {
          props = {
            components: propagationMod.components ?? {},
            ...baseProps
          };
        }
        return createHeadAndContent(
          unescapeHTML(styles + links + scripts),
          renderTemplate`${renderComponent(
            result,
            "Content",
            propagationMod.Content,
            props,
            slots
          )}`
        );
      },
      propagation: "self"
    });
    return {
      Content,
      headings: propagationMod.getHeadings?.() ?? [],
      remarkPluginFrontmatter: propagationMod.frontmatter ?? {}
    };
  } else if (baseMod.Content && typeof baseMod.Content === "function") {
    return {
      Content: baseMod.Content,
      headings: baseMod.getHeadings?.() ?? [],
      remarkPluginFrontmatter: baseMod.frontmatter ?? {}
    };
  } else {
    throw UnexpectedRenderError;
  }
}
function isPropagatedAssetsModule(module) {
  return typeof module === "object" && module != null && "__astroPropagation" in module;
}

// astro-head-inject

const contentDir = '/src/content/';

const contentEntryGlob = /* #__PURE__ */ Object.assign({"/src/content/libro/analisis-integrador.md": () => import('./analisis-integrador_BQuvmTmi.mjs'),"/src/content/libro/api-http-json.md": () => import('./api-http-json_G9ISzgA0.mjs'),"/src/content/libro/assert-afirmaciones.md": () => import('./assert-afirmaciones_sJcyHL-k.mjs'),"/src/content/libro/ayuda.md": () => import('./ayuda_BfLOWktC.mjs'),"/src/content/libro/cadenas-y-archivos.md": () => import('./cadenas-y-archivos_jF67TdTF.mjs'),"/src/content/libro/casos-limite.md": () => import('./casos-limite_DPRt5nP7.mjs'),"/src/content/libro/consumir-api.md": () => import('./consumir-api_BNlqFyyG.mjs'),"/src/content/libro/control-de-flujo.md": () => import('./control-de-flujo_CItLE4Y1.mjs'),"/src/content/libro/errores-try-except.md": () => import('./errores-try-except_CLXnI0pg.mjs'),"/src/content/libro/excepciones-propias.md": () => import('./excepciones-propias_6s1UujRm.mjs'),"/src/content/libro/flask-json.md": () => import('./flask-json_CS6zSwHa.mjs'),"/src/content/libro/flask-parametros.md": () => import('./flask-parametros_CJinXUKP.mjs'),"/src/content/libro/flask-post.md": () => import('./flask-post_BKLWXU27.mjs'),"/src/content/libro/flask-primera-app.md": () => import('./flask-primera-app_SqeSo_T4.mjs'),"/src/content/libro/flask-rest-crud.md": () => import('./flask-rest-crud_CE3tWE8f.mjs'),"/src/content/libro/funciones.md": () => import('./funciones_Ba7uOXQ8.mjs'),"/src/content/libro/git.md": () => import('./git_BKY3zTCg.mjs'),"/src/content/libro/ia-arboles.md": () => import('./ia-arboles_kXaXnTQh.mjs'),"/src/content/libro/ia-clasificacion.md": () => import('./ia-clasificacion_eYJF8BNj.mjs'),"/src/content/libro/ia-clustering.md": () => import('./ia-clustering_Bd1OarVR.mjs'),"/src/content/libro/ia-datos.md": () => import('./ia-datos_CGh4QINN.mjs'),"/src/content/libro/ia-evaluacion.md": () => import('./ia-evaluacion_Dh2lKT_l.mjs'),"/src/content/libro/ia-intro.md": () => import('./ia-intro_BGgK_IAX.mjs'),"/src/content/libro/ia-proyecto.md": () => import('./ia-proyecto_Cuv0lVnj.mjs'),"/src/content/libro/ia-regresion.md": () => import('./ia-regresion_CFgeqjeJ.mjs'),"/src/content/libro/introduccion.md": () => import('./introduccion_CWIQKN29.mjs'),"/src/content/libro/linux-fundamentos.md": () => import('./linux-fundamentos_DsOsxtNV.mjs'),"/src/content/libro/linux-intermedio.md": () => import('./linux-intermedio_CfeG2vOM.mjs'),"/src/content/libro/listas-y-colecciones.md": () => import('./listas-y-colecciones_C4Ycb6k_.mjs'),"/src/content/libro/matplotlib.md": () => import('./matplotlib_uqgR3mhI.mjs'),"/src/content/libro/modulos-y-pip.md": () => import('./modulos-y-pip_1AAKGoyi.mjs'),"/src/content/libro/numpy-arrays.md": () => import('./numpy-arrays_BEWRw6pZ.mjs'),"/src/content/libro/numpy-calculo.md": () => import('./numpy-calculo_DNSugceB.mjs'),"/src/content/libro/pandas-groupby.md": () => import('./pandas-groupby_DeUWDb1X.mjs'),"/src/content/libro/pandas-limpieza.md": () => import('./pandas-limpieza_DLbcsfAL.mjs'),"/src/content/libro/pandas-seleccion.md": () => import('./pandas-seleccion_BUBi4zqR.mjs'),"/src/content/libro/pandas-series-dataframe.md": () => import('./pandas-series-dataframe_Cuel8inC.mjs'),"/src/content/libro/pokedex-api.md": () => import('./pokedex-api_BFcIiTZI.mjs'),"/src/content/libro/poo-avanzado.md": () => import('./poo-avanzado_BgF-n28u.mjs'),"/src/content/libro/poo-introduccion.md": () => import('./poo-introduccion_D1d5P0m0.mjs'),"/src/content/libro/primer-test.md": () => import('./primer-test_C9c65M0w.mjs'),"/src/content/libro/proyecto-db.md": () => import('./proyecto-db_C2DBVW5S.mjs'),"/src/content/libro/proyecto-testing.md": () => import('./proyecto-testing_CdF57aZQ.mjs'),"/src/content/libro/python-introduccion.md": () => import('./python-introduccion_BVPONJqw.mjs'),"/src/content/libro/raise-validar.md": () => import('./raise-validar_BSdklL3C.mjs'),"/src/content/libro/sql-agregaciones.md": () => import('./sql-agregaciones_D1YabatH.mjs'),"/src/content/libro/sql-crear.md": () => import('./sql-crear_BLRfzAxZ.mjs'),"/src/content/libro/sql-intro.md": () => import('./sql-intro_BmLc8Sq5.mjs'),"/src/content/libro/sql-join.md": () => import('./sql-join_aPDOIiaT.mjs'),"/src/content/libro/sql-select.md": () => import('./sql-select_BjjWGnil.mjs'),"/src/content/libro/sql-update-delete.md": () => import('./sql-update-delete_BZ1ZDOmA.mjs'),"/src/content/libro/sqlite-python.md": () => import('./sqlite-python_C4rRD-yZ.mjs'),"/src/content/libro/tdd.md": () => import('./tdd_D4DX-h_n.mjs')});
const contentCollectionToEntryMap = createCollectionToGlobResultMap({
	globResult: contentEntryGlob,
	contentDir,
});

const dataEntryGlob = /* #__PURE__ */ Object.assign({});
const dataCollectionToEntryMap = createCollectionToGlobResultMap({
	globResult: dataEntryGlob,
	contentDir,
});
createCollectionToGlobResultMap({
	globResult: { ...contentEntryGlob, ...dataEntryGlob },
	contentDir,
});

let lookupMap = {};
lookupMap = {"libro":{"type":"content","entries":{"api-http-json":"/src/content/libro/api-http-json.md","analisis-integrador":"/src/content/libro/analisis-integrador.md","ayuda":"/src/content/libro/ayuda.md","assert-afirmaciones":"/src/content/libro/assert-afirmaciones.md","cadenas-y-archivos":"/src/content/libro/cadenas-y-archivos.md","casos-limite":"/src/content/libro/casos-limite.md","consumir-api":"/src/content/libro/consumir-api.md","control-de-flujo":"/src/content/libro/control-de-flujo.md","errores-try-except":"/src/content/libro/errores-try-except.md","excepciones-propias":"/src/content/libro/excepciones-propias.md","flask-json":"/src/content/libro/flask-json.md","flask-parametros":"/src/content/libro/flask-parametros.md","flask-post":"/src/content/libro/flask-post.md","flask-primera-app":"/src/content/libro/flask-primera-app.md","flask-rest-crud":"/src/content/libro/flask-rest-crud.md","funciones":"/src/content/libro/funciones.md","git":"/src/content/libro/git.md","ia-arboles":"/src/content/libro/ia-arboles.md","ia-clasificacion":"/src/content/libro/ia-clasificacion.md","ia-clustering":"/src/content/libro/ia-clustering.md","ia-datos":"/src/content/libro/ia-datos.md","ia-evaluacion":"/src/content/libro/ia-evaluacion.md","ia-intro":"/src/content/libro/ia-intro.md","ia-proyecto":"/src/content/libro/ia-proyecto.md","ia-regresion":"/src/content/libro/ia-regresion.md","introduccion":"/src/content/libro/introduccion.md","linux-fundamentos":"/src/content/libro/linux-fundamentos.md","linux-intermedio":"/src/content/libro/linux-intermedio.md","listas-y-colecciones":"/src/content/libro/listas-y-colecciones.md","matplotlib":"/src/content/libro/matplotlib.md","modulos-y-pip":"/src/content/libro/modulos-y-pip.md","numpy-arrays":"/src/content/libro/numpy-arrays.md","numpy-calculo":"/src/content/libro/numpy-calculo.md","pandas-groupby":"/src/content/libro/pandas-groupby.md","pandas-limpieza":"/src/content/libro/pandas-limpieza.md","pandas-seleccion":"/src/content/libro/pandas-seleccion.md","pandas-series-dataframe":"/src/content/libro/pandas-series-dataframe.md","pokedex-api":"/src/content/libro/pokedex-api.md","poo-introduccion":"/src/content/libro/poo-introduccion.md","poo-avanzado":"/src/content/libro/poo-avanzado.md","primer-test":"/src/content/libro/primer-test.md","proyecto-db":"/src/content/libro/proyecto-db.md","proyecto-testing":"/src/content/libro/proyecto-testing.md","python-introduccion":"/src/content/libro/python-introduccion.md","raise-validar":"/src/content/libro/raise-validar.md","sql-agregaciones":"/src/content/libro/sql-agregaciones.md","sql-crear":"/src/content/libro/sql-crear.md","sql-intro":"/src/content/libro/sql-intro.md","sql-join":"/src/content/libro/sql-join.md","sql-select":"/src/content/libro/sql-select.md","sql-update-delete":"/src/content/libro/sql-update-delete.md","tdd":"/src/content/libro/tdd.md","sqlite-python":"/src/content/libro/sqlite-python.md"}}};

new Set(Object.keys(lookupMap));

function createGlobLookup(glob) {
	return async (collection, lookupId) => {
		const filePath = lookupMap[collection]?.entries[lookupId];

		if (!filePath) return undefined;
		return glob[collection][filePath];
	};
}

const renderEntryGlob = /* #__PURE__ */ Object.assign({"/src/content/libro/analisis-integrador.md": () => import('./analisis-integrador_C3HZGrWq.mjs'),"/src/content/libro/api-http-json.md": () => import('./api-http-json_NJ26h9J1.mjs'),"/src/content/libro/assert-afirmaciones.md": () => import('./assert-afirmaciones_bOaNiqUo.mjs'),"/src/content/libro/ayuda.md": () => import('./ayuda_Bjm2edsy.mjs'),"/src/content/libro/cadenas-y-archivos.md": () => import('./cadenas-y-archivos_CbsTs0xW.mjs'),"/src/content/libro/casos-limite.md": () => import('./casos-limite_BFLw8AGf.mjs'),"/src/content/libro/consumir-api.md": () => import('./consumir-api_B2f1O8k5.mjs'),"/src/content/libro/control-de-flujo.md": () => import('./control-de-flujo_DsrbFQbM.mjs'),"/src/content/libro/errores-try-except.md": () => import('./errores-try-except_e0rtruOm.mjs'),"/src/content/libro/excepciones-propias.md": () => import('./excepciones-propias_BYXWIZfr.mjs'),"/src/content/libro/flask-json.md": () => import('./flask-json_DxK8mspp.mjs'),"/src/content/libro/flask-parametros.md": () => import('./flask-parametros_EJJN3B-9.mjs'),"/src/content/libro/flask-post.md": () => import('./flask-post_D5uJ_zQh.mjs'),"/src/content/libro/flask-primera-app.md": () => import('./flask-primera-app_xH6wGfh6.mjs'),"/src/content/libro/flask-rest-crud.md": () => import('./flask-rest-crud_M60-Ak8Z.mjs'),"/src/content/libro/funciones.md": () => import('./funciones_Cw1IkbkY.mjs'),"/src/content/libro/git.md": () => import('./git_D-Sdh9rZ.mjs'),"/src/content/libro/ia-arboles.md": () => import('./ia-arboles_rDklNLpi.mjs'),"/src/content/libro/ia-clasificacion.md": () => import('./ia-clasificacion_piECFHGi.mjs'),"/src/content/libro/ia-clustering.md": () => import('./ia-clustering_vYBIPhjr.mjs'),"/src/content/libro/ia-datos.md": () => import('./ia-datos_Cffav5LL.mjs'),"/src/content/libro/ia-evaluacion.md": () => import('./ia-evaluacion_BPs0AIfZ.mjs'),"/src/content/libro/ia-intro.md": () => import('./ia-intro_A-RQ7BYZ.mjs'),"/src/content/libro/ia-proyecto.md": () => import('./ia-proyecto_Costg1JJ.mjs'),"/src/content/libro/ia-regresion.md": () => import('./ia-regresion_DXKbcqTT.mjs'),"/src/content/libro/introduccion.md": () => import('./introduccion_DZyHS1ru.mjs'),"/src/content/libro/linux-fundamentos.md": () => import('./linux-fundamentos_B_QItPLS.mjs'),"/src/content/libro/linux-intermedio.md": () => import('./linux-intermedio_C3-K3az6.mjs'),"/src/content/libro/listas-y-colecciones.md": () => import('./listas-y-colecciones_CxWM-o8_.mjs'),"/src/content/libro/matplotlib.md": () => import('./matplotlib_CT9HZDMA.mjs'),"/src/content/libro/modulos-y-pip.md": () => import('./modulos-y-pip_DU_WxgBB.mjs'),"/src/content/libro/numpy-arrays.md": () => import('./numpy-arrays_DAY4R9A3.mjs'),"/src/content/libro/numpy-calculo.md": () => import('./numpy-calculo_D_7Uw_VU.mjs'),"/src/content/libro/pandas-groupby.md": () => import('./pandas-groupby_QdkY7yLo.mjs'),"/src/content/libro/pandas-limpieza.md": () => import('./pandas-limpieza_D8XdtAFz.mjs'),"/src/content/libro/pandas-seleccion.md": () => import('./pandas-seleccion_BtbKgqck.mjs'),"/src/content/libro/pandas-series-dataframe.md": () => import('./pandas-series-dataframe_DvIlx3sP.mjs'),"/src/content/libro/pokedex-api.md": () => import('./pokedex-api_zwckEzZb.mjs'),"/src/content/libro/poo-avanzado.md": () => import('./poo-avanzado_BuOFQ33o.mjs'),"/src/content/libro/poo-introduccion.md": () => import('./poo-introduccion_CftcHrHO.mjs'),"/src/content/libro/primer-test.md": () => import('./primer-test_BJTGfLvz.mjs'),"/src/content/libro/proyecto-db.md": () => import('./proyecto-db_BpK45qX5.mjs'),"/src/content/libro/proyecto-testing.md": () => import('./proyecto-testing_D5jTWnFq.mjs'),"/src/content/libro/python-introduccion.md": () => import('./python-introduccion_CoKBgKZw.mjs'),"/src/content/libro/raise-validar.md": () => import('./raise-validar_B8WVQIZY.mjs'),"/src/content/libro/sql-agregaciones.md": () => import('./sql-agregaciones_KXYeeMEX.mjs'),"/src/content/libro/sql-crear.md": () => import('./sql-crear_qtX31zLt.mjs'),"/src/content/libro/sql-intro.md": () => import('./sql-intro_CSWL6Rvp.mjs'),"/src/content/libro/sql-join.md": () => import('./sql-join_BpeCz1Z7.mjs'),"/src/content/libro/sql-select.md": () => import('./sql-select_BLShN08I.mjs'),"/src/content/libro/sql-update-delete.md": () => import('./sql-update-delete_ConlQHKp.mjs'),"/src/content/libro/sqlite-python.md": () => import('./sqlite-python_D7nO760b.mjs'),"/src/content/libro/tdd.md": () => import('./tdd_CUq_8-G9.mjs')});
const collectionToRenderEntryMap = createCollectionToGlobResultMap({
	globResult: renderEntryGlob,
	contentDir,
});

const cacheEntriesByCollection = new Map();
const getCollection = createGetCollection({
	contentCollectionToEntryMap,
	dataCollectionToEntryMap,
	getRenderEntryImport: createGlobLookup(collectionToRenderEntryMap),
	cacheEntriesByCollection,
});

// Agrupa los capítulos del libro en secciones desplegables.
const GRUPOS = [
  { nombre: 'Introducción', icono: '🎒', slugs: ['introduccion'] },
  { nombre: 'Linux', icono: '🐧', slugs: ['linux-fundamentos', 'linux-intermedio'] },
  {
    nombre: 'Fundamentos',
    icono: '🐍',
    slugs: [
      'python-introduccion', 'control-de-flujo', 'funciones',
      'listas-y-colecciones', 'cadenas-y-archivos',
      'poo-introduccion', 'poo-avanzado', 'modulos-y-pip',
    ],
  },
  {
    nombre: 'Análisis de datos',
    icono: '📊',
    slugs: [
      'numpy-arrays', 'numpy-calculo', 'pandas-series-dataframe', 'pandas-seleccion',
      'pandas-limpieza', 'pandas-groupby', 'matplotlib', 'analisis-integrador',
    ],
  },
  {
    nombre: 'APIs',
    icono: '🛰️',
    slugs: [
      'api-http-json', 'flask-primera-app', 'flask-json', 'flask-parametros',
      'flask-post', 'flask-rest-crud', 'consumir-api', 'pokedex-api',
    ],
  },
  {
    nombre: 'Bases de datos',
    icono: '🗄️',
    slugs: [
      'sql-intro', 'sql-crear', 'sql-select', 'sql-agregaciones',
      'sql-update-delete', 'sql-join', 'sqlite-python', 'proyecto-db',
    ],
  },
  {
    nombre: 'Inteligencia Artificial',
    icono: '🤖',
    slugs: [
      'ia-intro', 'ia-datos', 'ia-clasificacion', 'ia-evaluacion',
      'ia-regresion', 'ia-arboles', 'ia-clustering', 'ia-proyecto',
    ],
  },
  {
    nombre: 'Testing y calidad',
    icono: '🧪',
    slugs: [
      'errores-try-except', 'raise-validar', 'excepciones-propias', 'assert-afirmaciones',
      'primer-test', 'casos-limite', 'tdd', 'proyecto-testing',
    ],
  },
  { nombre: 'Git', icono: '🔀', slugs: ['git'] },
  { nombre: 'Ayuda', icono: '❓', slugs: ['ayuda'] },
];

// caps: array YA ordenado por 'order'. Devuelve grupos con sus capítulos + nº global.
function agrupar(caps) {
  const pos = new Map(caps.map((c, i) => [c.slug, i]));
  return GRUPOS
    .map((g) => ({
      nombre: g.nombre,
      icono: g.icono,
      items: g.slugs.filter((s) => pos.has(s)).map((s) => ({ cap: caps[pos.get(s)], n: pos.get(s) })),
    }))
    .filter((g) => g.items.length);
}

export { agrupar as a, getCollection as g };
