from time import sleep
import random

#----------------------------------------------------------------------------------------------------------------------------

#The class used to make a card object that has a colour and a numeral denomination
class Card:
#The card class isn't used on its own but is insted used within the deck class to make a deck of cards
        def __init__(self, num, colour):
                self.num = int(num)
                self.colour = colour
#Show function is needed as a card object cannot be represented as a string
        def show(self):
                return ('{0}, {1}'.format(self.colour, self.num))
#The deck uses the card object and puts them all in a list to make a whole deck
class Deck:
#These are the different colours that will be used in the deck
        colour = ['red','black','yellow']

        def __init__(self):
                self.cards = []
                self.make_deck()

        def make_deck(self):
#This is the logic that is used to make the deck. For each colour there is 10 numbers.
                for c in self.colour:
                        for n in range(1, 11):
                                self.cards.append(Card(n, c))
        
        def show_deck(self):
                for n, c in enumerate(self.cards, 1):
                        print('{0}. {1}'.format(n, c.show()))

#Simple shuffle function using the built in shuffle method
        def shuffle(self):
                print('Shuffling...')
                random.shuffle(self.cards)
#Player class that holds the player information such as name and hand. The hand is used to store their won cards
#Creates deck object with all colours and numbers
deck = Deck()
class Player:

        def __init__(self, name):
                self.hand = []
                self.name = name

        def draw(self):
#Card must be removed from the deck if it was drawn, hence the pop method
                card = deck.cards.pop(0)
                print('{} drew the {}'.format(self.name, card.show()))
                #self.hand.append(card)
                return card

#----------------------------------------------------------------------------------------------------------------------------

#For loop that goed through user.txt and decided whether the details entered are valid
def authenticate():
                while True:
                        auth_name = input('Username: ')
                        passwrd = input('Password: ')
                        f = open('users.txt','r')
                        #For each line in the file, if the line reads the username and password return the name
                        for l in f:
                                if auth_name + '-' + passwrd + '\n' == l:
                                        print('Access granted')
                                        f.close()
                                        return auth_name
                                        break
                        else:
                        #Access is bared against incorrect usernames and passwords
                                print('Access denied')
                        #Authentication will run again upon an unsuccessful logon attempt, hence continue
                                continue
                        break

#----------------------------------------------------------------------------------------------------------------------------
                
#This is where the programme runs and you can see the logical order of how each run goes
def main():
        
        #Explanation of key below     
        '''To understand the key here is that the first colour
        is the player 1 and the second is player 2. If the input
        is true then player 1 has won. If it is false, then player
        2 has won'''

        winner_key = {

                 'redblack':True,
                 'yellowred':True,
                 'blackyellow':True,
                 'blackred':False,
                 'redyellow':False,
                 'yellowblack':False
                 
                }
        
        
        #User has the option to set the game speed. Default value is 2
        speed = 2
        #The first user is authenticated and their name is set to their player ID
        n1 = authenticate()    
        player1 = Player(n1)
        #Since the deck will always be in order, the deck needs to be shuffled so that each game plays out differently
        deck.shuffle()
        #Below is the option to show the shuffled deck before play begins
        #deck.show_deck()

        #Here is the code for if a second player would like to play or if you are just playing against a computer  
        is2p = input('Would you like to play against a friend? [Y/N]: ')
        if is2p.lower().startswith('y'):
            print('Enter the players details below')
            n2 = authenticate()
            player2 = Player(n2)
        else:
            player2 = Player('CPU')

        print('''
        \n*RULES*\n
        If the colour of the cards are the same, the card
        with the highest numeral denomination wins.
        Otherwise, the colours will trump one another to
        determine the winner (see key below). The winning
        player takes the opponent's card and play continues
        until the deck has 0 cards left.
        
        RED beats BLACK
        YELLOW beats RED
        BLACK beats YELLOW
        In the event of a tie, HIGHEST NUMBER wins
        
        Note: There can never be a tie in numbers
        as each card only ever appears once.
        
        PLEASE KEEP IN MIND THIS IS A GAME OF CHANCE SO iF YOU LOSE
        DON'T BE TOO SALTY AS THE GAME IS JUST FOR FUN AND IS NOT
        SUPPOSED TO BE COMPETITIVE''')


        breaker = 0
        try:
            speed = int(input('\nEnter the speed you would like to play at (2 is the default, lower is faster): '))
        except:
            print('Default value selected (2)')
            speed = 2
            
        print('Loading...')
        sleep(1)
        input('\nTo start, press the enter key')

        while True:
        #Here is the basic gameplay loop. The deck is drawn out until no cards are remaining. This is checked first       
                if len(deck.cards) == 0:
                        
                        winner_score = max(len(player1.hand), len(player2.hand))
                        
                        if len(player1.hand) > len(player2.hand):
                                winner_name = player1.name

                        else:
                                winner_name = player2.name


                        with open('highscores.txt','a') as f:
                                f.write(str(winner_score)+', '+winner_name+'\n')
                                #f.write(str(winner_score)+'\n')
                                
                        print('The winner with {0} cards in hand is {1}'.format(winner_score, winner_name))
                        #Number of won rounds is always half of the cards they hold since the winner wins both their card and the opponents
                        print(winner_name,' won ',(winner_score//2),' rounds')

                        while True:
                                menu = input('Play again or view highscores or exit: ')
                                if menu.lower().startswith('y'):
                                        main()
                                
                                elif menu.lower().startswith('h') or menu.lower().startswith('v'):
                                        with open('highscores.txt','r') as f:
                                                #Makes list from scores then sorts them in descending order and slices off the top 5 to display
                                                scores = [i for i in f]
                                                scores.sort(reverse=True)
                                                topscores = scores[:5]
                                                print('The top 5 high scores are:')
                                                for p, l in enumerate(topscores, start=1):
                                                    print(str(p)+') '+str(l))

                                                print('Thank you for playing!')

                                        breaker = 1
                                        break
                                
                                else:
                                        print('Thank you for playing!') 
                                        break
                if breaker == 1:
                        break

                sleep(speed)
        #Cards are drawn and displayed during this phase, players are give time to see who has drawn what
                c1, c2 = player1.draw(), player2.draw()
                sleep(speed)
        #It is important that the colour is checked before the number as the colour always trumps a higher number
        #If the colours are the same, then the number will decide the winner
                if c1.colour == c2.colour:
                        if c1.num > c2.num:
                                print(player1.name,' wins!\n')
                                player1.hand.extend([c1, c2])
                        
                        else:
                                print(player2.name,' wins!\n')
                                player2.hand.extend([c2, c1])
        #If the colour is the same, the number will act as a tie breaker
        #Colours are concatenated and then checked against a key to see who is the winner
                else:
                        result = c1.colour + c2.colour
                        winner = winner_key[result]
                        if winner:
                                print(player1.name,' wins!\n')
                                player1.hand.extend([c1, c2])
                        else:
                                print(player2.name,' wins!\n')
                                player2.hand.extend([c2, c1])

#----------------------------------------------------------------------------------------------------------------------------
                                
#Prevents main being ran as a module
if __name__ == '__main__':
        main()
        
