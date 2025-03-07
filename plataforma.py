# -*- coding: utf-8 -*-
"""Plataforma.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1sklkTfPE0ANikkluXJV3RyrDi095jrn4
"""

import streamlit as st
import pandas as pd

# Datos iniciales (en memoria - podrías guardarlos en un CSV/SQLite para persistencia)
if 'catalogo_cuentas' not in st.session_state:
    st.session_state['catalogo_cuentas'] = pd.DataFrame(columns=['Código', 'Nombre', 'Tipo'])

if 'polizas' not in st.session_state:
    st.session_state['polizas'] = pd.DataFrame(columns=['Folio', 'Fecha', 'Concepto', 'Cuenta', 'Debe', 'Haber'])

if 'configuracion' not in st.session_state:
    st.session_state['configuracion'] = {
        "Empresa": "Mi Empresa S.A. de C.V.",
        "RFC": "XAXX010101000"
    }

# Menú lateral
menu = st.sidebar.selectbox("Menú", [
    "Inicio",
    "Catálogo de Cuentas",
    "Módulo de Pólizas",
    "Consultas (Auxiliares y Balanzas)",
    "Configuración"
])

# Función para mostrar balances (balanza de comprobación)
def mostrar_balanza():
    if st.session_state['polizas'].empty:
        st.warning("No hay movimientos registrados.")
        return
    balanza = st.session_state['polizas'].groupby('Cuenta').agg({'Debe': 'sum', 'Haber': 'sum'}).reset_index()
    st.dataframe(balanza)

# Inicio
if menu == "Inicio":
    st.title("Sistema Contable de Información Financiera")
    st.write("Bienvenido al Sistema Contable para la materia de Sistemas Contables de Información Financiera.")

    # Mostrar imagen al inicio (ajusta la ruta o URL de la imagen)
    st.image("UNRC.png", caption="Universidad Nacional Rosario Castellanos", width=350)

# Catálogo de cuentas
elif menu == "Catálogo de Cuentas":
    st.title("Catálogo de Cuentas")

    with st.form("Alta de Cuenta"):
        codigo = st.text_input("Código")
        nombre = st.text_input("Nombre")
        tipo = st.selectbox("Tipo", ["Activo", "Pasivo", "Capital", "Ingresos", "Gastos"])
        submit = st.form_submit_button("Agregar Cuenta")

        if submit:
            nueva_cuenta = pd.DataFrame([[codigo, nombre, tipo]], columns=['Código', 'Nombre', 'Tipo'])
            st.session_state['catalogo_cuentas'] = pd.concat([st.session_state['catalogo_cuentas'], nueva_cuenta], ignore_index=True)
            st.success("Cuenta agregada correctamente")

    st.write("### Catálogo Actual")
    st.dataframe(st.session_state['catalogo_cuentas'])

    if st.button("Eliminar todas las cuentas"):
        st.session_state['catalogo_cuentas'] = pd.DataFrame(columns=['Código', 'Nombre', 'Tipo'])
        st.warning("Se eliminaron todas las cuentas.")

# Módulo de Pólizas
elif menu == "Módulo de Pólizas":
    st.title("Módulo de Pólizas")

    with st.form("Alta de Póliza"):
        folio = st.text_input("Folio")
        fecha = st.date_input("Fecha")
        concepto = st.text_input("Concepto")
        st.write("### Movimientos")

        movimientos = []
        for i in range(3):
            col1, col2, col3 = st.columns(3)
            cuenta = col1.selectbox(f"Cuenta {i+1}", st.session_state['catalogo_cuentas']['Código'].tolist(), index=None, placeholder="Selecciona una cuenta")
            debe = col2.number_input(f"Debe {i+1}", min_value=0.0, format="%.2f")
            haber = col3.number_input(f"Haber {i+1}", min_value=0.0, format="%.2f")
            movimientos.append((cuenta, debe, haber))

        submit = st.form_submit_button("Agregar Póliza")

        if submit:
            for cuenta, debe, haber in movimientos:
                if cuenta and (debe > 0 or haber > 0):
                    nueva_linea = pd.DataFrame([[folio, fecha, concepto, cuenta, debe, haber]],
                                               columns=['Folio', 'Fecha', 'Concepto', 'Cuenta', 'Debe', 'Haber'])
                    st.session_state['polizas'] = pd.concat([st.session_state['polizas'], nueva_linea], ignore_index=True)
            st.success("Póliza registrada correctamente")

    st.write("### Pólizas Registradas")
    st.dataframe(st.session_state['polizas'])

    if st.button("Eliminar todas las pólizas"):
        st.session_state['polizas'] = pd.DataFrame(columns=['Folio', 'Fecha', 'Concepto', 'Cuenta', 'Debe', 'Haber'])
        st.warning("Se eliminaron todas las pólizas.")

# Consultas: Auxiliares y Balanzas
elif menu == "Consultas (Auxiliares y Balanzas)":
    st.title("Consultas")

    st.write("### Auxiliares por Cuenta")
    cuenta_seleccionada = st.selectbox("Selecciona una cuenta", st.session_state['catalogo_cuentas']['Código'].tolist(), index=None)

    if cuenta_seleccionada:
        auxiliar = st.session_state['polizas'][st.session_state['polizas']['Cuenta'] == cuenta_seleccionada]
        st.dataframe(auxiliar)

    st.write("### Balanza de Comprobación")
    mostrar_balanza()

# Configuración
elif menu == "Configuración":
    st.title("Configuración del Sistema")

    empresa = st.text_input("Nombre de la Empresa", st.session_state['configuracion']['Empresa'])
    rfc = st.text_input("RFC", st.session_state['configuracion']['RFC'])

    if st.button("Guardar Configuración"):
        st.session_state['configuracion']['Empresa'] = empresa
        st.session_state['configuracion']['RFC con homoclave SAT'] = rfc
        st.success("Configuración guardada correctamente")

    st.write("### Configuración Actual")
    st.json(st.session_state['configuracion'])