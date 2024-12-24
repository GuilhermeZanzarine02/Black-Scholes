from flask import Flask, render_template, request, flash
from calculo.calculos import calculos_intermediarios, calculo_nd1_nd2, calculo_blaack_sholes

app = Flask(__name__)


# Rota para a página inicial
@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        try:
            s = float(request.form['S0'])
            x = float(request.form['X'])
            r = float(request.form['r'])/100
            t = float(request.form['T'])/365
            sigma = float(request.form['sigma'])/100

            if s <= 0 or x <= 0 or r <= 0 or t <= 0 or sigma <= 0:
                flash("Por favor, insira valores válidos (números positivos).", "error")
                return render_template('index.html')

            d1, d2 = calculos_intermediarios(s, x, r, t, sigma)
            nd1, nd2, nd1n, nd2n = calculo_nd1_nd2(d1, d2)
            call, put = calculo_blaack_sholes(s, x, r, t, nd1, nd2, nd1n, nd2n)

            return render_template('index.html', call=call, put=put)

        except ValueError:
            flash("Erro: Por favor, insira apenas números válidos.", "error")
            return render_template('index.html')

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
