

### ######### ### ### ### ######### ### ### ### ######### ### ### ### ######### ### 

### imports


import speech_recognition as sr
from gtts import gTTS

import os
import re

import streamlit as st



###### 
# app Title
st.title(" Virtual Assitant ")


### Variables

# Variable for the towel data 
towel_req = [[0,0],         #      , room number
             [0,0],         #  flag, count bath towel 
             [0,0],         #  flag, count face towel
             [0,0]]         #  flag, count washcloth

key_towel = '.*\\bi need some towels\\b.*|.*\\bi need some towel\\b.*' #"I need some towels"



### ######### ### ### ### ######### ### Speech to Text and Text to Speech Functions

# gTTS - Convert Text to speech
def text_to_speech(text):
    print("Virtual Assistant: ", text)
    st.write("Virtual Assistant: ", text)
    speaker = gTTS(text=text, lang="en", slow=False)
    speaker.save("res.mp3")
    os.system("afplay res.mp3") 
    os.remove("res.mp3")

# Speech Recognition, using speech_recognition
def speech_to_text():
    text = ""
    recognizer = sr.Recognizer()
    with sr.Microphone() as mic:
        st.write("--- listening now --- ")
        print("--- listening now --- ")
        audio = recognizer.listen(mic)
    try:
        text = recognizer.recognize_google(audio)
        st.write("Human:",text)
        print("Human:",text)
    except:
        st.write("Human: Error no sound recondized")
        print("Human: Error no sound recondized")
        #text_to_speech('i am sorry i did not get that.')
    return text.lower()

### ######### ### ### ### ######### ### YES / NO 

######
#### yes or no 


def yesNo(vaReply):
    
    yes = '.*\\byes\\b.*|.*\\byep\\b.*|.*\\bcorrect\\b.*'
    no =  '.*\\bno\\b.*|.*\\bnegative\\b.*|.*\\bnope\\b.*'
    
    # Var
    exitLoop = False
        
    while True:
        
        # output 
        text_to_speech(vaReply)
        # input 
        human_input = speech_to_text()
        
       # IF 
    
        if re.search(no,human_input):
            # no
            return False
        elif re.search(yes,human_input):
            # flag to exit loop
            return True
        else:
            text_to_speech("I am sorry i did not understand that.")
            st.write("I am sorry i did not understand that.")
    
    return exitLoop


### ######### ### ### ### ######### ###

######

def numberofTowels(type_of_towel):
    yes = '.*\\byes\\b.*|.*\\byep\\b.*|.*\\bcorrect\\b.*'
    clean_input = 0     

    vaReply = "how many " + type_of_towel + " towels would you like?"
    text_to_speech(vaReply)
    
    while (True):
    
        # input 
        human_input = speech_to_text()
        # only the numbers
        try:
            clean_input = int(re.sub('\D', '', human_input) )
        except:
            vaReply = "I am sorry i did not get that.  How many " + type_of_towel + " towels would you like?"
            text_to_speech(vaReply)
            print('except')
             
        if (clean_input <= 20) & (clean_input > 0): 
            return clean_input
            
        elif clean_input > 20:
            vaReply = 'i am sorry the max towels we can send you is 20.  We will send you 20.'    
            text_to_speech(vaReply)
            return 20
        else:
            text_to_speech('is this another converstation')
            print('is this another converstation')


######
### Type of Towels



def TypeofTowel(towel_req):
    
    # Var
    
    exit = False
    
    
    while (exit == False):
    
        # output 
        vaReply = "what type of towels would you like: bath towels, hand towels, or washcloths"
        text_to_speech(vaReply)
        # Input 
        human_input = speech_to_text()
        

       ### if statment
        if re.search('.*\\bbath\\b.*',human_input):
            towel_req[1][0] = 1 
            exit = True
            # number of towels
            towel_req[1][1] = numberofTowels('bath') 
            
        elif re.search('.*\\bhand\\b.*|.*\\bhands\\b.*',human_input):
            towel_req[2][0] = 1 
            exit = True
            # number of towels
            towel_req[2][1] = numberofTowels('hand') 
            
        elif re.search('.*\\bwashcloth\\b.*',human_input):
            towel_req[3][0] = 1 
            exit = True
            # number of towels
            towel_req[3][1] = numberofTowels('washcloth') 
        
        else:
            print('ELSE')
            #while 
                #smart-chat responce
                # maybe if smart chatbot responce cosi is > ___ threshhold 
            vaReply = "I am sorry i did not understand that"
            text_to_speech(vaReply)
        
    return towel_req      



######
### Room Number


def roomNumber():
   # VAR 
    flag = False
    keyRoomNumber = False
    clean_input = 0   

    vaReply = "What room number should I send this up too?"
    #text_to_speech(vaReply)
    
    while (keyRoomNumber == False):
        text_to_speech(vaReply)
       
        # input 
        human_input = speech_to_text()
        
        try:
            clean_input = int(re.sub('\D', '', human_input) )
            print('try - clean input: ',clean_input)
            
        except:
            vaReply = "I am sorry i did not get that, what is your room number?"
            text_to_speech(vaReply)
            print('except')
        
        if (clean_input <= 5000) & (clean_input > 0): 
            flag = True
            room_number = clean_input 
        elif (clean_input > 5000) & (clean_input < 0):
            text_to_speach('I am sorry that room number does not exist')
            
            
       # FLAG to confirm room number 
        if flag == True:
            keyRoomNumber , flag = room_confirmation(room_number)
    
    return room_number


