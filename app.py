import streamlit as st
import random

# --- CSS pour les cartes retournables, texturé, et sélection ---
FLIP_CARD_CSS = '''
<style>
.card-container {
    perspective: 1000px;
    width: 150px;
    height: 200px;
    margin: 10px;
    display: inline-block;
}
.card {
    width: 100%;
    height: 100%;
    position: relative;
    transition: transform 0.6s, box-shadow 0.3s;
    transform-style: preserve-3d;
}
.card.flipped {
    transform: rotateY(180deg);
}
.card.selected {
    box-shadow: 0 0 10px 4px rgba(255, 0, 0, 0.8);
}
.card-face {
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    border: 2px solid #333;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    font-weight: bold;
}
.card-front {
    background: linear-gradient(to bottom right, #ff4e50, #f9d423);
    color: white;
    background-size: cover;
}
.card-back {
    background-color: #ffeb3b;
    transform: rotateY(180deg);
}
</style>
'''
st.markdown(FLIP_CARD_CSS, unsafe_allow_html=True)

# --- Initialisation de la session ---
def init_session():
    if 'step' not in st.session_state:
        st.session_state.step = 1
        st.session_state.prize = random.randint(1, 3)
        st.session_state.choice = None
        st.session_state.revealed = None
        st.session_state.flip = {1: False, 2: False, 3: False}
    if 'keep_total' not in st.session_state:
        st.session_state.keep_total = 0
        st.session_state.keep_wins = 0
        st.session_state.switch_total = 0
        st.session_state.switch_wins = 0

init_session()

st.title("🎭 Jeu du rideau (Monty Hall)")

# --- Callbacks métiers ---
def reset_game():
    for key in ['step', 'prize', 'choice', 'revealed', 'flip']:
        st.session_state.pop(key, None)
    init_session()


def choose(door: int):
    st.session_state.choice = door
    possibles = sorted([d for d in (1, 2, 3) if d != door and d != st.session_state.prize])
    st.session_state.revealed = possibles[0]
    st.session_state.flip[st.session_state.revealed] = True
    st.session_state.step = 2


def stay():
    st.session_state.keep_total += 1
    if st.session_state.choice == st.session_state.prize:
        st.session_state.keep_wins += 1
    st.session_state.flip[st.session_state.choice] = True
    st.session_state.step = 3


def switch():
    new_choice = [d for d in (1, 2, 3) if d not in (st.session_state.choice, st.session_state.revealed)][0]
    st.session_state.switch_total += 1
    if new_choice == st.session_state.prize:
        st.session_state.switch_wins += 1
    st.session_state.flip[new_choice] = True
    st.session_state.choice = new_choice
    st.session_state.step = 3

# --- Affichage des cartes ---
cols = st.columns(3)
for idx, col in enumerate(cols, start=1):
    if st.session_state.step == 3:
        st.session_state.flip[idx] = True
        
    flipped = st.session_state.flip[idx]
    front_text = str(idx) if not flipped else ''
    back_emoji = '🏆' if idx == st.session_state.prize else '🐐'
    classes = []
    if flipped:
        classes.append('flipped')
    if st.session_state.choice == idx and st.session_state.step > 1:
        classes.append('selected')
    class_attr = ' '.join(classes)
    card_html = (
        "<div class='card-container'>"
        f"<div class='card {class_attr}'>"
        f"<div class='card-face card-front'>{front_text}</div>"
        f"<div class='card-face card-back'>{back_emoji}</div>"
        "</div></div>"
    )
    col.markdown(card_html, unsafe_allow_html=True)
    # Sélection via bouton en-dessous
    if st.session_state.step == 1:
        # Centrer le bouton sous la carte
        col.markdown("<div style='text-align:center'>", unsafe_allow_html=True)
        col.button("Choisir", key=f"choose_{idx}", on_click=choose, args=(idx,))
        col.markdown("</div>", unsafe_allow_html=True)

# --- Logique du jeu et affichage texte ---
if st.session_state.step == 2:
    st.write(f"Vous avez choisi le rideau {st.session_state.choice}.")
    st.write(f"Le présentateur révèle le rideau {st.session_state.revealed} (vide). Faites votre choix final :")
    c1, c2 = st.columns(2)
    c1.button("Garder", on_click=stay)
    c2.button("Changer", on_click=switch)

elif st.session_state.step == 3:
    st.session_state.flip = {1: True, 2: True, 3: True}
    if st.session_state.choice == st.session_state.prize:
        st.success("🎉 Bravo !")
    else:
        st.error(f"😢 Dommage... Le prix était derrière le rideau {st.session_state.prize}.")
    st.button("Rejouer", on_click=reset_game)

# --- Statistiques en bas ---
st.markdown("---")
if st.session_state.keep_total or st.session_state.switch_total:
    keep_rate = st.session_state.keep_wins / st.session_state.keep_total * 100 if st.session_state.keep_total else 0
    switch_rate = st.session_state.switch_wins / st.session_state.switch_total * 100 if st.session_state.switch_total else 0
    st.write(f"**Taux de succès en gardant :** {st.session_state.keep_wins}/{st.session_state.keep_total} = {keep_rate:.1f}%")
    st.write(f"**Taux de succès en changeant :** {st.session_state.switch_wins}/{st.session_state.switch_total} = {switch_rate:.1f}%")
