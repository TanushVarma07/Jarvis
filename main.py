import os
import asyncio
import speech_recognition as sr
import edge_tts
import pygame

from dotenv import load_dotenv
from google import genai



load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise Exception("Gemini API key missing")


client = genai.Client(
    api_key=API_KEY
)

VOICE = "en-US-GuyNeural"

pygame.mixer.init()


async def generate_voice(text):

    file = "jarvis.mp3"


    communicate = edge_tts.Communicate(
        text,
        VOICE
    )


    await communicate.save(file)



    pygame.mixer.music.load(file)

    pygame.mixer.music.play()


    while pygame.mixer.music.get_busy():

        await asyncio.sleep(0.1)


    pygame.mixer.music.unload()

    os.remove(file)



def speak(text):

    print("\nJarvis:")
    print(text)


    text = text.replace("*","")
    text = text.replace("#","")


    asyncio.run(
        generate_voice(text)
    )


recognizer = sr.Recognizer()


def listen():

    with sr.Microphone() as source:

        print("\nListening...")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=1
        )


        audio = recognizer.listen(
            source
        )


    try:

        print("Recognizing...")


        command = recognizer.recognize_google(
            audio
        )


        print("You:", command)


        return command



    except:

        print(
            "Could not understand"
        )

        return ""


def ask_gemini(question):

    response = client.models.generate_content(

        model="gemini-2.5-flash",

        contents=question

    )


    return response.text


print("="*50)
print("🤖 JARVIS VOICE ASSISTANT ONLINE")
print("Say 'exit' to stop")
print("="*50)


speak(
    "Hello. I am Jarvis. How can I help you?"
)



while True:


    user_input = listen()



    if user_input.lower() in [
        "exit",
        "quit",
        "stop"
    ]:


        speak(
            "Thanks. Shutting down."
        )

        break



    if user_input:


        try:

            answer = ask_gemini(
                user_input
            )


            speak(answer)



        except Exception as e:


            print(e)


            speak(
                "Sorry. I found an error."
            )