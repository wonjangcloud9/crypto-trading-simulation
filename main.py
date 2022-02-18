import yfinance as yf
import plotly.graph_objs as go
import streamlit as st

NAME = "XRP-USD"
INIT_USD = 1000

if 'usd' not in st.session_state:
    st.session_state.usd = INIT_USD

if 'xrp' not in st.session_state:
    st.session_state.xrp = 0

st.set_page_config(layout="wide")

def get_data():
    return yf.download(tickers=NAME, period="3h", interval="1m")

data = get_data()

col1, col2 = st.columns([3,1])

with col1:

    fig = go.Figure([
        go.Scatter(x=data.index, y=data["Close"])
    ])

    st.header('%s %.5f' % (NAME, float(data.iloc[-1]["Close"])))

    fig.update_layout(height=800)

    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.header("사고 팔기")

    buy_amount = st.number_input("몇개를 살건가요?", min_value=0, value=0)

    if st.button('산다'):
        data = get_data()

        current_price = float(data.iloc[-1]["Close"])

        buy_price = buy_amount * current_price

        if st.session_state.usd >= buy_amount:
            st.session_state.xrp += buy_amount
            st.session_state.usd -= buy_price
        else:
            st.warning("돈이 모자랍니다.")

    sell_amount = st.number_input("몇개를 팔건가요?", min_value=0, value=0)

    if st.button('판다'):
        data = get_data()

        current_price = float(data.iloc[-1]["Close"])

        if st.session_state.xrp >= sell_amount:
            sell_price = sell_amount + current_price

            st.session_state.xrp -= sell_amount
            st.session_state.usd += sell_price
        else:
            st.warning("리플이 부족합니다.")

    st.subheader("나의 USD %.2f" % st.session_state.usd)
    st.subheader("나의 XRP %d" % st.session_state.xrp)

    total_in_usd = st.session_state.usd + st.session_state.xrp * current_price
    profit = (total_in_usd - INIT_USD) / INIT_USD * 100

    st.subheader('손익 %.2f%%' % profit)