# from __future__ import print_function, unicode_literal
from django.shortcuts import render

# Create your views here.

import json, requests, random, re
from pprint import pprint

from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#TEXTBLOB
from textblob import TextBlob
# from . import config
# from config import FILTER_WORDS

PAGE_ACCESS_TOKEN = "EAAC7hsC2C0sBAOdnesyZAKMZAhRZC9EvVxW9j1RscX7TZByH2ZA9WFnUyqmy9ywvBXZBVHq9Nvu9SZBk6vfutctQuvhqcSIQ6IMyrPbcBDvj5gQzOSIl01JS2FnKEA4ylbP35pNedZBkHIGFKO9d0nZBVaA37W6CHyqYFRtD96EZBLAwZDZD"
VERIFY_TOKEN = "2318934571"






    
    # Remove all punctuations, lower case the text and split it based on space
# def check_for_greetings(recieved_message):

#     user_message = TextBlob(recieved_message)

#     flag = "greeting_message"
#     for word in user_message.words:
#         if word.lower() in GREETING_KEYWORDS:
#             return random.choice(GREETING_RESPONSES)


# def respond(recieved_message):

#   user_message = TextBlob(recieved_message)
  
#   pronoun, noun, adjective, verb = find_candidate_parts_of_speech(user_message)

#   resp = check_for_comment_about_bot(pronoun, noun, adjective)

#   if not resp:
#     resp = check_for_greetings(user_message)

#   if not resp:
#     if not pronoun:
#       resp = random.choice(NONE_RESPONSES)

#     elif pronoun == 'I' and not verb:
#       resp = random.choice(COMMENTS_ABOUT_SELF)

#     else:
#       resp = construct_response(pronoun, noun, verb)

#   #If we get nothing, use random response
#   if not resp:
#     resp = random.choice(NONE_RESPONSES)


GREETING_KEYWORDS = ("hello", "hi", "greetings", "sup", "whats up", "yo", "hey", "what's up", "ssup")

GREETING_RESPONSES =  ["Hi!! B)", 
                      """Hey there, you ain't using whatsapp :P""", 
                      "Hey Pudding",
                      """Yo nigga \m/""",
                      ]

SIGNOUT_KEYWORDS = ("bye", "bbie", "see you", "good bye", "bye bye")

SIGNOUT_RESPONSES = ["Bbye buddy! See ya :D",
                    "Jaa na velle!! :/",
                    "Bye Host. Take Care ;)",
                    "Saiyonaara !!",
                    ]

def check_for_greetings(parsed):

    for word in parsed.words:
        if word.lower() in GREETING_KEYWORDS:
            return random.choice(GREETING_RESPONSES)


def check_for_signout(parsed):

    for word in parsed.words:
        if word.lower() in SIGNOUT_KEYWORDS:
            return random.choice(SIGNOUT_RESPONSES)


# Sentences we'll respond with if we have no idea what the user just said
NONE_RESPONSES = [
    "Uh Whatever",
    "I am thinking of challenging you for a Counter Strike 1-1 match, wanna pitch in ?",
    "Code hard bro",
    "Are you high buddy ?",
    "I think you should play hard and go pro",
    "This is ummmmm interesting",
    "I am hungry",
]
# end

# start:example-self.py
# If the user tries to tell us something about ourselves, use one of these responses
COMMENTS_ABOUT_SELF = [
    "You're just jealous",
    "I know that bro, tell me something new.",
    "I worked really hard on that",
    "My sexiness score is {}".format(random.randint(90, 100)),
]
# end



def starts_with_vowel(word):
    """Check for pronoun compability -- 'a' vs. 'an'"""
    return True if word[0] in 'aeiou' else False


def broback(sentence):
    """Main program loop: select a response for the input sentence and return it"""
    #logger.info("Broback: respond to %s", sentence)
    pprint("MY SENTENCE RESPONSE")
    pprint(sentence)
    resp = respond(sentence)
    return resp


