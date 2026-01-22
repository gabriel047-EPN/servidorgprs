from flask import Flask, render_template
import math

app = Flask(__name__)

# ==============================
# CONSTANTES DEL SISTEMA DWDM
# ==============================

# Velocidad de la luz en el vacío (m/s) según ITU-T
C = 2.99792458e8

# Frecuencia de referencia ITU-T (THz)
F_REF = 193.1

# Espaciamientos de canal en THz
SPACINGS = {
    "12.5 GHz": 0.0125,
    "25 GHz": 0.025,
    "50 GHz": 0.05,
    "100 GHz": 0.1
}

# Rango de índices n (canales alrededor de la frecuencia central)
N_RANGE = range(-8, 9)


# ==============================
# FUNCIONES DE CÁLCULO
# ==============================

def frecuencia_a_longitud_onda(freq_thz):
    """
    Convierte frecuencia (THz) a longitud de onda (nm)
    """
    freq_hz = freq_thz * 1e12
    lambda_m = C / freq_hz
    return lambda_m * 1e9


def generar_tablas_dwdm():
    """
    Genera las tablas DWDM para diferentes granularidades
    definidas por la recomendación ITU-T G.694.1
    """
    tablas = {}

    for nombre, paso in SPACINGS.items():
        filas = []
        for n in N_RANGE:
            freq = F_REF + n * paso
            lambda_nm = frecuencia_a_longitud_onda(freq)
            filas.append({
                "n": n,
                "frecuencia": round(freq, 4),
                "longitud_onda": round(lambda_nm, 4)
            })
        tablas[nombre] = filas

    return tablas


# ==============================
# RUTA PRINCIPAL
# ==============================

@app.route("/")
def index():
    tablas = generar_tablas_dwdm()
    return render_template("index.html", tablas=tablas)


# ==============================
# EJECUCIÓN
# ==============================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
