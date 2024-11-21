import google.generativeai as genai
import logging
import os
from PIL import Image
import io
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)

class GeminiChatbot:
    def __init__(self, api_key):
        # Configure Gemini API
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def process_text_chat(self, user_input):
        """
        Process text-based chat input
        """
        try:
            response = self.model.generate_content(user_input).text
            return response
        except Exception as e:
            logging.error(f"Chat generation error: {e}")
            return "Sorry, I encountered an error processing your message."

    def process_image_chat(self, image_file, prompt="Describe this image in detail"):
        """
        Process image-based chat input
        """
        try:
            # Convert uploaded file to PIL Image
            img = Image.open(image_file)
            
            # Use Gemini Pro Vision model for image analysis
            model = genai.GenerativeModel("gemini-1.5-pro")
            response = model.generate_content([img, prompt])
            return response.text
        except Exception as e:
            logging.error(f"Image analysis error: {e}")
            return "Sorry, I couldn't analyze the image."

    @staticmethod
    def convert_image_to_base64(image_file):
        """
        Convert image to base64 for displaying in HTML
        """
        try:
            img = Image.open(image_file)
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            return base64.b64encode(buffered.getvalue()).decode('utf-8')
        except Exception as e:
            logging.error(f"Image conversion error: {e}")
            return None