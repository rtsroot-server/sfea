from flask import Flask, render_template, request, jsonify
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

# =======================================================
# ⚙️ CONFIGURAÇÕES DE E-MAIL
# =======================================================
EMAIL_REMETENTE = 'cliente.sfestetica@gmail.com'       
SENHA_APP = 'kelc zkjx thjs loke'
EMAIL_CLINICA = 'cliente.sfestetica@gmail.com'         

# Memória Temporária do Sistema
BANCO_CLIENTES = []

def calcular_idade_fallback(data_str):
    if not data_str: return 0
    try:
        data_nasc = datetime.strptime(data_str, '%Y-%m-%d')
        hoje = datetime.today()
        idade = hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
        return idade if idade > 0 else 0
    except Exception:
        return 0

# --- MOTOR DE ENVIO DE E-MAILS ---
def disparar_email(assunto, destinatario_aluno, texto_html):
    if SENHA_APP == 'COLE_AQUI_AS_16_LETRAS' or not destinatario_aluno:
        print("E-mail não configurado ou cliente sem e-mail.")
        return
    
    try:
        msg = MIMEMultipart()
        msg['From'] = f"Suzane Figueiredo Estética Avançada <{EMAIL_REMETENTE}>"
        msg['To'] = destinatario_aluno
        msg['Cc'] = EMAIL_CLINICA
        msg['Subject'] = assunto

        # Assinatura padronizada no e-mail
        assinatura = """
        <br><br>
        <hr style='border: none; border-top: 1px solid #D4B06A; width: 200px; margin-left: 0;'>
        <p style='color: #888; font-family: Arial; font-size: 12px;'>
        <b>Suzane Figueiredo Estética Avançada</b><br>
        Estrada Coronel Pedro Correa 740, loja 116<br>
        Barra Olímpica - Rio de Janeiro/RJ<br>
        </p>
        """
        
        msg.attach(MIMEText(texto_html + assinatura, 'html'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_REMETENTE, SENHA_APP.replace(" ", "")) # Remove os espaços caso tenha copiado assim
        
        # Envia para o Aluno e para a Clínica (Cópia)
        destinatarios = [destinatario_aluno, EMAIL_CLINICA]
        server.sendmail(EMAIL_REMETENTE, destinatarios, msg.as_string())
        server.quit()
        print(f"E-mail enviado com sucesso para {destinatario_aluno}")
    except Exception as e:
        print(f"Erro ao enviar email: {e}")


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dados', methods=['GET', 'POST'])
def dados():
    if request.method == 'POST':
        dados_cliente = request.get_json()
        BANCO_CLIENTES.append(dados_cliente)
        
        # DISPARA E-MAIL DE CADASTRO
        nome = dados_cliente.get('nome', 'Aluno')
        email = dados_cliente.get('email', '')
        corpo_email = f"<h2>Olá, {nome}!</h2><p>O seu registo na <b>Suzane Figueiredo Estética Avançada</b> foi concluído com sucesso. Seja muito bem-vindo(a)!</p>"
        disparar_email("Confirmação de Cadastro - Suzane Figueiredo", email, corpo_email)
        
        return jsonify({"status": "sucesso"})
    return render_template('dados.html')

@app.route('/contrato')
def contrato():
    return render_template('contrato.html', clientes=BANCO_CLIENTES)

@app.route('/salvar_contrato', methods=['POST'])
def salvar_contrato():
    dados = request.get_json()
    
    # DISPARA E-MAIL DE CONTRATO
    nome = dados.get('nome', 'Aluno')
    email = dados.get('email', '')
    corpo_email = f"<h2>Olá, {nome}!</h2><p>O seu <b>Contrato de Prestação de Serviços</b> e a sua <b>Autorização de Uso de Imagem</b> foram assinados digitalmente e recebidos com sucesso pela nossa equipa.</p>"
    disparar_email("Documentos Assinados - Suzane Figueiredo", email, corpo_email)
    
    return jsonify({"status": "sucesso"})

@app.route('/anamnese', methods=['GET', 'POST'])
def anamnese():
    if request.method == 'POST':
        dados_anamnese = request.get_json()
        
        # DISPARA E-MAIL DE ANAMNESE
        nome = dados_anamnese.get('nome', 'Aluno')
        email = dados_anamnese.get('email', '')
        corpo_email = f"<h2>Ficha de Anamnese Recebida</h2><p>A ficha de avaliação e anamnese do paciente <b>{nome}</b> foi guardada de forma segura no nosso sistema.</p>"
        disparar_email("Anamnese Registada - Suzane Figueiredo", email, corpo_email)
        
        return jsonify({"status": "sucesso", "mensagem": "Anamnese salva com sucesso!"})
    return render_template('anamnese.html', clientes=BANCO_CLIENTES)

@app.route('/protocolos')
def protocolos():
    return render_template('protocolos.html')

@app.route('/formulario_shape')
def formulario_shape():
    clientes_processados = []
    for c in BANCO_CLIENTES:
        cliente_copy = dict(c)
        idade_digitada = cliente_copy.get('idade')
        try:
            cliente_copy['idade_calculada'] = int(idade_digitada)
        except:
            data_nasc = cliente_copy.get('data_nascimento', '')
            cliente_copy['idade_calculada'] = calcular_idade_fallback(data_nasc)
        clientes_processados.append(cliente_copy)
        
    return render_template('formulario_shape.html', clientes=clientes_processados)

@app.route('/salvar_shape', methods=['POST'])
def salvar_shape():
    dados = request.get_json()
    
    # DISPARA E-MAIL DE ACOMPANHAMENTO SHAPE
    nome = dados.get('nome', 'Aluno')
    email = dados.get('email', '')
    corpo_email = f"<h2>Acompanhamento Shape Space</h2><p>O quadro de resultados e a evolução das sessões do paciente <b>{nome}</b> foram atualizados no sistema da clínica.</p>"
    disparar_email("Acompanhamento Atualizado - Suzane Figueiredo", email, corpo_email)
    
    return jsonify({"status": "sucesso"})

if __name__ == '__main__':
    app.run(debug=True)