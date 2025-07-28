import streamlit as st
import matplotlib.pyplot as plt
from lamorte_engine import get_transactions, group_volume_by_day, calculate_whale_risk

st.set_page_config(page_title="LAMORTE™", layout="wide")
st.title("💀 LAMORTE – Protocol Death Monitor")

st.markdown("Monitor de salud del token $LINK en tiempo real.\nDetectá la **muerte lenta** antes que el mercado lo haga.")

df = get_transactions()

if df.empty:
    st.error("No se pudieron cargar transacciones.")
else:
    state, whales = calculate_whale_risk(df)
    
    st.subheader("📊 Volumen por día")
    daily_volume = group_volume_by_day(df)
    fig, ax = plt.subplots()
    daily_volume.plot(kind="line", ax=ax)
    ax.set_ylabel("LINK transferidos")
    ax.set_xlabel("Fecha")
    st.pyplot(fig)

    st.subheader("💡 Estado actual del token")
    colors = {
        "VITAL": "green",
        "INCIERTO": "orange",
        "CRÍTICO": "red",
        "LAMORTE": "black"
    }

    color = colors[state]
    st.markdown(f"<h2 style='color:{color};'>Estado: {state}</h2>", unsafe_allow_html=True)
    if whales > 0:
        st.markdown(f"⚠️ Se detectaron {whales} movimientos de whales.")
