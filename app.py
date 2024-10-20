from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)

confirmados = set()  # Armazena os IDs das experiências confirmadas

def carregar_experiencias():
    """Carrega as experiências do arquivo CSV."""
    experiencias = []
    if os.path.exists('experiencias.csv'):
        with open('experiencias.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                experiencias.append(row)
    return experiencias

def salvar_experiencia(id, titulo, descricao, categoria, data, duracao, periodo, localizacao, curiosidades, preco, imagem):
    """Salva uma nova experiência no CSV."""
    with open('experiencias.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([id, titulo, descricao, categoria, data, duracao, periodo, localizacao, curiosidades, preco, imagem])

@app.route('/')
def index():
    """Página inicial que lista todas as experiências."""
    experiencias = carregar_experiencias()

    # Ordenar as experiências: confirmadas primeiro
    experiencias.sort(key=lambda e: e['ID'] not in confirmados)

    return render_template('index.html', experiencias=experiencias, confirmados=confirmados)

@app.route('/criar', methods=['GET', 'POST'])
def criar():
    """Página para criar uma nova experiência."""
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        categoria = request.form['categoria']
        data = request.form['data']
        duracao = request.form['duracao']
        periodo = request.form['periodo']
        localizacao = request.form['localizacao']
        curiosidades = request.form['curiosidades']
        preco = request.form['preco']
        imagem = request.form['imagem']

        experiencias = carregar_experiencias()
        id_experiencia = str(len(experiencias) + 1)

        salvar_experiencia(id_experiencia, titulo, descricao, categoria, data, duracao, periodo, localizacao, curiosidades, preco, imagem)
        return redirect(url_for('index'))

    return render_template('criar.html')

@app.route('/detalhes/<id_experiencia>', methods=['GET', 'POST'])
def detalhes(id_experiencia):
    """Página de detalhes de uma experiência, com opção de confirmação."""
    experiencias = carregar_experiencias()
    experiencia = next((e for e in experiencias if e['ID'] == id_experiencia), None)

    if not experiencia:
        return "Experiência não encontrada", 404

    if request.method == 'POST':
        # Ao invés de adicionar a experiência diretamente à lista de confirmados, redirecionar para a página de pagamento
        return redirect(url_for('pagamento', id_experiencia=id_experiencia))

    return render_template('detalhes.html', experiencia=experiencia)


@app.route('/pagamento/<id_experiencia>', methods=['GET', 'POST'])
def pagamento(id_experiencia):
    """Página de confirmação de pagamento para a experiência selecionada."""
    experiencias = carregar_experiencias()
    experiencia = next((e for e in experiencias if e['ID'] == id_experiencia), None)

    if not experiencia:
        return "Experiência não encontrada", 404

    if request.method == 'POST':
        # Confirmar a experiência adicionando o ID à lista 'confirmados'
        confirmados.add(id_experiencia)

        # Redirecionar para a página de agradecimento após o pagamento
        return redirect(url_for('agradecimento', id_experiencia=id_experiencia))

    return render_template('pagamento.html', experiencia=experiencia)


@app.route('/agradecimento/<id_experiencia>')
def agradecimento(id_experiencia):
    """Página de agradecimento após a confirmação do pagamento."""
    experiencias = carregar_experiencias()
    experiencia = next((e for e in experiencias if e['ID'] == id_experiencia), None)

    if not experiencia:
        return "Experiência não encontrada", 404

    return render_template('agradecimento.html', experiencia=experiencia)


if __name__ == '__main__':
    app.run(debug=True)