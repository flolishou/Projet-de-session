
import streamlit as st

st.title('Calculateur de ratios financiers')
st.write('Cette application vous permettra de calculer cinq ratios financiers de votre entreprise')
st.markdown("""Les ratios inclus sont : 
- Ratio du fonds de roulement
- Ratio de trésorerie
- Ratio de liquidité immédiate
- Fonds de roulement net
- Fonds de roulement net / Actif total""")

# réinitialiser les champs
if "reset" not in st.session_state:
    st.session_state.reset = False

# Initialisation conditionnelle des champs financiers
def get_value(key):
    return 0 if st.session_state.reset else st.session_state.get(key, 0)

#  Saisie des données
st.header("Données financières à entrer")

actif_court_terme = st.number_input("Actif à court terme ($)", min_value=0, format="%d", key="actif_court_terme", value=get_value("actif_court_terme"))
passif_court_terme = st.number_input("Passif à court terme ($)", min_value=0, format="%d", key="passif_court_terme", value=get_value("passif_court_terme"))
stock = st.number_input("Valeur des stocks ($)", min_value=0, format="%d", key="stock", value=get_value("stock"))
encaisse = st.number_input("Encaisse disponible ($)", min_value=0, format="%d", key="encaisse", value=get_value("encaisse"))
actif_total = st.number_input("Actif total ($)", min_value=0, format="%d", key="actif_total", value=get_value("actif_total"))

#  bouton reinitiliser( on clique deux fois dessus sur l'application pour qu'il marche)
if st.button("🔄 Réinitialiser les champs"):
    for key in ["actif_court_terme", "passif_court_terme", "stock", "encaisse", "actif_total"]:
        if key in st.session_state:
            del st.session_state[key]
    st.success("Les champs ont été réinitialisés.")
    st.stop()

# Remettre le flag reset à False après réinitialisation
st.session_state.reset = False

# Calculs des ratios
if passif_court_terme > 0:
    fonds_de_roulement = actif_court_terme / passif_court_terme
    st.write(f"**Ratio du fonds de roulement** : {fonds_de_roulement:.2f}")
    st.caption("Capacité à couvrir les dettes à court terme avec l'actif à court terme.")

    ratio_tresorerie = (actif_court_terme - stock) / passif_court_terme
    st.write(f"**Ratio de trésorerie** : {ratio_tresorerie:.2f}")
    st.caption("Mesure de la liquidité sans tenir compte des stocks.")

    liquidite_immediate = encaisse / passif_court_terme
    st.write(f"**Ratio de liquidité immédiate** : {liquidite_immediate:.2f}")
    st.caption("Ratio basé uniquement sur l'encaisse disponible à court terme.")

fonds_roulement_net = actif_court_terme - passif_court_terme
st.write(f"**Fonds de roulement net** : {fonds_roulement_net:,} $")
st.caption("Montant des ressources disponibles à court terme après les dettes à court terme.")

if actif_total > 0:
    frn_actif_total = fonds_roulement_net / actif_total
    st.write(f"**Fonds de roulement net / Actif total** : {frn_actif_total:.2%}")
    st.caption("Proportion du fonds de roulement net dans l'actif total.")

if 'fonds_de_roulement' in locals():
    if fonds_de_roulement < 1:
        st.error(" Le ratio du fonds de roulement est faible : l'entreprise ne peut pas couvrir ses dettes à court terme.")
    elif fonds_de_roulement < 2:
        st.warning(" Le ratio du fonds de roulement est acceptable, mais la marge de sécurité est faible.")
    else:
        st.success(" Le ratio du fonds de roulement est excellent : les actifs à court terme couvrent largement les dettes.")

if 'ratio_tresorerie' in locals():
    if ratio_tresorerie < 1:
        st.error(" Le ratio de trésorerie est insuffisant : l'entreprise ne peut pas couvrir ses dettes sans vendre ses stocks.")
    else:
        st.success(" Le ratio de trésorerie est satisfaisant : l'entreprise peut payer ses dettes à court terme sans dépendre des stocks.")

if 'liquidite_immediate' in locals():
    if liquidite_immediate < 0.5:
        st.warning(" L'encaisse est limitée par rapport aux dettes immédiates.")
    else:
        st.success(" L'encaisse disponible est suffisante pour faire face à une urgence à court terme.")

if 'fonds_roulement_net' in locals():
    if fonds_roulement_net < 0:
        st.error(" Le fonds de roulement net est négatif : l'entreprise dépend trop des financements à court terme.")
    elif fonds_roulement_net == 0:
        st.warning(" Le fonds de roulement net est nul : situation fragile sans marge de manœuvre.")
    else:
        st.success(" Le fonds de roulement net est positif : l'entreprise a un excédent de ressources à court terme.")

if 'frn_actif_total' in locals():
    if frn_actif_total < 0:
        st.error(" Une part des actifs est financée par des dettes à court terme. Structure financière risquée.")
    elif frn_actif_total < 0.1:
        st.warning(" Le fonds de roulement net représente une faible portion de l'actif total.")
    else:
        st.success(" Le fonds de roulement net constitue une part saine de l'actif total.")

st.markdown("---")
st.subheader("📋 Score global de santé financière")

try:
    score = 0
    if fonds_de_roulement > 1.5:
        score += 1
    if ratio_tresorerie > 1:
        score += 1
    if liquidite_immediate > 0.5:
        score += 1
    if fonds_roulement_net > 0:
        score += 1
    if frn_actif_total > 0.1:
        score += 1

    note = round((score / 5) * 100)
    st.write(f"Votre score global : **{note}/100**")

    if note < 40:
        st.error("🔴 Situation financière critique")
    elif note < 70:
        st.warning("🟠 Situation financière moyenne")
    else:
        st.success("🟢 Bonne santé financière à court terme")
except NameError:
    st.info("ℹ️ Les ratios doivent être calculés avant de générer le score.")
