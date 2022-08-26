from distutils.cmd import Command
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from importlib.resources import contents
import webbrowser
from cv2 import log
from numpy import take
import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
import requests
from requests import get
import wikipedia
import pywhatkit as kit
import smtplib
import sys
import pyjokes
import pyautogui
import time
import instaloader
import PyPDF2


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

engine.setProperty('voices', voices[0].id)

# Functions =>
# text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

# to convert voice into text
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        r.pause_threshold = 1
        audio = r.listen(source, phrase_time_limit=5)

    try:
        print('Recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")

    except Exception as e:
        speak('Say that again please....')
        return 'none'
    return query

# greetings
def wishMe():
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour <= 12:
        speak('Good Morning')
    elif hour > 12 and hour < 18:
        speak('Good Afternoon')
    else:
        speak('Good Evening')
    speak('I am jarvis. please tell me how can i help you')

# to send email
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your email id', 'your password')
    server.sendmail('your email id', to, content)
    server.close()


def news():
    main_url = 'http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=ba1c0213e9e44576bc484917a2df0030'

    main_page = requests.get(main_url).json()

    articles = main_page['articles']

    head = []
    day = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth']
    for ar in articles:
        head.append(ar['title'])
    for i in range (len(day)):
        speak(f'today {day[i]} news is: {head[i]}')


def pdf_reader():
    book = open('bookname.pdf', 'rb')           # open pdf in binary mode
    pdfReader = PyPDF2.PdfFileReader(book)
    pages = pdfReader.numPages
    speak(f'Total numbers of pages in this book {pages}')
    speak(f'Sir, please enter the page number i have to read')
    pg = int(input('please enter the page number: '));
    page = pdfReader.getPage(pg)
    text = page.extractText()
    speak(text)
    # jarvis book reading speed can be controlled b user



# Main function
if __name__ == '__main__':
    wishMe()
    while True:

        query = takeCommand().lower()

        # Logic
        if 'open notepad' in query:
            npath = 'C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Accessories'
            os.startfile(npath)
        
        elif 'open abobe reader' in query:
            apath = 'C:\\Program Files (x86)\\Adobe\\Acrobat Reader DC\\Reader\\AcroRd32.exe'
            os.startfile(apath)

        elif 'open command prompt' in query:
            os.system('start cmd')

        elif 'open camera' in query:
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow('webcam', img)
                k = cv2.waitKey(50)
                if k==27:
                    break
            cap.release()
            cv2.destroyAllWindows()

        elif 'ip address' in query:
            ip = get('https://api.ipify.org').text
            speak(f'your IP address is {ip}')

        elif 'wikipedia' in query:          #error
            speak(f'Searching wikipedia....')
            query = query.replace('wikipedia', '')
            results = wikipedia.summary(query, sentence=2)
            speak("According to wikipedia")
            speak(results)
            print(results)

        elif 'open youtube' in query:
            webbrowser.open('www.youtube.com')

        elif 'open instagram' in query:
            webbrowser.open('www.instagram.com/login')

        elif 'open stack overflow' in query:
            webbrowser.open('www.stackoverflow.com')

        elif 'open google' in query:
            speak('Sir, what should i search on google')
            cm = takeCommand().lower()
            webbrowser.open(f'{cm}')

        elif 'play songs on youtube' in query:
            kit.playonyt('see you again')


        # To close jarvis
        elif 'you can sleep' in query:
            speak('Thanks for using me sir, have a good day')
            sys.exit()


        # to close any application (Ex. Notepad)
        elif 'close notepad' in query:
            speak('Okay sir, closing notepad')
            os.system('taskkill /f /im notepad.exe')

        # to tell joke
        elif 'tell me a joke' in query:
            joke = pyjokes.get_joke()
            speak(joke)

        elif 'shut down the pc' in query:
            os.system('shutdown /s /t S')

        elif 'restart the pc' in query:
            os.system('shutdown /r /t S')



        elif 'switch the window'in query:
            pyautogui.keyDown('alt')
            pyautogui.press('tab')
            time.sleep(1)
            pyautogui.keyUp('alt')

        elif 'tell me news' in query:
            speak('Please wait sir, fetching the latest news for you....')
            news()


        elif 'email to someone' in query:
            
            speak('Sir what should i send')
            query = takeCommand().lower()
            if 'send a file' in query:
                email = 'your@gmail.com'        # your email
                password = 'your_pass'          # your password
                send_to_email = 'person@gmail.com'  # whom you are sending mail to
                speak('Okay sir, what is the subject for this email')
                query = takeCommand().lower()
                subject = query
                speak('and sir, what is the message for this email')
                query2 = takeCommand().lower()
                message = query2
                speak('Sir, please enter the correct path of the file into the terminal')
                file_location = input('Please enter the file path here')

                speak('Please wait, I am sending the email now....')

                msg = MIMEMultipart()
                msg['From'] = email
                msg['To'] = send_to_email
                msg['Subject'] = subject

                msg.attach(MIMEText(message, 'plain'))

                # Setup the attachment
                filename = os.path.basename(file_location)
                attachment = open(file_location, 'rb')
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filenae= %s' % filename)

                # Attach the attachment to the MIMEMultipart object
                msg.attach(part)

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(email, password)
                text = msg.as_string()
                server.sendmail(email, send_to_email, text)
                server.quit()
                speak('email has been sent to (name_here)')
            
            else:
                email = 'your@gmail.com'
                password = 'your_pass'
                send_to_email = 'person@gmail.com'
                message = query

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(email, password)
                server.sendmail(email, send_to_email, message)
                server.quit()
                speak('Email has been sent to (name_here)')




        # To find location using IP address
        elif 'where i am' in query or 'where we are' in query:
            speak('wait sir, let me check')
            try:
                ipAdd = requests.get('https://api.ipify.org').text
                print(ipAdd)
                url = 'https://get.geojs.io/v1/ip/geo/' + ipAdd + '.json'
                geo_requests = requests.get(url)
                geo_data = geo_requests.json()

                city = geo_data['city']
                country = geo_data['country']
                speak(f"Sir i am not sure, but i think we are in {city} city of {country} country")
            
            except Exception as e:
                speak("Sorry sir, due to network issue i am not able to find where we arfe curently.")
                pass



        
        # To check Instagram profile
        elif 'instagram profile' in query or 'profile on instagram' in query:       #error
            speak("Sir please enter the user name correctly.")
            name = input("Enter username here: ")
            webbrowser.open("www.instagram.com/{name}")
            speak(f"Sir here is the profile of the user {name}")
            time.sleep(5)
            speak("Sir would you like to download profile picture of this account")
            condition = takeCommand().lower()
            if 'yes' in condition:
                mod = instaloader.Instaloader()
                mod.download_profile(name, profiile_pic_only=True)
                speak("I am done Sir, profile picture is saved in our main folder, now i am ready for the next command")
            else:
                pass


        
        # To take screenshot
        elif 'take screenshot' in query or 'take a screenshot' in query:
            speak("Sir, please tell me the name for this screenshot file")
            name = takeCommand().lower()
            speak("Please sir hold the screen for few seconds, i am taking the screenshot")
            time.sleep(3)
            img = pyautogui.screenshot()
            img.save(f"{name}.png")
            speak("I am done sir, the screenshot is saved in our main folder, now i am ready for the next command")

        

        # To read pdf
        elif 'read pdf' in query:
            pdf_reader()

        

        # To hide files and folders
        elif 'hide all files' in query or 'hide this folder' in query or 'visible for everyone' in query:
            speak('sir please tell me you want to hide this folder or make it visible again for everyone')
            condition = takeCommand().lower()
            if 'hide' in condition:
                os.system('attrib +h /s /d')
                speak('sir, all the the files in this folders are now hidden.')

            elif 'visible' in condition:
                os.system('atrrib -h /s /d')
                speak('sir, all the the files in this folders are now hidden.')

            elif 'leave it' in condition or 'leave for now' in condition:
                speak('Ok sir')




        speak('Sir, do you have any other workfor me?')


















    

# Features =>
# (1)  Open Notepad
# (2)  Open Adobe PDF Reader 
# (3)  Open Command Promopt 
# (4)  Open Camera 
# (5)  IP ADDRESS 
# (6)  Search Wikipedia 
# (7)  Open Youtube
# (8)  Open Instagram
# (9)  Open Twitter
# (10) Open Stackoverflow
# (11) Open Whatsapp and send message 
# (12) Open Google and Search 
# (13) Play songs on Youtube
# (14) Close any opened Application 
# (15) Exit Jarvis Program 
# (16) Tell a joke 
# (17) Shutdown PC 
# (18) Restart PC 
# (19) Switch tabs 
# (20) Email to Anyone 
# (21) Tell News 
# (22) Find location using IP Address 
# (23) Check Instagram Profile 
# (24) Take a Screenshot
# (25) Read PDF  (Audiobook)
# (26) Hide Files and Folders