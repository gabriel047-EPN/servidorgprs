from flask import Flask, render_template

app = Flask(__name__)

# ============================================================
# CONSTANTES ITU-T G.694.1
# ============================================================
C = 2.99792458e8      # Velocidad de la luz en el vacío (m/s)
F_REF = 193.1         # Frecuencia de referencia ITU (THz)
DELTA_F = 0.0125      # Granularidad base (THz = 12.5 GHz)

# Rango ilustrativo (bandas C + L)
F_MIN = 184.5000
F_MAX = 195.9375


# ============================================================
# FUNCIONES
# ============================================================
def frecuencia_a_lambda_nm(f_thz):
    """
    Convierte frecuencia (THz) a longitud de onda aproximada (nm)
    """
    return (C / (f_thz * 1e12)) * 1e9


def generar_tablas_dwmd():
    """
    Genera tablas DWDM separadas por espaciamiento de canal
    según la recomendación ITU-T G.694.1.
    
    Todas las rejillas (25, 50 y 100 GHz) se derivan
    del grid base de 12.5 GHz.
    """

    tablas = {
        "12.5 GHz": [],
        "25 GHz": [],
        "50 GHz": [],
        "100 GHz": []
    }

    # Cálculo del rango de índices n
    n_min = int(round((F_MIN - F_REF) / DELTA_F))
    n_max = int(round((F_MAX - F_REF) / DELTA_F))

    for n in range(n_min, n_max + 1):

        # Frecuencia central nominal
        f = round(F_REF + n * DELTA_F, 4)

        # Longitud de onda aproximada
        lambda_nm = round(frecuencia_a_lambda_nm(f), 4)

        # Grid base: 12.5 GHz (todos los canales)
        tablas["12.5 GHz"].append((n, f, lambda_nm))

        # Subconjuntos derivados
        if n % 2 == 0:   # 25 GHz
            tablas["25 GHz"].append((n, f, lambda_nm))

        if n % 4 == 0:   # 50 GHz
            tablas["50 GHz"].append((n, f, lambda_nm))

        if n % 8 == 0:   # 100 GHz
            tablas["100 GHz"].append((n, f, lambda_nm))

    return tablas


# ============================================================
# RUTA WEB PRINCIPAL
# ============================================================
@app.route("/")
def index():
    tablas = generar_tablas_dwmd()
    return render_template("index.html", tablas=tablas)


# ============================================================
# MAIN (Render ignora este bloque, pero es útil localmente)
# ============================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