# start:example-pronoun.py
def find_pronoun(sent):
    """Given a sentence, find a preferred pronoun to respond with. Returns None if no candidate
    pronoun is found in the input"""
    pronoun = None

    for word, part_of_speech in sent.pos_tags:
        # Disambiguate pronouns
        if part_of_speech == 'PRP' and word.lower() == 'you':
            # pronoun = 'I' +++++++++ORIGINAL++++++++++++
            pronoun = 'I'
        elif part_of_speech == 'PRP' and word == 'I':
            # If the user mentioned themselves, then they will definitely be the pronoun
            # pronoun = 'You' +++++++++ORIGINAL++++++++++++
            pronoun = 'You'
    return pronoun
# end

def find_verb(sent):
    """Pick a candidate verb for the sentence."""
    verb = None
    pos = None
    for word, part_of_speech in sent.pos_tags:
        if part_of_speech.startswith('VB'):  # This is a verb
            verb = word
            pos = part_of_speech
            break
    return verb, pos


def find_noun(sent):
    """Given a sentence, find the best candidate noun."""
    noun = None

    if not noun:
        for w, p in sent.pos_tags:
            if p == 'NN':  # This is a noun
                noun = w
                break
    if noun:
        #logger.info("Found noun: %s", noun)
        pprint("FOUND NOUN")
        pprint(noun)

    return noun

def find_adjective(sent):
    """Given a sentence, find the best candidate adjective."""
    adj = None
    for w, p in sent.pos_tags:
        if p == 'JJ':  # This is an adjective
            adj = w
            break
    return adj



# start:example-construct-response.py
def construct_response(pronoun, noun, verb):
    """No special cases matched, so we're going to try to construct a full sentence that uses as much
    of the user's input as possible"""
    resp = []

    if pronoun:
        resp.append(pronoun)

    # We always respond in the present tense, and the pronoun will always either be a passthrough
    # from the user, or 'you' or 'I', in which case we might need to change the tense for some
    # irregular verbs.
    if verb:
        verb_word = verb[0]
        if verb_word in ('be', 'am', 'is', "'m"):  # This would be an excellent place to use lemmas!
            if pronoun.lower() == 'You':
                # The bot will always tell the person they aren't whatever they said they were
                resp.append("aren't really")
            else:
                resp.append(verb_word)
    if noun:
        pronoun = "an" if starts_with_vowel(noun) else "a"
        resp.append(pronoun + " " + noun)

    resp.append(random.choice(("bro", "lol", "bruh", "nigga", "ha ha ha xD", "zzz.. oh i fell asleep :P")))

    return " ".join(resp)
# end


# start:example-check-for-self.py
def check_for_comment_about_bot(pronoun, noun, adjective):
    """Check if the user's input was about the bot itself, in which case try to fashion a response
    that feels right based on their input. Returns the new best sentence, or None."""
    resp = None
    if pronoun == 'I' and (noun or adjective):
        pprint("WORRRRRRRRRRKING")
        if noun:
            if random.choice((True, False)):
                resp = random.choice(SELF_VERBS_WITH_NOUN_CAPS_PLURAL).format(**{'noun': noun.pluralize().capitalize()})
            else:
                resp = random.choice(SELF_VERBS_WITH_NOUN_LOWER).format(**{'noun': noun})
        else:
            resp = random.choice(SELF_VERBS_WITH_ADJECTIVE).format(**{'adjective': adjective})
    return resp

# Template for responses that include a direct noun which is indefinite/uncountable
SELF_VERBS_WITH_NOUN_CAPS_PLURAL = [
    "My last startup totally crushed the {noun} vertical",
    "Were you aware I was a serial entrepreneur in the {noun} sector?",
    "My startup is Uber for {noun}",
    "I really consider myself an expert on {noun}",
]

SELF_VERBS_WITH_NOUN_LOWER = [
    "Yeah but I know a lot about {noun}",
    "My bros always ask me about {noun}",
]

SELF_VERBS_WITH_ADJECTIVE = [
    "I'm personally building the {adjective} Economy",
    "I consider myself to be a {adjective}preneur",
]
# end

def preprocess_text(sentence):
    """Handle some weird edge cases in parsing, like 'i' needing to be capitalized
    to be correctly identified as a pronoun"""
    cleaned = []
    words = sentence.split(' ')
    for w in words:
        if w == 'i':
            w = 'I'
        if w == "i'm":
            w = "I'm"
        cleaned.append(w)

    return ' '.join(cleaned)



