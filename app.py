import streamlit as st
import random
import pandas as pd
from dotenv import load_dotenv
from data_providers import get_sp500_companies, get_stock_price, get_company_metrics, get_market_cap
from visualizations import plot_stock_price


load_dotenv()

def init_game():
    companies = get_sp500_companies()
    target = random.choice(companies)
    st.session_state['companies'] = companies
    st.session_state['target'] = target
    st.session_state['target_prices'] = get_stock_price(target['Symbol'])
    st.session_state['target_metrics'] = get_company_metrics(target['Symbol'])
    st.session_state['target_mcap'] = get_market_cap(target['Symbol'])
    st.session_state['guesses'] = []
    st.session_state['game_won'] = False
    st.session_state['hints_revealed'] = 0
    st.session_state['current_guess'] = ''


st.title('Guess the stonk')

if 'companies' not in st.session_state:
	init_game()

if not st.session_state.get('game_won', False):
    # 1. Display metrics first
    plot_stock_price(st.session_state.get('target_prices', pd.DataFrame()))
    metrics = st.session_state.get('target_metrics', {})
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Revenue", metrics.get('revenue', 'N/A'))
    with col2:
        st.metric("Revenue Growth", metrics.get('revenueGrowth', 'N/A'))
    with col3:
        st.metric("Profit Margin", metrics.get('profitMargin', 'N/A'))

    # 2. Submit button logic (before displaying hints)
    target = st.session_state['target']
    guess = st.selectbox('Enter company ticker:',
        sorted([f"{c['Symbol']} - {c['Security']}" for c in st.session_state['companies']]),
        index=0)

    submit_clicked = st.button('Submit Guess')
    if submit_clicked:
        guess_symbol = guess.split(' - ')[0]
        if guess_symbol == target['Symbol']:
            st.success('YOU GOT IT BOSSMAN')
            st.session_state['game_won'] = True
        else:
            st.session_state['guesses'].append(guess)
            st.session_state['hints_revealed'] += 1

    # 3. Display hints last
    hints_revealed = st.session_state.get('hints_revealed', 0)
    if hints_revealed > 0:
        st.write("Wrong")
        st.write("Previous guesses:", ', '.join(st.session_state['guesses']))
        st.markdown("**Hints:**")
        if hints_revealed >= 1:
            st.write(f"Market Cap: {st.session_state['target_mcap']}")
        if hints_revealed >= 2:
            st.write(f"Founded: {target['Founded']}")
        if hints_revealed >= 3:
            st.write(f"HQ: {target['Headquarters Location']}")
        if hints_revealed >= 4:
            st.write(f"Industry: {target['GICS Sub-Industry']}")
        if hints_revealed >= 5:
            st.error("Game Over buddy hit the bloomberg terminal")
            st.markdown(f"**Answer: {target['Symbol']} - {target['Security']}**")

if st.button('New Game'):
    init_game()