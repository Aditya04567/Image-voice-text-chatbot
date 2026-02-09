import google.generativeai as genai
import sys
import argparse
import shlex
import datetime
import speech_recognition as sr
import pyttsx3
import os
from PIL import Image
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[logging.FileHandler('chatbot.log'), logging.StreamHandler(sys.stdout)]
)

# API Configuration (IMPORTANT: Replace with secure method in production)
API_KEY = "your api key"


class GeminiChatbot:
    def __init__(self):
        # Initialize recognizer and text-to-speech engine
        self.recognizer = sr.Recognizer()
        self.speech_engine = pyttsx3.init()

        # Configure Gemini API
        genai.configure(api_key=API_KEY)

    @staticmethod
    def parse_arguments():
        """
        Parse command-line arguments with robust handling
        """
        parser = argparse.ArgumentParser(
            description="Gemini AI Chatbot with Multi-Modal Input",
            epilog="Support for text, voice, and image-based interactions"
        )

        # Input method arguments
        parser.add_argument("--text", action='store_true', help="Enable text-based input")
        parser.add_argument("--voice", action='store_true', help="Enable voice-based input")
        parser.add_argument("--image", type=GeminiChatbot.validate_image_path, help="Path to image file for analysis")

        # Additional configuration arguments
        parser.add_argument("--prompt", nargs='*', default=["Describe this image in detail"],
                            help="Custom prompt for image analysis")
        parser.add_argument("--speak", action='store_true', help="Enable text-to-speech output")
        parser.add_argument("--log", action='store_true', help="Enable detailed logging")

        args = parser.parse_args(shlex.split(' '.join(sys.argv[1:])))
        args.prompt = ' '.join(args.prompt) if isinstance(args.prompt, list) else args.prompt
        return args

    @staticmethod
    def validate_image_path(path):
        """
        Validate and normalize image file path
        """
        if not os.path.exists(path):
            raise argparse.ArgumentTypeError(f"Image file not found: {path}")
        try:
            Image.open(path)
            return os.path.normpath(path)
        except Exception:
            raise argparse.ArgumentTypeError(f"Invalid image file: {path}")

    def text_input(self):
        """
        Handle text-based input
        """
        try:
            return input("You: ").strip()
        except Exception as e:
            logging.error(f"Text input error: {e}")
            return None

    def voice_input(self):
        """
        Handle voice-based input using speech recognition
        """
        try:
            print("Speak now... (listening)")
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                user_input = self.recognizer.recognize_google(audio).lower()
                print(f"Recognized: {user_input}")
                return user_input
        except sr.UnknownValueError:
            logging.warning("Could not understand audio")
        except sr.RequestError as e:
            logging.error(f"Speech recognition error: {e}")
        except Exception as e:
            logging.error(f"Unexpected voice input error: {e}")
        return None

    def image_analysis(self, image_path, prompt, speak=False):
        """
        Analyze image using Gemini API and optionally speak the output.
        """
        try:
            img = Image.open(image_path)
            model = genai.GenerativeModel("gemini-1.5-pro")

            # Generate response
            response = model.generate_content([img, prompt])
            response_text = response.text

            # Output response
            print("Image Analysis: ", response_text)

            # Speak response if enabled
            if speak:
                sanitized_response = response_text.replace("*", "")
                self.text_to_speech(sanitized_response)

            return response_text
        except Exception as e:
            logging.error(f"Image analysis error: {e}")
            return None

    def text_to_speech(self, text):
        """
        Convert text to speech, ignoring asterisks.
        """
        try:
            sanitized_text = text.replace("*", "")
            self.speech_engine.say(sanitized_text)
            self.speech_engine.runAndWait()
        except Exception as e:
            logging.error(f"Text-to-speech error: {e}")

    def log_interaction(self, input_type, user_input, response):
        """
        Log interactions to file
        """
        try:
            log_dir = os.path.join(os.getcwd(), 'logs')
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, f"chat_{datetime.date.today()}.log")
            with open(log_file, 'a', encoding='utf-8') as f:
                log_entry = (
                    f"[{datetime.datetime.now()}]\n"
                    f"Input Type: {input_type}\n"
                    f"User Input: {user_input}\n"
                    f"Response: {response}\n\n"
                )
                f.write(log_entry)
        except Exception as e:
            logging.error(f"Logging error: {e}")

    def chat(self, args):
        """
        Main chat logic
        """
        try:
            if args.image:
                response = self.image_analysis(args.image, args.prompt, speak=args.speak)
                if response and args.log:
                    self.log_interaction('image', args.image, response)
                return

            while True:
                user_input = self.text_input() if args.text else self.voice_input()
                if not user_input or user_input.lower() in ['quit', 'exit', 'bye']:
                    break

                try:
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(user_input).text
                    print("Chatbot: ", response)

                    if args.speak:
                        sanitized_response = response.replace("*", "")
                        self.text_to_speech(sanitized_response)

                    if args.log:
                        self.log_interaction('text' if args.text else 'voice', user_input, response)
                except Exception as e:
                    logging.error(f"Chat generation error: {e}")
                    break

        except Exception as e:
            logging.error(f"Unexpected chat error: {e}")

def main():
    """
    Main application entry point
    """
    try:
        chatbot = GeminiChatbot()
        args = chatbot.parse_arguments()
        chatbot.chat(args)
    except KeyboardInterrupt:
        print("\nChat terminated by user.")
    except Exception as e:
        logging.error(f"Application error: {e}")

if __name__ == "__main__":
    main()