######
### Confrim Room numbers



def room_confirmation(room_number):
   # VAR
    yes = '.*\\byes\\b.*|.*\\byep\\b.*|.*\\bcorrect\\b.*'
    no =  '.*\\bno\\b.*|.*\\bnegative\\b.*|.*\\bnope\\b.*|.*\\bnot\\b.*'
    
    vaReply = "you said room " + str(room_number) + ' is that correct?'
    text_to_speech(vaReply)
    
    while True:
        
        # input 
        human_input = speech_to_text()
        print('human input: ',bool(re.search(yes,human_input)))
        if re.search(no,human_input):
            vaReply = "no problem let me change that"
            text_to_speech(vaReply)
            return False, False
            
        elif re.search(yes,human_input):
            vaReply = "perfect"
            text_to_speech(vaReply)
            return True,True 
        else:
            vaReply = "I am sorry i did not understand that, you said room " + str(room_number) + ' is that correct?'
            text_to_speech(vaReply) 
        print('confirm loop')





######
### Confirm Towels

def towel_confirmation(towel_req):

    
    # VAR
    yes = '.*\\byes\\b.*|.*\\byep\\b.*|.*\\bcorrect\\b.*'
    no =  '.*\\bno\\b.*|.*\\bnegative\\b.*|.*\\bnope\\b.*|.*\\bnot\\b.*'
    
    
    towel_dict = {1:'bath', 2:'hand', 3:'washcloths'}
    words = ['','','']
    conj_words = ['','']
    towels_word = ' towels '
    c = 0
    
    
  ### runs through towel array to Create vaReply sentence
    for i in range(1,4):
        
    # checks agent towel type flag in array 
        if towel_req[i][0] == 1:
            # checks to see if word towels should be used (not using word towels after washcloths)
            if i == 3:
                towels_word  = ''
            words[(i-1)] = str(towel_req[i][1]) + ' ' + towel_dict[i] + towels_word
            c += 1
            
    # chooses conjections for sentence         
    if c == 2:
        conj_words[0] = 'and '
    elif c == 3:
        conj_words[0] = ','
        conj_words[1] = 'and '
    
    # appends sentence
    vaReply = 'to confirm, you would like ' + words[0] + conj_words[0] + words[1] + conj_words[1] + words[2] + ', is this correct?'    
    
    while True:
        
        # output
        text_to_speech(vaReply)
        
        # input 
        human_input = speech_to_text()
        

        if re.search(no,human_input):
            vaReply = "no problem let me change that"
            text_to_speech(vaReply)
            # causes the loop to run again 
            return False
            
        elif re.search(yes,human_input):
            vaReply = "perfect"
            text_to_speech(vaReply)
            # exits the loop 
            return True 
        else:
            text_to_speech('I am sorry i did not get that') 









### ######### ### ### ### ######### ### ### ### ######### ### ### ### ######### ###
###                                          main loop for Towels
### ######### ### ### ### ######### ### ### ### ######### ### ### ### ######### ###





def need_towels():
    yes = '.*\\byes\\b.*|.*\\byep\\b.*|.*\\bcorrect\\b.*'
    no =  '.*\\bno\\b.*|.*\\bnegative\\b.*|.*\\bnope\\b.*'
    
    #Var & flags
    #keyRoomNumber = False
    flag = True
    exit = False
    #additional_flag = False
    
    towel_req = [[0,0],         #      , room number
             [0,0],         #  flag, count bath towel 
             [0,0],         #  flag, count face towel
             [0,0]]         #  flag, count washcloth
    
    
    # loop for towel 
    while exit == False:
        
       ### Loop to select more then 1 type of towel
        while (flag == True):
            
           # Type of Towel 
            towel_req = TypeofTowel(towel_req)

           # Would you like additonal towels ? 
            flag = yesNo('would you like any additional type of towel')
                    
    ### Confirm towel amounts          
        exit = towel_confirmation(towel_req)
        
    ### Input Room Number 
    towel_req[0][0] = roomNumber()
    
    
    ### ### ###
    
    return towel_req
        




### ######### ### ### ### ######### ### ######### ### ### ### ######### ###
#                                           Main Program
### ######### ### ### ### ######### ### ######### ### ### ### ######### ###


if __name__ == "__main__":
    
    
    # flags
    mainloopflag = True
    new_topic = True
    quit = False

    
    # main loop 
    while (mainloopflag == True):
        # Welcome 
        if new_topic == True:
            text_to_speech('Hello this is the Tokyo Grand Hyatt, how can we help you')  
            new_topic = False
        
        elif new_topic == False:
           quit = yesNo('Can can i help you with anything else')
           if quit==True:
               break
            
        res = speech_to_text()
        
        
    ### Menu System 
    
        # I need some Towels
        if re.search(key_towel, res):
            towel_req = need_towels()
            text_to_speech('Excelent, we will send them straight up!')
            print(towel_req)


            