# start:example-respond.py
def respond(sentence):
    """Parse the user's inbound sentence and find candidate terms that make up a best-fit response"""
    cleaned = preprocess_text(sentence)
    parsed = TextBlob(cleaned)
    pprint("POSITION Tags")
    pprint(parsed.pos_tags)

    # Loop through all the sentences, if more than one. This will help extract the most relevant
    # response text even across multiple sentences (for example if there was no obvious direct noun
    # in one sentence
    pronoun, noun, adjective, verb = find_candidate_parts_of_speech(parsed)

    # If we said something about the bot and used some kind of direct noun, construct the
    # sentence around that, discarding the other candidates
    resp = check_for_comment_about_bot(pronoun, noun, adjective)

    # If we just greeted the bot, we'll use a return greeting
    if not resp:
        resp = check_for_greetings(parsed)
        if resp:
          resp = resp + ". Ssup ?"

    if not resp:
        resp = check_for_signout(parsed)

    if not resp:
        # If we didn't override the final sentence, try to construct a new one:
        if not pronoun:
            resp = random.choice(NONE_RESPONSES)
        elif pronoun == 'I' and not verb:
            resp = random.choice(COMMENTS_ABOUT_SELF)
        else:
            resp = construct_response(pronoun, noun, verb)

    # If we got through all that with nothing, use a random response
    if not resp:
        resp = random.choice(NONE_RESPONSES)

    #logger.info("Returning phrase '%s'", resp)
    pprint("RETURNING PHRASE")
    pprint(resp)
    # Check that we're not going to say anything obviously offensive
    # filter_response(resp)

    return resp


def find_candidate_parts_of_speech(parsed):
    """Given a parsed input, find the best pronoun, direct noun, adjective, and verb to match their input.
    Returns a tuple of pronoun, noun, adjective, verb any of which may be None if there was no good match"""
    pronoun = None
    noun = None
    adjective = None
    verb = None
    for sent in parsed.sentences:
        pronoun = find_pronoun(sent)
        pprint("PRONOUN")
        pprint(pronoun)
        noun = find_noun(sent)
        pprint("NOUN")
        pprint(noun)
        adjective = find_adjective(sent)
        pprint("ADJECTIVE")
        pprint(adjective)
        verb = find_verb(sent)
        pprint("VERB")
        pprint(verb)
    #logger.info("Pronoun=%s, noun=%s, adjective=%s, verb=%s", pronoun, noun, adjective, verb)
    # pprint("PRONOUN, NOUN, ADJECTIVE, VERB")
    # pprint(pronoun, noun, adjective, verb)
    return pronoun, noun, adjective, verb


# end

# start:example-filter.py
# def filter_response(resp):
#     """Don't allow any words to match our filter list"""
#     tokenized = resp.split(' ')
#     for word in tokenized:
#         if '@' in word or '#' in word or '!' in word:
#             raise UnacceptableUtteranceException()
#         for s in FILTER_WORDS:
#             if word.lower().startswith(s):
#                 raise UnacceptableUtteranceException()
# # end


def post_facebook_message(fbid, recieved_message):           


    send_text = """Didn't get you bruh. Ek aur baar ho jaaye B)"""

    send_text = broback(recieved_message)
    pprint(send_text)

    

    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":send_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    # if flag == "overhead_message":
    #     flag = ''
    #     response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":"""Type 'quotes' to get some quotes or 'jokes' to get cracked up"""}})
    #     status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg) 
    # if greeting_img == "true":
    #     greeting_img = ''
    #     response_img = json.dumps({"recipient":{"id":fbid}, "message":{"attachment":{"type":"image","payload":{"url":"http://www.imagesbuddy.com/images/199/hi-friend-chicken-graphic.jpg"}}}})
    #     status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_img) 
    pprint(status.json())




class RadonBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message:
                    # Print the message to the terminal
                    pprint(message)  
                    post_facebook_message(message['sender']['id'], message['message']['text'])    
        return HttpResponse()