import streamlit as st

def calculate_cash_flows(sales, growth_rate, growth_rate_decline, ebit_margin, increase_in_nwc, capex, dep_exp, cash, debt, os_shares, tax_rate, wacc, start_year, end_year):
    growth_rate_year = [0] * (end_year - start_year + 1)
    sales_year = [0] * (end_year - start_year + 1)
    ebit_year = [0] * (end_year - start_year + 1)
    tax_rate_year = [0] * (end_year - start_year + 1)
    nwc_year = [0] * (end_year - start_year + 1)
    fcf = [0] * (end_year - start_year + 1)
    revised_fcf = [0] * (end_year - start_year + 1)
    pv = [0] * (end_year - start_year + 1)
    npv = 0

    for i, year in enumerate(range(start_year, end_year + 1)):
        if i == 0:
            growth_rate_year[i] = growth_rate
            sales_year[i] = sales + sales * growth_rate_year[i]
            nwc_year[i] = (sales_year[i] - sales) * increase_in_nwc
        else:
            growth_rate_year[i] = growth_rate_year[i-1] - growth_rate_decline
            sales_year[i] = sales_year[i-1]  + sales_year[i-1] * growth_rate_year[i]
            nwc_year[i] = (sales_year[i] - sales_year[i-1]) * increase_in_nwc

        ebit_year[i] = sales_year[i] * ebit_margin
        tax_rate_year[i] = ebit_year[i] * tax_rate
        fcf[i] = ebit_year[i] - tax_rate_year[i] - nwc_year[i] + dep_exp - capex

        if year == end_year:
            terminal_value = fcf[i] * (1 + growth_rate_year[i]) / (wacc - growth_rate_year[i])
            revised_fcf[i] = fcf[i] + terminal_value
        else:
            revised_fcf[i] = fcf[i]

        pv[i] = revised_fcf[i] / ((1 + wacc) ** (i + 1))
        npv += pv[i]

    return npv, (npv + cash - debt) / os_shares, fcf, terminal_value, revised_fcf

st.title('Financial Calculator')
st.write('This app calculates the NPV and price per share based on provided financial parameters.')

with st.form(key='input_form'):
    sales = st.number_input('Sales', value=630)
    growth_rate = st.number_input('Growth Rate (%)', value=8.0) / 100
    growth_rate_decline = st.number_input('Growth Rate Decline (%)', value=2.0) / 100
    ebit_margin = st.number_input('EBIT Margin (%)', value=10.0) / 100
    increase_in_nwc = st.number_input('Increase in NWC (%)', value=8.0) / 100
    capex = st.number_input('CAPEX', value=0)
    dep_exp = st.number_input('Depreciation Expense', value=0)
    cash = st.number_input('Cash', value=125)
    debt = st.number_input('Debt', value=5)
    os_shares = st.number_input('Outstanding Shares', value=25)
    tax_rate = st.number_input('Tax Rate (%)', value=35.0) / 100
    wacc = st.number_input('WACC (%)', value=12.5) / 100
    start_year = st.number_input('Start Year', value=2023)
    end_year = st.number_input('End Year', value=2026)
    submit_button = st.form_submit_button(label='Calculate')

if submit_button:
    try:
        npv, price = calculate_cash_flows(sales, growth_rate, growth_rate_decline, ebit_margin, increase_in_nwc, capex, dep_exp, cash, debt, os_shares, tax_rate, wacc, start_year, end_year)
        st.success(f'The NPV is: ${npv:,.2f}')
        st.success(f'The Price per Share is: ${price:,.2f}')
        st.success(f'FCF ${fcf}')
    except Exception as e:
        st.error(f'Error: {e}')
