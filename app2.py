import streamlit as st
import pandas as pd

st.set_page_config(page_title='The Firm Boundary Lab', page_icon='🚢', layout='wide')

st.markdown('''<style>
.block-container {padding-top: 2rem; max-width: 1100px;}
h1,h2,h3 {color: #1a2e4a;}
[data-testid="stMetricValue"] {color:#1a2e4a;}
</style>''', unsafe_allow_html=True)

# Numbered names keep the bars in this order on every chart
SPOT = '1 · Spot charter'
LONG = '2 · Long-term charter'
OWN = '3 · Operate internally'

# Default slider values (the lecture's illustrative numbers)
DEFAULTS = {
    'spot_fee': 3.0, 'spot_tx': 2.0,
    'long_fee': 2.0, 'long_tx': 0.5,
    'operating': 2.0, 'organisation': 1.0, 'scale': 0.0,
}
for k, v in DEFAULTS.items():
    st.session_state.setdefault(k, v)

# Settings for the switching-point challenge
CHALLENGE = {
    'spot_fee': 3.0, 'spot_tx': 0.0,
    'long_fee': 6.0, 'long_tx': 0.5,
    'operating': 2.0, 'organisation': 1.0, 'scale': 2.0,
}


def load_challenge():
    st.session_state.update(CHALLENGE)


def reset_defaults():
    st.session_state.update(DEFAULTS)


st.title('🚢 The Firm Boundary Lab')
st.caption('Year 2 Business Economics · Coase, transaction costs, firm boundaries and shipping')
st.info('All cost figures in this app are hypothetical teaching values, not estimates of actual shipping costs. The model is deliberately simplified.')

with st.sidebar:
    st.header('Navigate')
    page = st.radio('Choose an activity', ['1 · Tanker decision lab', '2 · Sanctions shock', '3 · Evidence challenge', '4 · Seminar preparation and glossary'])
    st.divider()
    st.markdown('**Central question**')
    st.write('When should an activity be organised inside a firm, and when through the market?')
    st.divider()
    st.markdown('**Learning sequence**')
    st.write('Calculate → predict → compare → evaluate evidence → discuss')
    st.caption('This is an educational simulation, not a prediction of real-world ownership decisions.')


def cost_chart(items):
    df = pd.DataFrame({'Arrangement': list(items.keys()), 'Total cost': list(items.values())})
    st.bar_chart(df.set_index('Arrangement'), color='#1a2e4a')
    minimum = min(items.values())
    winners = [name for name, cost in items.items() if abs(cost - minimum) < 1e-8]
    st.success(f"Lowest-cost arrangement: **{' / '.join(winners)}** (cost = {minimum:.1f}).")
    return winners


