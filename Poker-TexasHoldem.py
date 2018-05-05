# Calculating the total final points and announcing the winner
import string, math, random, itertools

class Card (object):

	# Creating objects of the class Rank and Suit and assigning values to it
    RANKS = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
    SUITS = ('Spades', 'Diamonds', 'Hearts', 'Clubs')

    def __init__ (self, rank, suit):
        self.rank = rank
        self.suit = suit

  #Assinging ranks to cards - A,K,Q,J for comparison among ranks
    def __str__ (self):
        if self.rank == 14:
            rank = 'A'
        elif self.rank == 13:
            rank = 'K'
        elif self.rank == 12:
            rank = 'Q'
        elif self.rank == 11:
            rank = 'J'
        else:
            rank = self.rank
        return str(rank) + self.suit

  #Functions used to compare the ranks among cards (used to sort the cards based on their ranks)
    def __eq__ (self, other):
        return (self.rank == other.rank)

    def __ne__ (self, other):
        return (self.rank != other.rank)

    def __lt__ (self, other):
        return (self.rank < other.rank)

    def __le__ (self, other):
        return (self.rank <= other.rank)

    def __gt__ (self, other):
        return (self.rank > other.rank)

    def __ge__ (self, other):
        return (self.rank >= other.rank)

   
class Deck (object):
  #Creating a deck of 52 cards using ranks and suits defined in the Card Class. Also, creating an instance of class Card
    def __init__ (self):
        self.deck = []
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                card = Card (rank, suit)
                self.deck.append(card)
  
  #Using the library Random, suffling the cards after each game
    def shuffle (self):
        random.shuffle (self.deck)

  #Returning the length of the deck
    def __len__ (self):
        return len (self.deck)

  #Dealing the cards. Poping 1 card from the deck and returning the popped card
    def deal (self):
        if len(self) == 0:
            return None
        else:
            return self.deck.pop(0)

