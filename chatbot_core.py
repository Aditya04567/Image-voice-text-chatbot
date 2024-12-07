import re
import google.generativeai as genai
import logging
import os
from PIL import Image
import io
import base64
import threading

# Configure logging
logging.basicConfig(level=logging.INFO)

class GeminiChatbot:
    def __init__(self, api_key):
        # Configure Gemini API
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self._stop_flag = threading.Event()  # Flag to stop ongoing processing

    def stop_processing(self):
        """
        Stop the current processing.
        """
        logging.info("Stopping current processing.")
        self._stop_flag.set()

    def reset_stop_flag(self):
        """
        Reset the stop flag for new input.
        """
        self._stop_flag.clear()

    def format_response(self, text, paragraph_marker="#PARAGRAPH#"):
        """
        Format chatbot response to include paragraph breaks and clean text.
        """
        try:
            # Remove asterisks (*)
            text = text.replace('*', '')

            # Replace custom paragraph markers with double line breaks (console output)
            text = text.replace(paragraph_marker, "\n\n")

            # Add indentation for numbered or bulleted lists
            text = re.sub(r'(?m)^(\d+)\.', r'\1.', text)  # Ensure numbered points have a period
            text = re.sub(r'(?m)^(-|\*) ', r'- ', text)  # Standardize unordered bullet points

            # Replace multiple spaces with a single space
            text = re.sub(r'\s+', ' ', text)

            # Strip leading and trailing spaces
            text = text.strip()

            return text
        except Exception as e:
            logging.error(f"Formatting error: {e}")
            return text  # Return the raw text in case of errors

    def process_text_chat(self, user_input):
        """
        Process text-based chat input and apply formatting.
        """
        try:
            # Stop any ongoing processing
            self.stop_processing()
            self.reset_stop_flag()  # Prepare for new input

            # Generate the raw response from the Gemini model
            raw_response = self.model.generate_content(user_input).text

            # Check for interrupt signal during response generation
            if self._stop_flag.is_set():
                logging.info("Processing interrupted.")
                return "Processing interrupted by new input."

            # Format the response
            formatted_response = self.format_response(raw_response)

            return formatted_response
        except Exception as e:
            logging.error(f"Chat processing error: {e}")
            return "Sorry, I encountered an error processing your message."

    def process_image_chat(self, image_file, prompt="Describe this image in detail"):
        """
        Process image-based chat input
        """
        try:
            # Stop any ongoing processing
            self.stop_processing()
            self.reset_stop_flag()  # Prepare for new input

            # Convert uploaded file to PIL Image
            img = Image.open(image_file)
            
            # Use Gemini Pro Vision model for image analysis
            model = genai.GenerativeModel("gemini-1.5-pro")
            response = model.generate_content([img, prompt])

            # Check for interrupt signal during response generation
            if self._stop_flag.is_set():
                logging.info("Processing interrupted.")
                return "Processing interrupted by new input."

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
def format_response(self, text, paragraph_marker="#PARAGRAPH#"):
    """
    Format chatbot response to include paragraph breaks and clean text.
    """
    try:
        # Remove asterisks (*)
        text = text.replace('*', '')

        # Replace custom paragraph markers with double line breaks
        text = text.replace(paragraph_marker, "\n\n")

        # Add indentation for numbered or bulleted lists
        text = re.sub(r'(?m)^(\d+\.)', r'\n\1', text)  # Numbered points on new lines
        text = re.sub(r'(?m)^(-|\*) ', r'  - ', text)  # Indent unordered bullet points

        # Replace multiple spaces with a single space
        text = re.sub(r'\s+', ' ', text)

        # Strip leading and trailing spaces
        text = text.strip()

        return text
    except Exception as e:
        logging.error(f"Formatting error: {e}")
        return text  # Return the raw text in case of errors