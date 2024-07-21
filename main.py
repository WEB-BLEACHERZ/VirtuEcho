import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import requests
import json
import time
import random

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    command = ""
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
    except Exception as e:
        print(f"Error: {str(e)}")
    return command

def get_weather():
    api_key = "9722b5942a0dd963e1e3d43b0fc6ef1e"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = "Salem"
    complete_url = base_url + "q=" + city_name + "&appid=" + api_key
    response = requests.get(complete_url)
    weather_data = response.json()
    if weather_data["cod"] != "404":
        main = weather_data["main"]
        weather_description = weather_data["weather"][0]["description"]
        temp = main["temp"]
        humidity = main["humidity"]
        weather_info = f"Temperature: {temp}, Humidity: {humidity}%, Description: {weather_description}"
        return weather_info
    else:
        return "City Not Found"

def get_news():
    api_key = "73730e80de5042438a5ff2c239d4aba7"
    base_url = "https://newsapi.org/v2/top-headlines?country=us&apiKey="
    complete_url = base_url + api_key
    response = requests.get(complete_url)
    news_data = response.json()
    headlines = [article['title'] for article in news_data['articles'][:5]]
    news_info = "Here are the top 5 news headlines: " + ", ".join(headlines)
    return news_info

reminders = []

def add_reminder(reminder):
    reminders.append(reminder)
    talk("Reminder added!")

def get_reminders():
    return "Here are your reminders: " + ", ".join(reminders)



def set_timer(duration):
    talk(f"Setting a timer for {duration} seconds")
    time.sleep(duration)
    talk("Time's up!")

def tell_fact():
    facts = [
        "Honey never spoils.",
        "A day on Venus is longer than a year on Venus.",
        "Bananas are berries, but strawberries are not.",
        "There are more stars in the universe than grains of sand on Earth."
    ]
    fact = random.choice(facts)
    return fact

def get_motivational_quote():
    quotes = [
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Success is not how high you have climbed, but how you make a positive difference to the world. - Roy T. Bennett",
        "Your time is limited, don’t waste it living someone else’s life. - Steve Jobs",
        "You miss 100% of the shots you don’t take. - Wayne Gretzky"
    ]
    quote = random.choice(quotes)
    return quote

def translate_text(text, language):
    url = "https://api.mymemory.translated.net/get"
    params = {"q": text, "langpair": f"en|{language}"}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        translation_data = response.json()
        translated_text = translation_data['responseData']['translatedText']
        return translated_text
    except requests.exceptions.RequestException as e:
        return f"Error fetching translation: {str(e)}"

def play_game():
    talk("Let's play a guessing game. I'm thinking of a number between 1 and 10.")
    number = random.randint(1, 10)
    guess = 5
    while guess != number:
        talk("Take a guess.")
        try:
            guess = int(take_command())
            if guess < number:
                talk("Higher!")
            elif guess > number:
                talk("Lower!")
        except ValueError:
            talk("Please guess a number.")
    talk(f"Congratulations! You guessed the number {number}.")

def run_alexa():
    command = take_command()
    print(command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
    elif 'who the heck is' in command:
        person = command.replace('who the heck is', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)
    elif 'date' in command:
        talk('sorry, I have a headache')
    elif 'are you single' in command:
        talk('I am in a relationship with wifi')
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'weather' in command:
        weather_info = get_weather()
        print(weather_info)
        talk(weather_info)
    elif 'news' in command:
        news_info = get_news()
        print(news_info)
        talk(news_info)
    elif 'add reminder' in command:
        reminder = command.replace('add reminder', '')
        add_reminder(reminder)
    elif 'reminders' in command:
        reminders_info = get_reminders()
        print(reminders_info)
        talk(reminders_info)
    
    elif 'set timer' in command:
        duration = int(command.replace('set timer for', '').strip())
        set_timer(duration)
    elif 'fact' in command:
        fact = tell_fact()
        print(fact)
        talk(fact)
    elif 'motivational quote' in command:
        motivational_quote = get_motivational_quote()
        print(motivational_quote)
        talk(motivational_quote)
    elif 'translate' in command:
        talk("What should I translate?")
        text = take_command()
        talk("Which language?")
        language = take_command()
        translation = translate_text(text, language)
        print(translation)
        talk(translation)
    elif ' game' in command:
        play_game()
    else:
        talk('Please say the command again.')

while True:
    run_alexa()
