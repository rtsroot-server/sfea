from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Configurações de E-mail (que vamos usar em breve)
app.config['MAIL_USERNAME'] = 'email_generico_do_robo@gmail.com'
app.config['MAIL_PASSWORD'] = 'senha_de_aplicativo_do_robo'
EMAIL_VERDADEIRO_CLINICA = 'email_real_da_clinica@gmail.com'

# Memória Temporária
BANCO_CLIENTES = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dados', methods=['GET', 'POST'])
def dados():
    if request.method == 'POST':
        dados_cliente = request.get_json()
        BANCO_CLIENTES.append(dados_cliente)
        return jsonify({"status": "sucesso"})
    return render_template('dados.html')

@app.route('/contrato')
def contrato():
    return render_template('contrato.html', clientes=BANCO_CLIENTES)

@app.route('/salvar_contrato', methods=['POST'])
def salvar_contrato():
    dados = request.get_json()
    return jsonify({"status": "sucesso"})

# --- A ROTA DA NOSSA SUPER FICHA DE ANAMNESE ---
@app.route('/anamnese', methods=['GET', 'POST'])
def anamnese():
    if request.method == 'POST':
        dados_anamnese = request.get_json()
        return jsonify({"status": "sucesso", "mensagem": "Anamnese salva com sucesso!"})
    return render_template('anamnese.html', clientes=BANCO_CLIENTES)


if __name__ == '__main__':
    app.run(debug=True)