# Class to distribute cards in the game. 2 cards before flop, 3 cards after flop, 1 card at turn and 1 card at river
class Card_Display():  
    def __init__(self, numPlayers, player_bank, player_names):
        self.deck = Deck()
        self.deck.shuffle()
        self.hands = []
        self.tlist = []
        self.numCards_in_Hands = 2
        self.player_names = player_names
        self.money1 = Betting(numPlayers, player_bank, player_names)        
        self.point1 = Points(numPlayers, player_bank, player_names)        
        self.numPlayers = numPlayers
        self.final_pot_value = 0
        self.final_player_bet = []
        self.player_bank = player_bank
         
    # Distributing 2 distinct cards to each player once the game has started
    def pre_flop(self, numPlayers, player_names):
        print("\n-------------------------------------------------------------------------------------------")
        print("----------------------------------------Pre Flop-------------------------------------------")
        print("-------------------------------------------------------------------------------------------\n")
        print("\n-----------------------------Pre Flop Cards display (Sorted)-------------------------------\n")
        for i in range(numPlayers):
            hand = []
            for j in range(self.numCards_in_Hands):
                hand.append(self.deck.deal())
            self.hands.append(hand)
        
        for i in range(len(self.hands)):
            sortedHand = sorted (self.hands[i], reverse = True)
            hand = ''
            for card in sortedHand:
                hand = hand + str(card) + ' '
            print (str(self.player_names[i])  + ' : ' + hand)

        # Call the Betting & Reset function
        print("\n------------------------------------Pre Flop Betting---------------------------------------\n")
        self.money1.blind_bets(self.money1.numPlayers, self.money1.player_names)
        self.money1.betting_round(self.money1.cur_index, self.money1.players_bet, self.money1.player_bet_counter, self.money1.player_names)
        if self.money1.all_fold == 0:
            self.money1.reset_index(self.money1.cur_index, self.money1.players_bet, self.money1.bet_money, self.money1.player_bet_counter)
            print("\nCurent Pot Value = " + str(self.money1.pot))
            self.flop(self.numPlayers, self.player_names)
        else:
            for i in range(len(self.money1.players_bet)):
                self.final_player_bet.append(self.money1.players_bet[i])
            self.final_pot_value = self.money1.pot
            self.point1.result_fold(self.player_names, self.final_player_bet)
                

    
    #Picking 3 cards from the remaining deck and appending those to each of the player's hand
    def flop(self, numPlayers, player_names):  
        print("\n------------------------------------Flop Cards display------------------------------------\n")
        flop_hand = []
        for j in range(3):
            flop_hand.append(self.deck.deal())
        
        
        print("Flop Cards are: " +  " ".join(str(card) for card in flop_hand))
        for i in range(len(self.hands)):
            for j in flop_hand:
                self.hands[i].append(j)
        
        print("\nPlayer Cards after Flop (Sorted)")
        for i in range(len(self.hands)):
            sortedHand = sorted (self.hands[i], reverse = True)
            hand = ''
            for card in sortedHand:
                hand = hand + str(card) + ' '
            print (str(self.player_names[i])  + ' : ' + hand)

        # Call the Betting & Reset function
        print("\n-----------------------------------After Flop Betting-------------------------------------\n")
        #Print the bank balance of each player after pre flop betting
        print("Current Bank Balance of the players:\n")
        for i in range(len(self.player_bank)):
            print(str(self.player_names[i]) + ": " + str(self.player_bank[i]))
        print("\n")
        
        self.money1.betting_round(self.money1.cur_index, self.money1.players_bet, self.money1.player_bet_counter, self.money1.player_names)
        if self.money1.all_fold == 0:
            self.money1.reset_index(self.money1.cur_index, self.money1.players_bet, self.money1.bet_money, self.money1.player_bet_counter)
            print("\nCurent Pot Value = " + str(self.money1.pot))
            self.turn(self.numPlayers, self.player_names)
        else:
            for i in range(len(self.money1.players_bet)):
                self.final_player_bet.append(self.money1.players_bet[i])
            self.final_pot_value = self.money1.pot
            self.point1.result_fold(self.player_names, self.final_player_bet)
        
                
            
    #Picking 1 card from the remaining deck and appending those to each of the player's hand
    def turn(self, numPlayers, player_names):
        print("\n------------------------------------Turn Card display-------------------------------------\n")
        turn = []
        for j in range(1):
            turn.append(self.deck.deal())
        
        
        print("Turn Card is: " +  " ".join(str(card) for card in turn))
        for i in range(len(self.hands)):
            for j in turn:
                self.hands[i].append(j)
        
        print("\nPlayer Cards after Turn (Sorted)")
        for i in range(len(self.hands)):
            sortedHand = sorted (self.hands[i], reverse = True)
            hand = ''
            for card in sortedHand:
                hand = hand + str(card) + ' '
            print (str(self.player_names[i])  + ' : ' + hand)

        # Call the Betting & Reset function
        print("\n-----------------------------------After Turn Betting-------------------------------------\n")
        #Print the bank balance of each player after pre flop betting
        print("Current Bank Balance of the players:\n")
        for i in range(len(self.player_bank)):
            print(str(self.player_names[i]) + ": " + str(self.player_bank[i]))
        print("\n")
        
        self.money1.betting_round(self.money1.cur_index, self.money1.players_bet, self.money1.player_bet_counter, self.money1.player_names)
        if self.money1.all_fold == 0:
            self.money1.reset_index(self.money1.cur_index, self.money1.players_bet, self.money1.bet_money, self.money1.player_bet_counter)
            print("\nCurent Pot Value = " + str(self.money1.pot))
            self.river(self.numPlayers, self.player_names)
        else:
            for i in range(len(self.money1.players_bet)):
                self.final_player_bet.append(self.money1.players_bet[i])
            self.final_pot_value = self.money1.pot
            self.point1.result_fold(self.player_names, self.final_player_bet)
  
        
    #Picking 1 card from the remaining deck and appending those to each of the player's hand
    def river(self, numPlayers, player_names):        
        print("\n------------------------------------River Card display------------------------------------\n")
        river = []
        for j in range(1):
            river.append(self.deck.deal())
             
        print("River Card is: " +  " ".join(str(card) for card in river))
        for i in range(len(self.hands)):
            for j in river:
                self.hands[i].append(j)
        
        print("\nPlayer Cards after River (Sorted)")
        for i in range(len(self.hands)):
            sortedHand = sorted (self.hands[i], reverse = True)
            hand = ''
            for card in sortedHand:
                hand = hand + str(card) + ' '
            print (str(self.player_names[i])  + ' : ' + hand)

        # Call the Betting & Reset function
        print("\n-----------------------------------After River Betting------------------------------------\n")
        #Print the bank balance of each player after pre flop betting
        print("Current Bank Balance of the players:\n")
        for i in range(len(self.player_bank)):
            print(str(self.player_names[i]) + ": " + str(self.player_bank[i]))
        print("\n")
              
        self.money1.betting_round(self.money1.cur_index, self.money1.players_bet, self.money1.player_bet_counter, self.money1.player_names)
        if self.money1.all_fold == 0:
            self.money1.reset_index(self.money1.cur_index, self.money1.players_bet, self.money1.bet_money, self.money1.player_bet_counter)
            print("\nCurent Pot Value = " + str(self.money1.pot))
            self.final_pot_value = self.money1.pot
            
            for i in range(len(self.money1.players_bet)):
                self.final_player_bet.append(self.money1.players_bet[i])
        else:
            for i in range(len(self.money1.players_bet)):
                self.final_player_bet.append(self.money1.players_bet[i])
            self.final_pot_value = self.money1.pot
            self.point1.result_fold(self.player_names, self.final_player_bet)



