from flask import Flask, render_template, request, session, jsonify, url_for
import os
import secrets
from lyzr import QABot

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

os.environ['OPENAI_API_KEY'] = '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'

# Create the uploads directory if it doesn't exist
os.makedirs('uploads', exist_ok=True)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' in request.files:
        file = request.files['file']
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        session['file_path'] = file_path
        session['index_name'] = generate_index_name()  # Generate a unique index name
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'No file uploaded'})


@app.route('/ask', methods=['POST'])
def ask():
    question = request.form['question']
    file_path = session['file_path']
    index_name = session['index_name']
    vector_store_params = {
        "vector_store_type": "WeaviateVectorStore",
        "index_name": index_name
    }
    qa_bot = QABot.pdf_qa(
        input_files=[file_path],
        vector_store_params=vector_store_params
    )
    response = qa_bot.query(question)
    sources = [source.text for source in response.source_nodes]
    return jsonify({'response': response.response, 'sources': sources})


@app.route('/clear', methods=['POST'])
def clear():
    file_path = session.get('file_path')
    if file_path and os.path.exists(file_path):
        os.remove(file_path)
    session.clear()
    return jsonify({'success': True})


def generate_index_name():
    # Generate a unique index name starting with a capital letter
    return "Index" + secrets.token_hex(4).capitalize()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
