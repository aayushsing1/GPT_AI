from flask import Flask, render_template, request
from g4f.client import Client
from googletrans import Translator, LANGUAGES

app = Flask(__name__)

client = Client()
translator = Translator()

@app.route('/', methods=['GET', 'POST'])
def index():
    generated_response = None
    if request.method == 'POST':
        content = request.form.get('content')
        
        if content:
            try:
                # Generate response from AI
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": content}],
                )
                generated_response = response.choices[0].message.content.strip()
                
                # Check if the generated response is in Chinese
                detected_language = translator.detect(generated_response).lang
                if detected_language == 'zh-cn' or detected_language == 'zh-tw':  # Simplified or Traditional Chinese
                    # Translate the response to English
                    generated_response = translator.translate(generated_response, src='zh', dest='en').text
            
            except Exception as e:
                generated_response = f"Error: {str(e)}"
        
        return generated_response

    return render_template('chatai.html')  # Render your main HTML page


@app.route('/generate_gpt', methods=['GET', 'POST'])
def generate_gpt():

    generated_response = None
    if request.method == 'POST':
        content = request.form.get('content')
        
        if content:
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": content}],
                )
                generated_response = response.choices[0].message.content
            except Exception as e:
                generated_response = f"Error: {str(e)}"
        
        return generated_response

    return render_template('gpt4.html')  # Render your main HTML page


if __name__ == '__main__':
    app.run(debug=True)