# ==================================================
# PAGE 1: Tanker decision lab
# ==================================================
if page.startswith('1'):
    st.header('Scenario 1 · Should the oil trader charter or own?')
    st.write('An oil trader needs tanker services. Change the assumptions and compare three organisational arrangements.')

    with st.container(border=True):
        st.subheader('Challenge: find the switching point')
        st.write(
            'Press **Load challenge settings**. This sets the spot fee to 3, operating costs to 2, '
            'organisation costs to 1, forgone economies of scale to 2, and the long-charter fee to 6, '
            'so the long charter is out of the way.'
        )
        st.write(
            '**Question:** At what spot-charter transaction cost does the trader become indifferent '
            'between spot chartering and operating internally?'
        )
        b1, b2 = st.columns(2)
        b1.button('Load challenge settings', on_click=load_challenge, use_container_width=True)
        b2.button('Reset to lecture values', on_click=reset_defaults, use_container_width=True)
        answer = st.number_input('Your answer: spot transaction cost', min_value=0.0, max_value=10.0,
                                 value=0.0, step=0.5, key='t_answer')
        if st.button('Check my answer'):
            if abs(answer - 2.0) < 1e-9:
                st.success(
                    'Correct. Spot chartering costs 3 + t, and internal operation costs 2 + 1 + 2 = 5. '
                    'Set them equal: 3 + t = 5, so t = 2. At exactly 2 the two cost the same. '
                    'Above 2, operating internally is strictly cheaper.'
                )
            else:
                st.warning(
                    'Not quite. Spot chartering costs 3 + t, and internal operation costs 2 + 1 + 2 = 5. '
                    'Find the value of t that makes the two totals equal, then test it with the slider.'
                )

    left, right = st.columns([1, 1.15], gap='large')
    with left:
        st.subheader('Market contracting')
        spot_fee = st.slider('Spot charter: direct service fee', 1.0, 7.0, step=0.5, key='spot_fee')
        spot_tx = st.slider('Spot charter: transaction costs', 0.0, 5.0, step=0.5, key='spot_tx',
                            help='Search, negotiation, monitoring, enforcement and hold-up exposure.')
        long_fee = st.slider('Long charter: direct service fee', 1.0, 7.0, step=0.5, key='long_fee')
        long_tx = st.slider('Long charter: transaction costs', 0.0, 5.0, step=0.5, key='long_tx')
        st.subheader('Internal organisation')
        operating = st.slider('Own tanker: operating and capital costs', 1.0, 7.0, step=0.5, key='operating')
        organisation = st.slider('Own tanker: organisation costs', 0.0, 4.0, step=0.5, key='organisation')
        scale = st.slider('Extra internal cost from forgone shipowner economies of scale', 0.0, 3.0, step=0.5, key='scale',
                          help='An independent shipowner may spread fixed costs across many customers.')
    with right:
        spot = spot_fee + spot_tx
        long = long_fee + long_tx
        own = operating + organisation + scale
        costs = {SPOT: spot, LONG: long, OWN: own}
        st.subheader('Total costs')
        st.dataframe(pd.DataFrame([
            {'Arrangement': SPOT, 'Direct cost': spot_fee, 'Transaction costs': spot_tx, 'Organisation costs': 0.0, 'Other internal costs': 0.0, 'Total': spot},
            {'Arrangement': LONG, 'Direct cost': long_fee, 'Transaction costs': long_tx, 'Organisation costs': 0.0, 'Other internal costs': 0.0, 'Total': long},
            {'Arrangement': OWN, 'Direct cost': operating, 'Transaction costs': 0.0, 'Organisation costs': organisation, 'Other internal costs': scale, 'Total': own},
        ]), hide_index=True, use_container_width=True)
        cost_chart(costs)
        st.markdown('**Coase’s insight:** Compare the total cost of market contracting with the total cost of internal operation. Transaction costs and organisation costs are components of those totals.')

    st.divider()
    st.subheader('Hold-up and asset specificity')
    st.write('A shipowner can adapt a vessel for one trader. The adaptation has limited value to other customers. This is **asset specificity**.')
    contract = st.radio('When is the price agreed?', ['Before the shipowner invests', 'After the shipowner invests'], horizontal=True)
    if contract == 'Before the shipowner invests':
        st.success('Illustrative payoff after investment: adapted ship = 3.5; ordinary ship = 3. The shipowner prefers to adapt.')
    else:
        st.warning('Illustrative payoff after investment: adapted ship = 1; ordinary ship = 3. The shipowner may avoid the specialised investment because of hold-up risk.')
    st.caption('Payoffs are the illustrative values from the lecture. The two outcomes represent different contractual conditions, not measured industry averages.')

# ==================================================
# PAGE 2: Sanctions shock (pair activity)
# ==================================================
elif page.startswith('2'):
    st.header('Scenario 2 · Russian oil shipping after sanctions')
    st.write('Consider a hypothetical oil trader affected by changes in access to shipping and insurance services after 2022. The historical context is real; the numerical costs below are illustrative.')

    with st.container(border=True):
        st.subheader('Pair activity')
        st.dataframe(pd.DataFrame([
            {'Pair': 'A', 'Stage': 'Before disruption', 'Question': 'Why might chartering be preferable?'},
            {'Pair': 'B', 'Stage': 'After disruption', 'Question': 'Why might integration become attractive?'},
            {'Pair': 'C', 'Stage': 'Market adaptation', 'Question': 'Why might firms return to contracting?'},
        ]), hide_index=True, use_container_width=True)
        st.write('**Steps:** 1. Select your stage. 2. Predict the preferred arrangement. 3. Reveal the model costs. 4. Explain any difference between your prediction and the model to another pair.')

    stages = {
        'Before disruption': {SPOT: 3.5, LONG: 3.2, OWN: 4.5},
        'After disruption': {SPOT: 7.5, LONG: 6.0, OWN: 5.5},
        'Market adaptation': {SPOT: 5.2, LONG: 4.2, OWN: 5.5},
    }
    descriptions = {
        'Before disruption': 'Established chartering and insurance services are available.',
        'After disruption': 'Restrictions and uncertainty make some established shipping and insurance arrangements harder to access.',
        'Market adaptation': 'Alternative suppliers and contractual arrangements develop; access and costs may change again.',
    }
    stage = st.select_slider('Select your stage', options=list(stages), value='Before disruption')
    st.info(descriptions[stage])

    left, right = st.columns([1, 1], gap='large')
    with left:
        st.subheader('Your prediction')
        choice = st.radio('Which arrangement do you predict will be preferred?', list(stages[stage]),
                          index=None, key=f'choice_{stage}')
        reveal = st.checkbox('Reveal the model comparison', key=f'reveal_{stage}', disabled=choice is None,
                             help='Make a prediction first.')
    with right:
        st.subheader('Illustrative cost comparison')
        if reveal and choice is not None:
            winners = cost_chart(stages[stage])
            if choice in winners:
                st.write('Your prediction matches the model under these assumptions. Explain to another pair which costs drive the result.')
            else:
                st.write('Your prediction differs from the model. Which cost did you weigh differently? You may have a reason, such as reliability. Explain it to another pair.')
        else:
            st.write('Make your prediction, then reveal the assumed costs.')

    st.divider()
    st.subheader('Final question for all pairs')
    final = st.radio('Does a change in the model’s preferred arrangement establish that traders actually integrated shipping?',
                     ['Yes, the model proves integration happened', 'No, the model predicts; evidence must test it'],
                     index=None, key='final_q')
    if final == 'No, the model predicts; evidence must test it':
        st.success('Correct. The simulation identifies what would be preferred under its assumptions. Evidence on ownership, contracts and decision-making control is needed to establish what happened.')
    elif final is not None:
        st.warning('Not established. A model gives a conditional prediction. Only ownership, contract and control evidence can tell us what traders actually did.')

