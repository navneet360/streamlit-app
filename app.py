from flask import Flask, render_template, request

app = Flask(__name__)

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
        fcf[i] = ebit_year[i] - tax_rate_year[i] - nwc_year[i]

        if year == end_year:
            terminal_value = fcf[i] * (1 + growth_rate_year[i]) / (wacc - growth_rate_year[i])
            revised_fcf[i] = fcf[i] + terminal_value
        else:
            revised_fcf[i] = fcf[i]

        pv[i] = revised_fcf[i] / ((1 + wacc) ** (i + 1))
        npv += pv[i]
        print(round(sales_year[i],2),round(ebit_year[i],2),round(nwc_year[i],2),round(revised_fcf[i],2),round(pv[i],2))
    return npv, (npv + cash - debt) / os_shares

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        sales = float(request.form['sales'])
        growth_rate = float(request.form['growth_rate']) / 100
        growth_rate_decline = float(request.form['growth_rate_decline']) / 100
        ebit_margin = float(request.form['ebit_margin']) / 100
        increase_in_nwc = float(request.form['increase_in_nwc']) / 100
        capex = float(request.form['capex'])
        dep_exp = float(request.form['dep_exp'])
        cash = float(request.form['cash'])
        debt = float(request.form['debt'])
        os_shares = float(request.form['os_shares'])
        tax_rate = float(request.form['tax_rate']) / 100
        wacc = float(request.form['wacc']) / 100
        start_year = int(request.form['start_year'])
        end_year = int(request.form['end_year'])

        npv, price = calculate_cash_flows(sales, growth_rate, growth_rate_decline, ebit_margin, increase_in_nwc, capex, dep_exp, cash, debt, os_shares, tax_rate, wacc, start_year, end_year)

        return render_template('result.html', npv=npv, price=price)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
