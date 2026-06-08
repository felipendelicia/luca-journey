"""✅ Soluciones — SQL: actualizar y borrar"""
import sqlite3


def cambiar_nivel(conexion, nombre, nuevo_nivel):
    conexion.execute("UPDATE pokemon SET nivel = ? WHERE nombre = ?", (nuevo_nivel, nombre))


def subir_todos(conexion, cuanto):
    conexion.execute("UPDATE pokemon SET nivel = nivel + ?", (cuanto,))


def borrar(conexion, nombre):
    conexion.execute("DELETE FROM pokemon WHERE nombre = ?", (nombre,))


def borrar_debiles(conexion, umbral):
    conexion.execute("DELETE FROM pokemon WHERE nivel < ?", (umbral,))


def bajar_todos(conexion, cuanto):
    conexion.execute("UPDATE pokemon SET nivel = nivel - ?", (cuanto,))
    conexion.commit()


def cambiar_tipo(conexion, nombre, nuevo):
    conexion.execute("UPDATE pokemon SET tipo = ? WHERE nombre = ?", (nuevo, nombre))
    conexion.commit()


def duplicar_niveles(conexion):
    conexion.execute("UPDATE pokemon SET nivel = nivel * 2")
    conexion.commit()


def poner_nivel_minimo(conexion, minimo):
    conexion.execute("UPDATE pokemon SET nivel = ? WHERE nivel < ?", (minimo, minimo))
    conexion.commit()


def borrar_de_tipo(conexion, tipo):
    conexion.execute("DELETE FROM pokemon WHERE tipo = ?", (tipo,))
    conexion.commit()


def borrar_todos(conexion):
    conexion.execute("DELETE FROM pokemon")
    conexion.commit()


def subir_de_tipo(conexion, tipo, cuanto):
    conexion.execute("UPDATE pokemon SET nivel = nivel + ? WHERE tipo = ?", (cuanto, tipo))
    conexion.commit()


def renombrar(conexion, viejo, nuevo):
    conexion.execute("UPDATE pokemon SET nombre = ? WHERE nombre = ?", (nuevo, viejo))
    conexion.commit()


def nivelar(conexion, valor):
    conexion.execute("UPDATE pokemon SET nivel = ?", (valor,))
    conexion.commit()


def borrar_fuertes(conexion, umbral):
    conexion.execute("DELETE FROM pokemon WHERE nivel > ?", (umbral,))
    conexion.commit()


def limitar_nivel(conexion, maximo):
    conexion.execute("UPDATE pokemon SET nivel = ? WHERE nivel > ?", (maximo, maximo))
    conexion.commit()


def incrementar(conexion, nombre, cuanto):
    conexion.execute("UPDATE pokemon SET nivel = nivel + ? WHERE nombre = ?", (cuanto, nombre))
    conexion.commit()


def cambiar_nivel_de_tipo(conexion, tipo, valor):
    conexion.execute("UPDATE pokemon SET nivel = ? WHERE tipo = ?", (valor, tipo))
    conexion.commit()


def sumar_a_los_debiles(conexion, umbral, cuanto):
    conexion.execute("UPDATE pokemon SET nivel = nivel + ? WHERE nivel < ?", (cuanto, umbral))
    conexion.commit()


def reset_tipo(conexion, viejo, nuevo):
    conexion.execute("UPDATE pokemon SET tipo = ? WHERE tipo = ?", (nuevo, viejo))
    conexion.commit()


def borrar_y_contar(conexion, tipo):
    cur = conexion.execute("DELETE FROM pokemon WHERE tipo = ?", (tipo,))
    conexion.commit()
    return cur.rowcount