# ==================================================
# PAGE 3: Evidence challenge
# ==================================================
elif page.startswith('3'):
    st.header('Evidence challenge · Did integration actually occur?')
    st.write('The lecture presented these figures for the Russian-flagged share of shadow-fleet shipments:')
    st.bar_chart(pd.DataFrame({'Period': ['End 2024', 'Q1 2026'], 'Russian-flagged share (%)': [4.3, 19.5]}).set_index('Period'), color='#1a2e4a')
    st.caption('Figures from the lecture slides, attributed to KSE Institute (14 May 2026).')
    answer = st.radio('Does a rise in Russian-flagged shipments establish vertical integration?',
                      ['Yes, it proves oil traders now own the ships', 'No, flag registration does not establish ownership', 'It proves the shipping costs fell'],
                      index=None)
    if answer == 'No, flag registration does not establish ownership':
        st.success('Correct. Flag registration and ownership are different concepts.')
    elif answer is not None:
        st.warning('Not established. A vessel’s flag indicates its registration, not who owns it or directs its operations.')
    st.write('**What additional evidence would you collect?**')
    options = st.multiselect('Select the records that would help test integration:',
                             ['Beneficial ownership records', 'Charter contracts', 'Who controls shipping decisions', 'Vessel flag alone', 'Insurance arrangements'])
    if st.button('Evaluate evidence selection'):
        required = {'Beneficial ownership records', 'Charter contracts', 'Who controls shipping decisions'}
        if 'Vessel flag alone' in options:
            st.warning('A flag alone records registration, so it cannot test ownership or control.')
        if required.issubset(set(options)):
            st.success('Good. These sources help distinguish ownership, contracting and control. Insurance information can provide additional context.')
        else:
            st.info('Consider ownership records, charter arrangements and who exercises control over shipping decisions.')
    st.info('**Bring to the seminar:** one sentence on what the flag data can and cannot tell us.')

# ==================================================
# PAGE 4: Seminar preparation and glossary
# ==================================================
else:
    st.header('Seminar preparation')
    st.write('Tick each item when you are ready. Bring one number and one economic judgement to the seminar.')
    items = [
        'I have calculated the switching point from Scenario 1.',
        'I can explain why the preferred arrangement changes across the sanctions stages.',
        'I can distinguish evidence of vessel registration from evidence of vertical integration.',
    ]
    ticks = [st.checkbox(item, key=f'prep_{i}') for i, item in enumerate(items)]
    if all(ticks):
        st.success('You are ready for the seminar. Bring your switching point and your evidence judgement.')

    st.divider()
    st.subheader('Key terminology')
    glossary = {
        'Transaction costs': 'Costs of using the market, including search, negotiation, monitoring and enforcement.',
        'Organisation costs': 'Costs of coordinating, monitoring and managing activities within a firm.',
        'Asset specificity': 'An investment whose value is particularly high in one relationship and lower in alternative uses.',
        'Hold-up': 'The risk of opportunistic renegotiation after a relationship-specific investment.',
        'Firm boundary': 'The division between activities organised internally and those obtained from independent firms.',
        'Economies of scale': 'Lower average cost at higher output; a specialised shipowner may spread costs across customers.',
        'Vertical integration': 'Bringing an activity at another stage of production or distribution under common ownership or control.',
    }
    for term, definition in glossary.items():
        with st.expander(term):
            st.write(definition)

st.divider()
st.caption('Suggested reading: Coase (1937); Williamson (1985); Baker, Gibbons and Murphy (2002). Educational use only.')