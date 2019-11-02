import random


def positive_responses(tweet):
    '''
    In the cases where our model chooses to reply to very positive responses, let's
    use these probably too rigid rules to determine a response.
    '''

    response = ""
    
    thanks = ['thank', 'thanks']
    thanks_replies = ["Thanks for being polite! ", ":) ", "Keep up the kindness! "]
    if any(x in tweet.lower() for x in thanks):
        response += random.choice(thanks_replies)

    good_day = ['good day', 'wonderful day', 'great day', 'fabulous day', 'awesome day', 'safe day']
    good_day_replies = ["You have a good day yourself! ", "Have a good day. ", "Hugs!! ",
                        "Keep spreading the positivity! "]
    if any(x in tweet.lower() for x in good_day):
        response += random.choice(good_day_replies)
    
    appreciate = ['appreciate']
    appreciate_replies = ["Appreciate your kindness! ", "Spread the love! ", "I appreciate you! "]
    if any(x in tweet.lower() for x in appreciate):
        response += random.choice(appreciate_replies)

    wait = ['waiting', 'wait for', 'where is']
    if any(x in tweet for x in wait):
        response += "Try downloading the SubwayTime app for more info. "
        
    if response != "":
        return response
    else:
        pass

def negative_responses(tweet):
    '''
    Some ideas for negative responses. Why can I only think of more things to say for negative
    tweets than I can for negative tweets? I might need to apply polite bot to myself.
    '''
    response = ""

    fuck_you = ['fuck you', 'you fuck', 'fucking asshole', 
                'fuck off', 'fuckin ass']
    fuck_you_replies = ["Cmon can you ease up a little bit? You're talking to a person. ",
                        "Lighten up a little will ya ", "Be nice please!! ", "Try not to say the F word. "
                        "It's not the NYCTSubway accounts fault! They're trying to help you. ",
                        "Stop it. ", "Dude. ", "Cmon now. ", "Hey your account is public, be nicer. ",
                        "Are you drunk? "]
    if any(x in tweet.lower() for x in fuck_you):
        response += random.choice(fuck_you_replies)

    curse = [' ass', 'asshole', 'retard', 'bitch', 'idiot', 'dumbass', 
             'jackass', ' shit', 'shitty']
    curse_replies = ["Watch your language please there are children here. ", "LANGUAGE!! ", 
                    "Maybe if you were nicer they'd help more. ", "Spread love not hate. ",
                    "It'll be ok boss. ", "What's your deal? "]
    if any(x in tweet.lower() for x in curse):
        response += random.choice(curse_replies)

    wait = ['waiting', 'wait for', 'where is']
    if any(x in tweet.lower() for x in wait):
        response += "Try downloading the SubwayTime app for more info. "

    if response != "":
        return response
    else:
        pass


def fuhgettaboutit():
    # if they reply to one of my replies, say "Fuhgettaboutitttttt"
    pass
