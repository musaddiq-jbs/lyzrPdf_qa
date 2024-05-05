# Building a PDF Question Answering App with Lyzr and Flask

## Introduction:
In the era of information overload, finding relevant information from lengthy PDF documents can be a daunting task. Imagine having a powerful tool that allows you to upload a PDF file and ask questions related to its content, getting accurate answers in seconds. In this blog post, we'll explore how to build a PDF Question Answering (QA) app using Lyzr, a state-of-the-art AI platform, and Flask, a popular Python web framework.

## Step 1: Setting up the Environment
To get started, make sure you have Python and Flask installed on your system. You can install Flask using pip:

```bash
pip install flask
```

Next, install the Lyzr library and pdfminer by running:

```bash
pip install lyzr pdfminer.six
```

## Step 2: Building the Flask Application
Create a new Python file, e.g., `app.py`, and set up the Flask application:

```python
from flask import Flask, render_template, request, session, jsonify
import os
import secrets
from lyzr import QABot

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

os.makedirs('uploads', exist_ok=True)
```

In this code snippet, we import the necessary modules, create a Flask app instance, set a secret key for session handling, and create an `uploads` directory to store the uploaded PDF files.

## Step 3: Implementing the File Upload Functionality
Next, let's add the functionality to handle file uploads:

```python
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' in request.files:
        file = request.files['file']
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        session['file_path'] = file_path
        session['index_name'] = generate_index_name()
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'No file uploaded'})
```

This code defines the `/upload` endpoint that accepts a POST request with a PDF file. It saves the uploaded file to the `uploads` directory and stores the file path and a unique index name in the session.

## Step 4: Implementing the Question Answering Functionality
Now, let's add the core functionality of the app — answering questions based on the uploaded PDF:

```python
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
```

This code defines the `/ask` endpoint that accepts a POST request with a question. It retrieves the file path and index name from the session, initializes the Lyzr QABot with the uploaded PDF, and queries the bot with the provided question. The response and sources are then returned as JSON.

## Step 5: Adding a Clear Functionality
To allow users to clear the uploaded PDF and start fresh, let's add a `/clear` endpoint:

```python
@app.route('/clear', methods=['POST'])
def clear():
    file_path = session.get('file_path')
    if file_path and os.path.exists(file_path):
        os.remove(file_path)
    session.clear()
    return jsonify({'success': True})
```

This code removes the uploaded PDF file and clears the session data.

## Step 6: Creating the HTML Template
Create an HTML template file, e.g., `index.html`, to provide a user-friendly interface for uploading PDFs and asking questions. You can use HTML, CSS, and JavaScript to design an intuitive and visually appealing interface.

## Step 7: Running the Application
Finally, run the Flask application:

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
```

You can now access the PDF QA app by visiting `http://localhost:5000` in your web browser.

## Live Sample Project
To see a live demonstration of the PDF Question Answering app, you can visit the following URL: [http://172.105.252.48/](http://172.105.252.48/)

## Conclusion
In this blog post, we explored how to build a powerful PDF Question Answering app using Lyzr and Flask. By leveraging Lyzr's advanced AI capabilities and Flask's simplicity, we created an intuitive tool that allows users to upload PDF documents, ask questions, and receive accurate answers in seconds.

We covered the step-by-step process of setting up the environment, creating the Flask application, implementing key functionalities, and running the application. The app demonstrates the potential of AI-driven question answering in various domains, from research and academia to business and legal fields.

To experience the app firsthand, be sure to check out the live sample project hosted at [http://172.105.252.48/](http://172.105.252.48/). It provides a real-world example of how the app functions and allows you to interact with it directly.

By harnessing the power of Lyzr and Flask, you can unlock valuable insights from PDF documents and make them more accessible than ever before. So why not give it a try and see how it can enhance your work with PDF files? Start building your own PDF Question Answering app today and revolutionize the way you interact with documents!
