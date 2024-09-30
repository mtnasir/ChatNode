#!/usr/bin/env python3
# chatnode.py

# Copyright (c) 2024 mtnasir
# Email: eng.m.naser@gmail.com
#
# This file is part of ChatNode.
#
# ChatNode is free software: you can redistribute it and/or modify
# it under the terms of the MIT License as published by
# the Massachusetts Institute of Technology. See the LICENSE file for details.

import re
import speech_recognition as sr
import pyttsx3
import json
import openai
import os
import speech_recognition as sr
# import winsound  # Import winsound or a similar library for non-Windows systems
from openai import OpenAI
import sys
# Get the API key from the environment variable
openai_api_key = os.getenv('OPENAI_API_KEY')


class ChatNode:
    def __init__(self, gaol, status,role,messages,output_json_formate):
        self.__gaol = gaol
        self.__status = status
        self.__role = role
        self.__messages = messages
        self.__output_json_formate=output_json_formate
        self.recognizer = sr.Recognizer()
        self.client = OpenAI(
                # This is the default and can be omitted
                api_key=openai_api_key,
            )
    
    def beep(self,frequency, duration):
        os.system(f'play -nq -t alsa synth {duration / 1000} sine {frequency}')

    def record_and_transcribe(self):
        recognizer=self.recognizer
        # Use default microphone as the audio source
        with sr.Microphone() as source:
            print("Listening...")

            # Adjust for ambient noise with a shorter duration
            recognizer.adjust_for_ambient_noise(source)

            # Beep to signal the start of recording
            self.beep(500, 200)  # Reduce beep duration to 200 ms

            # Record the audio with a timeout and phrase limit
            audio = recognizer.listen(source, timeout=5)


            print("Transcribing...")

            try:
                # Use Google Speech Recognition to transcribe the audio
                text = recognizer.recognize_google(audio)
                print("You said:", text)
                return text
            except sr.UnknownValueError:
                print("Sorry, could not understand audio.")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
    
    def SpeakText(self,command):
        # Initialize the engine
        engine = pyttsx3.init()

        # Set properties for clearer speech
        rate = engine.getProperty('rate')   # Get the current speaking rate
        engine.setProperty('rate', rate - 50)  # Slow down the speech (default rate is around 200 words per minute)

        volume = engine.getProperty('volume')  # Get the current volume level
        engine.setProperty('volume', 1.0)  # Set volume level between 0.0 and 1.0

        engine.say(command)
        engine.runAndWait()


    def checker(self):
       
        client=  self.client 
        prompt = (
            f"""check if the customer request is confirmed and the conversation goal is achieved: 
            the goal is: {self.__gaol} and the conversation is: {self.__messages}
            \n\n respond in JSON format {self.__status}"""
        )
        
        rrole = [
            {"role": "system", "content": self.__role},
            {"role": "user", "content": prompt},
        ]
        
        chat_completion = client.chat.completions.create(
            messages=rrole,
            model="gpt-4o",
        )
        
        model_response0 = chat_completion.choices[0].message.content
        self.__messages.append({"role": "assistant", "content": model_response0})
        # Regular expression to find the JSON object
        json_pattern = re.compile(r'\{.*?\}', re.DOTALL)
        
        # Find the first match in the string
        model_response2 = json_pattern.findall(model_response0)
        
        if model_response2:
            # Extract the first match (assumed to be the JSON string)
            model_response2 = model_response2[0].strip('```json\n').strip('```')
            
            try:
                # Parse the JSON string
                json_response = json.loads(model_response2)
                # print("Parsed JSON response:", json_response)
                return json_response['done'],rrole
           
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON: {e}")
                return "false",rrole
        else:
            print("No JSON data found in the model response.")
            return "false",rrole


    def summariser(self):
        client=  self.client 
        message = ". summarise the customer request during the prevous conversation in a senstece with 20 words"
        self.__messages.append(
            {"role": "user", "content": message},
        )
        chat_completion = client.chat.completions.create(
        messages=self.__messages,
        model="gpt-4o",
            )
        summary = chat_completion.choices[0].message.content
        self.__messages.append({"role": "assistant", "content": summary})

        #####
        message = f"summarise the customer request during the prevous conversation in json formate {self.__output_json_formate}"
        self.__messages.append(
            {"role": "user", "content": message},
        )
        chat_completion = client.chat.completions.create(
        messages=self.__messages,
        model="gpt-4o",
            )
            
        jsondata = chat_completion.choices[0].message.content
        # Regular expression to find the JSON object
        json_pattern = re.compile(r'\{.*?\}', re.DOTALL)
        
        # Find the first match in the string
        model_response2 = json_pattern.findall(jsondata)
        
        # Extract the first match (assumed to be the JSON string)
        json_out = model_response2[0].strip('```json\n').strip('```')
        self.__messages.append({"role": "assistant", "content": jsondata})

        return summary, json_out
    
    def endconv(self):
        message = f"tell the customer that the call is ened in a polite way. "
        self.__messages.append(
            {"role": "user", "content": message},
        )
        client= self.client 
        
        chat_completion = client.chat.completions.create(
            messages=self.__messages,
            model="gpt-4o",
        )
        reply = chat_completion.choices[0].message.content
        self.__messages.append({"role": "assistant", "content": reply})
        self.SpeakText(reply)
        sys.exit()

    def main(self):
       
       
        
        client= self.client 
        while True:
            chat_completion = client.chat.completions.create(
                messages=self.__messages,
                model="gpt-4o",
            )
            reply = chat_completion.choices[0].message.content
            self.__messages.append({"role": "assistant", "content": reply})
            self.SpeakText(reply)
            import json


            # MyText=self.record_and_transcribe()
            attempt = 0
            max_attempts = 3  # Number of times to retry
            
            while attempt < max_attempts:
                try:
                    MyText = self.record_and_transcribe()
                    MyText="the custormer said: "+MyText+". respond to the customer in 30 words."

                    break  # If successful, break out of the loop
                except Exception as e:
                    attempt += 1
                    print(f"Error occurred: {e}")
                    if attempt < max_attempts:
                        print(f"Retrying... (Attempt {attempt + 1}/{max_attempts})")
                    else:
                        print("Max attempts reached. Exiting.")
                        self.endconv()

            # MyText="the custormer said: "+MyText+". respond to the customer in 30 words."
            message = MyText
            self.__messages.append(
                {"role": "user", "content": message},
            )
            
            # Convert the list of dictionaries to a JSON string
            json_string = json.dumps(self.__messages, indent=2)


            # Convert the dictionary to a JSON string
            messages_str = json.dumps(self.__messages)
            # print(messages_str)
            results,conv=self.checker()

            if results=="true":
                # print("done with the data")
                summary, json_out=self.summariser()
                print(summary)
                # print(json_out)
                return results,summary, json_out, self.__messages
            else:
                if results=="nan":
                    print("end")
                    return results,"nan", "nan", self.__messages
                    
                else:
                    print("not finshed, need more details")
                    return results,"false", "nan", self.__messages


