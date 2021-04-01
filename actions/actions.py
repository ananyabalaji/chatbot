# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

import ssl
import wolframalpha
import wikipedia

# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []

# Wikipedia and Wolfram Alpha lookup
ssl._create_default_https_context = ssl._create_unverified_context
app_id = "VY9P3H-W4HA5HU8YU"
client = wolframalpha.Client(app_id) 

class ActionSearch(Action):

   def name(self) -> Text:
       return "action_search"

   def run(self, dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

       qry=(tracker.latest_message)['text']
       print(qry)
       output = ""

       res = client.query(qry)
       if res['@success'] == 'true':
         try:
           output = next(res.results).text
         except StopIteration:
           print("No results")
       # Wolfram was able to resolve question
       if output == "":
         print("Let's try wikipedia")
         try:
           output = wikipedia.summary(qry, sentences=1);
         except wikipedia.exceptions.DisambiguationError as e:
           print("Disambugiation error")
           output = "Unable to disambiguate. Could be " + " ".join(e.options[0:3])
         except wikipedia.exceptions.PageError as e:
           print("Page error")
           output =  "Unable to process request"
       print (output)
       dispatcher.utter_message(text=output)

       return []
