from flask import Flask, render_template, request, jsonify
from chatbot_core import GeminiChatbot
import traceback

# IMPORTANT: Replace with a secure method in production
API_KEY = "AIzaSyCLbONUJS-ugWabNsJcorKJ-3tVHrCqCUM"

app = Flask(__name__)
chatbot = GeminiChatbot(API_KEY)

@app.route('/')
def index():
    """
    Render the main page
    """
    return render_template('index.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    """
    Handle chat interactions
    """
    if request.method == 'GET':
        return render_template('chat.html')
    
    try:
        # Text chat
        if 'message' in request.form:
            user_input = request.form['message']
            response = chatbot.process_text_chat(user_input)
            return jsonify({'response': response})
        
        # Image chat
        if 'image' in request.files:
            image_file = request.files['image']
            prompt = request.form.get('prompt', 'Describe this image in detail')
            
            # Convert image to base64 for preview
            base64_image = chatbot.convert_image_to_base64(image_file)
            
            # Analyze image
            response = chatbot.process_image_chat(image_file, prompt)
            
            return jsonify({
                'response': response, 
                'image': base64_image
            })
        
        return jsonify({'error': 'No valid input'}), 400

    except Exception as e:
        app.logger.error(f"Error processing chat: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)