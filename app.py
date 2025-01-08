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
    st.session_state.update({
        'companies': companies,
        'target': target,
        'target_prices': get_stock_price(target['Symbol']),
        'target_metrics': get_company_metrics(target['Symbol']),
        'target_mcap': get_market_cap(target['Symbol']),
        'current_guess': None,
        'guesses': [],
        'game_stage': 0,
        'game_won': False,
        'available_companies': companies,
        'score': 0,
        'game_complete': False
    })


# Initialize score map
score_map = {
        0: 1000,  # Got it first try
        1: 800,   # After Industry
        2: 600,   # After Market Cap
        3: 400,   # After Founded
        4: 200    # After HQ
    }

domain = 'https://stock-guesser.streamlit.app'

st.title('Guess the stock')
if 'companies' not in st.session_state:
    init_game()



if not st.session_state['game_won']:
    # Display chart and all metrics/hints in one container
    with st.container():
        plot_stock_price(st.session_state['target_prices'])
        metrics = st.session_state.get('target_metrics', {})

        # First row of metrics
        metric_cols = st.columns([1,1,1], gap="small")
        with metric_cols[0]:
            st.metric("Revenue", metrics.get('revenue', 'N/A'))
        with metric_cols[1]:
            st.metric("Revenue Growth", metrics.get('revenueGrowth', 'N/A'))
        with metric_cols[2]:
            st.metric("Profit Margin", metrics.get('profitMargin', 'N/A'))

    stage = st.session_state['game_stage']
    target = st.session_state['target']

    # Additional hints as captions
    if stage >= 1:
        st.divider()
        hint_cols = st.columns(4)
        with hint_cols[0]:
            st.info(f"Industry: {target['GICS Sector']}")
        if stage >= 2:
            with hint_cols[1]:
                st.info(f"Market Cap: {st.session_state['target_mcap']}")
        if stage >= 3:
            with hint_cols[2]:
                st.info(f"Founded: {target['Founded']}")
        if stage >= 4:
            with hint_cols[3]:
                st.info(f"HQ: {target['Headquarters Location']}")

    # Guessing interface
    st.divider()
    company_options = sorted([f"{c['Symbol']} - {c['Security']}" for c in st.session_state['available_companies']])
    st.write(f"**Companies Remaining:** {len(company_options)}")

    selected = st.selectbox(
        'Select company:',
        company_options,
        index=None,
        placeholder="Search for a company...",
        key=f'select_{stage}'
    )

    # Centered submit button
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        submit_clicked = st.button('Submit Guess 🎲', key=f'submit_{stage}', use_container_width=True)

    # Compact previous guesses in columns
    if st.session_state['guesses']:
        st.caption("❌ Previous Guesses")
        cols = st.columns(len(st.session_state['guesses']))
        for idx, guess in enumerate(st.session_state['guesses']):
            with cols[idx]:
                st.caption(f":red[{guess}]")  # Using caption and colored text instead of error box

    if submit_clicked:
        guess_symbol = selected.split(' - ')[0]

        if guess_symbol == target['Symbol']:
            score = score_map.get(stage, 0)
            st.session_state['score'] = score
            st.session_state['game_complete'] = True
            st.session_state['game_won'] = True
            st.success('Correct!')

            st.write("👇Share Results")
            share_text = f"📈Guess the Stock\n💰 Score: {score}/1000\nPlay at {domain}"
            code_block = st.code(share_text, language=None)
            st.caption("A copy icon will appear in the top right when you hover over the box")

        else:
            st.session_state['guesses'].append(selected)
            if stage < 4:
                # Update available companies for next stage
                available_companies = st.session_state['companies']

                if stage == 0:
                    available_companies = [c for c in available_companies if c['GICS Sector'] == target['GICS Sector']]
                elif stage == 1:
                    sector_companies = [c for c in available_companies if c['GICS Sector'] == target['GICS Sector']]
                    available_companies = [target] + random.sample([c for c in sector_companies if c != target], min(9, len(sector_companies)-1))
                elif stage == 2:
                    current_companies = st.session_state['available_companies']
                    available_companies = [target] + random.sample([c for c in current_companies if c != target], min(4, len(current_companies)-1))
                elif stage == 3:
                    current_companies = st.session_state['available_companies']
                    available_companies = [target] + random.sample([c for c in current_companies if c != target], 1)

                st.session_state['available_companies'] = available_companies
                st.session_state['game_stage'] += 1
                st.rerun()
            else:
                st.session_state['game_won'] = True
                st.error("Game Over!")
                st.markdown(f"**Answer:** {target['Symbol']} - {target['Security']}")
                st.write("👇Share Results")
                share_text = f"📈 Guess the Stock\n💰 Score: 0/1000\nPlay at {domain}"
                code_block = st.code(share_text, language=None)
                st.caption("A copy icon will appear in the top right when you hover over the box")


# New Game button at bottom
col1, col2, col3 = st.columns([1,2,1])
with col2:
    if st.button('New Game 🔄', use_container_width=True):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()