#Class for maintaining the bets among players for each round - Preflop, after flop, after turn and then after river followed by final Showdown
class Betting ():
    def __init__(self, numPlayers, player_bank, player_names):
        #Equal buy-in for each player at the begining of the game. Each player given $10,000 at the start of the game.
        self.player_bank = player_bank
        #Keeping track of the index of the current player
        self.player_names = player_names
        self.numPlayers = numPlayers
        
        self.cur_index = 0
        self.players_bet = [0] * numPlayers 
        self.player_bet_counter = [0] * numPlayers 
        self.bet_money = 0
        self.pot = 0 
        self.all_fold = 0
        

  #Method is called at start of each game (and not each round). Initializing the blinds, bet_money and pot. 
  #Check the number of players at start of the game and initialize the variables - self.players_bet(to keep index of each player) and
  #player_bet_counter to 
    def blind_bets(self, numPlayers, player_names):
        self.big_blind = 20
        self.small_blind = 10
        self.pot = self.big_blind + self.small_blind
        
        # Small and Big Blind
        print("The Blinds are:")
        print(self.player_names[1] + " - Small Blind of "+ str(self.small_blind))
        self.players_bet[1] = self.small_blind
        self.player_bank[1] = self.player_bank[1] - self.small_blind
        print(self.player_names[2%numPlayers] + " - Big Blind of " + str(self.big_blind))
        self.players_bet[(2%numPlayers)] = self.big_blind
        
        print("\nCurent Pot Value = " + str(self.pot))
        
        #Updating the bank balance of small and big blind players
        self.player_bank[(2%numPlayers)] = self.player_bank[(2%numPlayers)] - self.big_blind
    
        #Assigning the currect index [1] - after big blind
        self.cur_index = 3%numPlayers
            

  #Method called after each round - PreFlop, After Flop, After Turn and after flop
    def betting_round(self, cur_index, players_bet, player_bet_counter, player_names):
    
        #Flag variable to check if the betting is to be continued for the round or the round is completed
        flag = True
        
        #Make sure there are players to play (not all folded or all-in)
        if ((self.players_bet.count(-1) == len(players_bet) -1) or (self.player_bank.count(0) == len(players_bet))
            or (self.player_bank.count(0) + self.players_bet.count(-1) == len(self.players_bet) - 1)):
            flag = False
        else:
            flag = True
            
        #Repeated till a round of betting (PreFlop, Flop, Turn or River) completes
        while (flag == True and self.all_fold == 0 
#               and (self.player_bank.count(0) + self.players_bet.count(-1) < len(self.players_bet)) 
               and (self.players_bet.count(-1) < len(self.players_bet) -1)):
            print("\nPlayers Bet for the current round: ")
            for i in range(len(self.players_bet)):
                print(str(self.player_names[i]) + ": " + str(self.players_bet[i]))
            
            #Skip if the player is all-in or folded, else continue with his betting
            if self.player_bank[self.cur_index] == 0:
                print("\n" + str(self.player_names[self.cur_index]) + " is All-In!")
            elif self.players_bet[self.cur_index] != -1:
                self.betting_choice(self.cur_index, self.players_bet, self.player_bet_counter, self.player_names)
            else:
                print("\n" + str(self.player_names[self.cur_index]) + " has folded!")

            
            #Updating the current index to the next player
            self.cur_index = (self.cur_index + 1) % len(self.players_bet)
            
            #Checking if the round is completed. If in the self.players_bet list, all betting values are equal or few are equal and rest have folded
            #Also, using player_bet_counter variable, check if the big bling player has betted or not. If not, continue with the betting for the player
            if ((len(set(self.players_bet)) == 1) or ((len(set(self.players_bet)) == 2) and (self.players_bet.count(-1) > 0))):
                if player_bet_counter[self.cur_index] != 0:
                    flag = False
                else:
                    flag = True
            else:
                flag = True

  
  #Based on the cur index and players bet, give valid options to the user to - Call, Raise, Fold or Check
    def betting_choice(self, cur_index, players_bet, player_bet_counter, player_names):
        choice = 0
        
        print("\n\n" + str(self.player_names[self.cur_index]) +  "'s turn!")  
        
        #If the cur index bet is less than the max of self.players_bet, the player cannot check but can choose to Call, Fold and Raise
        if (self.players_bet[self.cur_index] < max(self.players_bet)):     
            choice = eval(input("Choose one of the following options:\nPress 1 to Call\nPress 2 to Raise\nPress 3 to Fold\n"))
            while (choice < 1 or choice >3):
                choice = eval(input("Invalid option. Choose one of the following options:\nPress 1 to Call\nPress 2 to Raise\nPress 3 to Fold\n"))
          
            if choice == 3:
                self.player_fold(self.cur_index, self.players_bet, self.player_bet_counter, self.player_names)
          
            elif choice == 2:
                self.bet_money = int(input("How much do you want to raise to? "))
                self.player_bank_blnc(self.cur_index, self.players_bet, self.bet_money, self.player_bet_counter)
          
            else:
                self.bet_money = max(self.players_bet) - self.players_bet[self.cur_index]
                self.player_bank_blnc(self.cur_index, self.players_bet, self.bet_money, self.player_bet_counter)
        
        # Condition only used at preflop round for the Big Blind player
        elif (((self.cur_index == 2%len(self.players_bet)) and (self.players_bet[self.cur_index] == self.big_blind)) or ((max(players_bet) == 0) and (self.player_bet_counter[self.cur_index]) == 0)):     
            choice = eval(input("Choose one of the following options:\nPress 1 to Raise\nPress 2 to Fold\nPress 3 to Check\n"))
            while (choice < 1 or choice >3):
                choice = eval(input("Invalid option. Choose one of the following options:\nPress 1 to Raise\nPress 2 to Fold\nPress 3 to Check\n"))
          
            if choice == 2:
                self.player_fold(self.cur_index, self.players_bet, self.player_bet_counter, self.player_names)
          
            elif choice == 1:
                self.bet_money = int(input("How much do you want to raise to? "))
                self.player_bank_blnc(self.cur_index, self.players_bet, self.bet_money, self.player_bet_counter)
          
            else:
                player_bet_counter[self.cur_index] = player_bet_counter[self.cur_index] + 1
        
        #Else give users all the options - Call, Raise, Fold and Check
        else:  
            choice = eval(input("Choose one of the following options:\nPress 1 to Call\nPress 2 to Raise\nPress 3 to Fold\nPress 4 to Check\n"))
            while (choice < 1 or choice > 4):
                choice = eval(input("Choose one of the following options:\nPress 1 to Call\nPress 2 to Raise\nPress 3 to Fold\nPress 4 to Check\n"))
            
            if choice == 3:
                self.player_fold(self.cur_index, self.players_bet, self.player_bet_counter, self.player_names)
            
            elif choice == 2:
                self.bet_money = int(input("How much do you want to raise to? "))
                self.player_bank_blnc(self.cur_index, self.players_bet, self.bet_money, self.player_bet_counter)
            
            elif choice == 4:
                self.player_bet_counter[self.cur_index] = self.player_bet_counter[self.cur_index] + 1
            
            else :
                self.bet_money = max(self.players_bet) - self.players_bet[self.cur_index]
                self.player_bank_blnc(self.cur_index, self.players_bet, self.bet_money, self.player_bet_counter)

  
    def reset_index(self, cur_index, players_bet, bet_money, player_bet_counter):
        # Bet for each player. 
        self.bet_money = 0
        # In case its a call or raise, Value added in the players index, in case of fold, -1 is updated in the index
        #Retain the value -1 (player has folded). Else replace all the items by 0
        self.players_bet = [-1 if x == -1 else 0 for x in self.players_bet]
        # Keeping a track of number of times a player's turn came. To be updated after each round i.e. after pre-flop, after flop and after turn
        self.player_bet_counter = [0] * len(self.players_bet)
        # Update the current index, next to the dealer
        self.cur_index = 1


  #Called when the user folds. self.players_bet updated to -1 (to indicate he has folded) and his bet counter increased by 1
    def player_fold(self, cur_index, players_bet, player_bet_counter, player_names):
        self.players_bet[self.cur_index] = -1
        
        #Check if all players have folded except 1, call the result function
        if (self.players_bet.count(-1) == len(self.players_bet)-1):
            self.all_fold = 1
        
        self.player_bet_counter[self.cur_index] = self.player_bet_counter[self.cur_index] + 1
        print(str(self.player_names[self.cur_index]) + " has folded!")
    

  # Can be called anytime to check the current bank balance of all the players
    def player_bank_blnc(self, cur_index, players_bet, bet_money, player_bet_counter):
        self.bank_balance_check = []
        for i in range(len(self.players_bet)):
            self.bank_balance_check.append(0 if self.players_bet[i] == -1 else self.player_bank[i])
            
        if self.player_bank[self.cur_index] >= self.bet_money:
            if self.bet_money < (max(self.players_bet) - self.players_bet[self.cur_index]):
                print("Atleast "+ str(max(self.players_bet) - self.players_bet[self.cur_index]) +" required to call the hand")
                self.betting_choice(self.cur_index, self.players_bet, self.player_bet_counter, self.player_names)
                
#            elif ((self.player_bank[self.cur_index] == max(self.bank_balance_check)) and (self.bet_money > sorted(self.bank_balance_check)[-2])):
#                print("Player can bet a maximum of " + str(sorted(self.bank_balance_check)[-2]))
#                self.betting_choice(self.cur_index, self.players_bet, self.player_bet_counter, self.player_names)
                
            else:
                self.player_bank[self.cur_index] =  self.player_bank[self.cur_index] - self.bet_money
                self.players_bet[self.cur_index] =  self.players_bet[self.cur_index] + self.bet_money
                self.player_bet_counter[self.cur_index] = self.player_bet_counter[self.cur_index] + 1
                self.pot = self.pot + self.bet_money
        else:
            print("Dont have enough balance in your account. You have " + str(self.player_bank[self.cur_index]) + " left in your account. Kindly bet/fold accordingly")
            self.betting_choice(self.cur_index, self.players_bet, self.player_bet_counter, self.player_names)
      
    #To check balance of each player
    #def check_blnc(self):
    #    print("\nCurrent Amount in each player's bank: \n") 
    #    for i in range(len(self.player_bank)):
    #        print('Player ' + str((i % len(self.players_bet))) +  ': ' + str(self.player_bank[i]))
    #  
        
        
class Points(object):
    def __init__(self, numPlayers, player_bank, player_names):
	      #create a list to store total_point and card title
        self.player_points_list = []  
        self.player_title_list = []  
        self.final_points_list = []  
        self.final_title_list = []
        #Variable ot store highest card for each player
        self.max_point_index = 0
        self.all_hands = []
        self.winner_index = []
        self.player_names = player_names
        
		   #Creating an instance of Betting() class to access pot and player_bank variable
        self.betting_obj = Betting(numPlayers, player_bank, player_names)
        

    # point()function to calculate partial score
    def point(self,hand):                         
        sortedHand=sorted(hand,reverse=True)
        c_sum=0
        ranklist=[]
        for card in sortedHand:
            ranklist.append(card.rank)
        c_sum=ranklist[0]*13**4+ranklist[1]*13**3+ranklist[2]*13**2+ranklist[3]*13+ranklist[4]
        return c_sum

    def points_calculate(self, hands, player_names, final_player_bet):
        #print(len(self.final_cards.hands))
        self.final_player_bet = final_player_bet
        print("\nBest Hand of the players:\n")
        for i in range(len(hands)):
            self.player_points_list = []  
            self.player_title_list = []
            self.max_point_index = 0
            sortedHand = sorted (hands[i], reverse = True)
            self.all_hands = []
            for L in range(5, 6):            
                for subset in itertools.combinations(sortedHand, L):                  
                    self.all_hands.append(subset)
			
            #Check if the player has folded for the round:
            for curHand in self.all_hands:
                if self.final_player_bet[i] == -1:
                     self.player_title_list.append('Folded')
                     self.player_points_list.append(0)
                else:
                    self.isRoyal(curHand)
            
            if self.final_player_bet[i] == -1:
                self.final_points_list.append(0)
            else:
                self.final_points_list.append(max(self.player_points_list))
            
            self.max_point_index = self.player_points_list.index(max(self.player_points_list))
            
            if self.final_player_bet[i] == -1:
                self.final_title_list.append("Folded")
            else:
                self.final_title_list.append(self.player_title_list[self.max_point_index])

			    #Printing the best hand along with the title
            #print("Player " + str(i+1) + ": " + str(self.all_hands[self.max_point_index]) + " " + str(self.final_title_list[self.max_point_index]))
            hand = '' 
            for card in self.all_hands[self.max_point_index]:
                hand = hand + str(card) + ' '
            print (str(self.player_names[i]) + ': ' + hand + " --> " + str(self.player_title_list[self.max_point_index]))
        
        self.result(self.player_names)
            
    #returns the total_point and prints out 'Royal Flush' if true, if false, pass down to isStraightFlush(hand)
    def isRoyal (self, hand):               
        sortedHand=sorted(hand,reverse=True)
        flag=True
        h=10
        Cursuit=sortedHand[0].suit
        Currank=14
        total_point=h*13**5+self.point(sortedHand)
        for card in sortedHand:
            if card.suit!=Cursuit or card.rank!=Currank:
                flag=False
                break
            else:
                Currank-=1
        if flag:
            self.player_title_list.append('Royal Flush')
            self.player_points_list.append(total_point)    
        else:
            self.isStraightFlush(sortedHand)
    

    def isStraightFlush (self, hand):       #returns the total_point and prints out 'Straight Flush' if true, if false, pass down to isFour(hand)
        sortedHand=sorted(hand,reverse=True)
        flag=True
        h=9
        Cursuit=sortedHand[0].suit
        Currank=sortedHand[0].rank
        total_point=h*13**5+self.point(sortedHand)
        for card in sortedHand:
            if card.suit!=Cursuit or card.rank!=Currank:
                flag=False
                break
            else:
                Currank-=1
        if flag:
            self.player_title_list.append('Straight Flush')
            self.player_points_list.append(total_point) 
        else:
            self.isFour(sortedHand)

    def isFour (self, hand):                  #returns the total_point and prints out 'Four of a Kind' if true, if false, pass down to isFull()
        sortedHand=sorted(hand,reverse=True)
        flag=True
        h=8
        Currank=sortedHand[1].rank               #since it has 4 identical ranks,the 2nd one in the sorted listmust be the identical rank
        count=0
        total_point=h*13**5+self.point(sortedHand)
        for card in sortedHand:
            if card.rank==Currank:
                count+=1
        if not count<4:
            flag=True
            self.player_title_list.append('Four of a Kind')
            self.player_points_list.append(total_point) 
        else:
            self.isFull(sortedHand)
    
    def isFull (self, hand):                     #returns the total_point and prints out 'Full House' if true, if false, pass down to isFlush()
        sortedHand=sorted(hand,reverse=True)
        flag=True
        h=7
        total_point=h*13**5+self.point(sortedHand)
        mylist=[]                                 #create a list to store ranks
        for card in sortedHand:
            mylist.append(card.rank)
        rank1=sortedHand[0].rank                  #The 1st rank and the last rank should be different in a sorted list
        rank2=sortedHand[-1].rank
        num_rank1=mylist.count(rank1)
        num_rank2=mylist.count(rank2)
        if (num_rank1==2 and num_rank2==3)or (num_rank1==3 and num_rank2==2):
            flag=True
            self.player_title_list.append('Full House')
            self.player_points_list.append(total_point)
      
        else:
            flag=False
            self.isFlush(sortedHand)

    def isFlush (self, hand):                         #returns the total_point and prints out 'Flush' if true, if false, pass down to isStraight()
        sortedHand=sorted(hand,reverse=True)
        flag=True
        h=6
        total_point=h*13**5+self.point(sortedHand)
        Cursuit=sortedHand[0].suit
        for card in sortedHand:
            if not(card.suit==Cursuit):
                flag=False
                break
        if flag:
            self.player_title_list.append('Flush')
            self.player_points_list.append(total_point)
        else:
            self.isStraight(sortedHand)

    def isStraight (self, hand):
        sortedHand=sorted(hand,reverse=True)
        flag=True
        h=5
        total_point=h*13**5+self.point(sortedHand)
        Currank=sortedHand[0].rank                        #this should be the highest rank
        for card in sortedHand:
            if card.rank!=Currank:
                flag=False
                break
            else:
                Currank-=1
        if flag:
            self.player_title_list.append('Straight')
            self.player_points_list.append(total_point)
        else:
            self.isThree(sortedHand)
        
    def isThree (self, hand):
        sortedHand=sorted(hand,reverse=True)
        flag=True
        h=4
        total_point=h*13**5+self.point(sortedHand)
        Currank=sortedHand[2].rank                    #In a sorted rank, the middle one should have 3 counts if flag=True
        mylist=[]
        for card in sortedHand:
            mylist.append(card.rank)
        if mylist.count(Currank)==3:
            flag=True
            self.player_title_list.append("Three of a Kind")
            self.player_points_list.append(total_point)
        else:
            flag=False
            self.isTwo(sortedHand)
        
    def isTwo (self, hand):                           #returns the total_point and prints out 'Two Pair' if true, if false, pass down to isOne()
        sortedHand=sorted(hand,reverse=True)
        flag=True
        h=3
        total_point=h*13**5+self.point(sortedHand)
        rank1=sortedHand[1].rank                        #in a five cards sorted group, if isTwo(), the 2nd and 4th card should have another identical rank
        rank2=sortedHand[3].rank
        mylist=[]
        for card in sortedHand:
            mylist.append(card.rank)
        if mylist.count(rank1)==2 and mylist.count(rank2)==2:
            flag=True
            self.player_title_list.append("Two Pair")
            self.player_points_list.append(total_point)
        else:
            flag=False
            self.isOne(sortedHand)
  
    def isOne (self, hand):                            #returns the total_point and prints out 'One Pair' if true, if false, pass down to isHigh()
        sortedHand=sorted(hand,reverse=True)
        flag=True
        h=2
        total_point=h*13**5+self.point(sortedHand)
        mylist=[]                                       #create an empty list to store ranks
        mycount=[]                                      #create an empty list to store number of count of each rank
        for card in sortedHand:
            mylist.append(card.rank)
        for each in mylist:
            count=mylist.count(each)
            mycount.append(count)
        if mycount.count(2)==2 and mycount.count(1)==3:  #There should be only 2 identical numbers and the rest are all different
            flag=True
            self.player_title_list.append("One Pair")
            self.player_points_list.append(total_point)
        else:
            flag=False
            self.isHigh(sortedHand)

    def isHigh (self, hand):                          #returns the total_point and prints out 'High Card' 
        sortedHand=sorted(hand,reverse=True)
        flag=True
        h=1
        total_point=h*13**5+self.point(sortedHand)
#    mylist=[]                                       #create a list to store ranks
#    for card in sortedHand:
#      mylist.append(card.rank)
        self.player_title_list.append("High Card")
        self.player_points_list.append(total_point)
    
    def result(self, player_names):
        # Results
        #All the indexes with maximum points
        self.winner_index = [i for i, j in enumerate(self.final_points_list) if j == max(self.final_points_list)]
        #Printing the winners along with their hand titles
        
        print("\n\n---------------------------------------Final Showdown--------------------------------------\n")
        for i in range(len(self.winner_index)):
            print("\nWinner: " + str(self.player_names[self.winner_index[i]]) + " wins with a " + str(self.final_title_list[self.winner_index[i]]))
            
    def result_fold(self, player_names, final_player_bet):
        # Get the index of the player who has not folded
        self.final_player_bet = final_player_bet
        #Printing the winners along with their hand titles
        print("\n\n---------------------------------------Final Showdown--------------------------------------\n")
        print("\nWinner: " + str(self.player_names[self.final_player_bet.index(max(self.final_player_bet))]) + " wins")

            
def main ():
    #Welcome message
    print("\n")
    print("-------------------------------------------------------------------------------------------")
    print("-------------------------------------------------------------------------------------------")
    print("------------------------Welcome to the game of Texas Hold'em - Poker-----------------------")
    print("-------------------------------------------------------------------------------------------")
    print("-------------------------------------------------------------------------------------------")
    print("\n")
    
    #getting players details (num of players and their names)
    numPlayers = eval (input ('Enter number of players (between 2 and 6): '))
    while (numPlayers < 2 or numPlayers > 6):
        numPlayers = eval(input ('Invalid option. Please enter number of players (between 2 and 6): '))
    
    player_names = []
    print("\nPlease enter the name of the players:")
    for i in range(numPlayers):
        a = str(input("Player "+ str(i+1) + ": "))
        player_names.append(a)
    
    #Getting the initial buy-in value for each player (same for all players)
    balance = eval(input("\nEnter the Buy-In value for each player (min buy-in = $10K and max buy-in = $10M): "))
    while (balance < 10000 or balance > 10000000):
        balance = eval(input ('Invalid option. Enter the Buy-In value for each player (min buy-in = $10K and max buy-in = $10M): '))

    player_bank = []
    for i in range(numPlayers):
        player_bank.append(balance)
        
        
  	 #Order of Execution:- Blind Bets -> PreFlop Cards -> Betting -> Flop Cards -> Betting -> Turn Card -> Betting -> 
  	 #River Card -> Betting -> Checking the result -> Final Showdown - > Updating the bank balance -> New Round

  	 #Continue playing the game until all players except one have 0 bank balance
    while(player_bank.count(0) != (numPlayers - 1)):
        points = Points(numPlayers, player_bank, player_names)
        game = Card_Display (numPlayers, player_bank, player_names)
        game.pre_flop(numPlayers,player_names)
        
        #If there are atleast 2 people who have not folded yet
        if game.final_player_bet.count(-1) != (numPlayers-1):
            points.points_calculate(game.hands, game.player_names, game.final_player_bet)
            #Declaring the results and updating the bank balance
            print("\nFinal Pot Value for the game: " + str(game.final_pot_value))
            #Pot amount to be distributed among the winners
            pot_distribute = game.final_pot_value / len(points.winner_index)
            for i in range(len(points.winner_index)):
                player_bank[points.winner_index[i]] = player_bank[points.winner_index[i]] + pot_distribute
        #If all except 1 have folded
        else:
            #Declaring the results and updating the bank balance
            print("\nFinal Pot Value for the game: " + str(game.final_pot_value))
            #Pot amount to be distributed among the winners
            pot_distribute = game.final_pot_value
            player_bank[game.final_player_bet.index(max(game.final_player_bet))] = player_bank[game.final_player_bet.index(max(game.final_player_bet))] + pot_distribute
        
        print("\nFinal bank balance of the players: ")
        for i in range(len(player_bank)):
            print("Player " + player_names[i] + "'s bank balance = " + str(int(player_bank[i])))
            
        #Updating the index of the players such that Player 1 is always the dealer
        def rotate(l, n):
            return l[n:] + l[:n]
        player_bank = rotate(player_bank,1)
        player_names = rotate(player_names,1)
        
        
        # Remove the players who have 0 balance remaining 
        numPlayers = numPlayers - player_bank.count(0)
        indexes = [i for i, j in enumerate(player_bank) if j == 0]
        player_bank = [i for i in player_bank if i != 0]
        for index in sorted(indexes, reverse=True):
            del player_names[index]
        
        if numPlayers == 1:
            print ("\n\n" + str(player_names[0]) + " is the final winner with " + str(player_bank[0]) + " in the bank!!\n")
            print("-----------------------------------------GAME OVER-----------------------------------------")
            exit
        else:
            print("\n\n\n\n\n")
            print("-------------------------------------------------------------------------------------------")
            print("-----------------------------------------Next Round----------------------------------------")
            print("-------------------------------------------------------------------------------------------")
            print("\n\n\n")
        
main()