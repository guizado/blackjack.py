import random
import math
from graphics import *


class Card():
	'''
	Data abstraction
	Card components: face, suit
	'''

	def __init__(self, face, suit):
		self.face = face
		self.suit = suit
		self.name = face + ' of ' + suit
		if self.face not in ('2', '3', '4', '5', '6', '7', '8', '9',
			'10', 'Jack', 'Queen', 'King', 'Ace'):
				raise TypeError('Card(): Invalid card face')
		if self.suit not in ('Spades', 'Hearts', 'Clubs', 'Diamonds'):
			raise TypeError('Card(): Invalid card suit')
        
	def getFace(self):
		'''Return: face'''
		return self.face
    
	def getSuit(self):
		'''Return: suit'''
		return self.suit
    
	def getName(self):
		'''Return: name'''
		return self.name
		
	def getSymbol(self):
		'''
		Return: Suit symbol
		Used for simplification
		'''
		
		symbols = {'Spades':'♠','Hearts':'♥','Clubs':'♣','Diamonds':'♦'}
		for k, v in symbols.items():
			if self.suit == k:
				return v
				
	def getShortFace(self):
		'''
		Return: first letter/number of the card's face
		Used for simplification
		'''
		if self.face == '10':
			return '10'
		else:
			return self.face[0]
		
	def __repr__(self):
		return self.getShortFace() + self.getSymbol()
    
    
    
class Deck():
	'''
	Data structure for cards
	A new deck contains 52 cards, corresponding to every combination
	of face and suit possible
	'''
	def __init__(self):
		self.deck = []
		for s in ('Hearts', 'Clubs', 'Spades', 'Diamonds'):
			for i in range(2, 11):
				self.deck.append(Card(str(i), s))
			for f in ('Jack', 'Queen', 'King', 'Ace'):
				self.deck.append(Card(f, s))
                                
	def reset(self):
		'''Revert the deck to its original 52 cards'''
		self.deck = Deck().deck
		
	def getRanCard(self):
		'''
		Return: random card object
		Remove: drawn card from the deck
		'''
		if len(self.deck) == 0:
			self.reset()
		return random.choice(self.deck)
		
	def getRanTuple(self, n=1):
		'''
		Return: tuple with n random cards from the deck, 1 by default
		Remove: drawn card from the deck
		'''
		t = ()
		for i in range(n):
			if len(self.deck) == 0:
				self.reset()
			r = random.choice(self.deck)
			self.deck.remove(r)
			t += (r,)
		return t
		
	def __len__(self):
		'''Return: number of undrawn cards'''
		return len(self.deck)
		
	def __repr__(self):
		r = '('
		for c in self.deck:
			r += str(c) + ' '
		return r + ')'  



class CardSprite():
	'''
	Graphical representation for card objects
	Tailored for the Blackjack game
	'''
	def __init__(self, card, win):
		self.card = card
		self.win = win
		self.center = Point(0,0)
		self.createShape()
		self.isDrawn = False
		
	def createShape(self):
		'''Create: All graphical components necessary'''
		'''Rectangle border'''
		self.rect = Rectangle(Point(self.center.getX() - 15, self.center.getY() + 25),
			Point(self.center.getX() + 15, self.center.getY() - 25))
		self.rect.setWidth(3)
		self.rect.setOutline('white')
		'''Face & suit label'''
		self.label_face = Text(Point(self.center.getX() - 3, self.center.getY() - 10),
			self.card.getShortFace())
		self.label_suit = Text(Point(self.center.getX() + 5, self.center.getY() + 10),
			self.card.getSymbol())
		for l in (self.label_face, self.label_suit):
			l.setSize(14)
			l.setTextColor('white')
		self.parts = (self.rect, self.label_face, self.label_suit)
			
	def draw(self, win):
		'''Graphics: draw the various components onto the window'''
		if not self.isDrawn:
			for e in self.parts:
				e.draw(win)
		self.isDrawn = True
			
	def undraw(self):
		'''Graphics: undraw the various components from the window'''
		if self.isDrawn:
			for e in self.parts:
				e.undraw()
		self.isDrawn = False
			
	def teleport(self, new_center):
		'''
		Replace center of the card with a new Point object
		Used for moving the CardSprite on the window
		'''
		self.undraw()
		self.center = new_center
		self.createShape()
		self.draw(self.win)



class CardBack(CardSprite):
	'''
	Graphical representaion for the back of the card, simulating
	a faced-down card
	Tailored for the Blackjack game
	Inherits from CardSprite
	'''
	
	def __init__(self, win):
		self.win = win
		self.center = Point(0,0)
		self.createShape()
		self.isDrawn = False
		
	def createShape(self):
		'''Create all the graphics objects'''
		'''Rectangle border'''
		self.rect = Rectangle(Point(self.center.getX() - 15, self.center.getY() + 25),
			Point(self.center.getX() + 15, self.center.getY() - 25))
		self.rect.setWidth(3)
		self.rect.setOutline('white')
		'''Card back'''
		self.line_1 = Line(Point(self.center.getX() - 15, self.center.getY() + 25),
			Point(self.center.getX() + 15, self.center.getY() - 25))
		self.line_2 = Line(Point(self.center.getX() - 15, self.center.getY() - 25),
			Point(self.center.getX()+ 15, self.center.getY() + 25))
		for e in (self.line_1, self.line_2):
			e.setFill('white')
		self.parts = (self.rect, self.line_1, self.line_2)



class BJHand():
	'''
	Data structure for cards
	'''	
	def __init__(self):
		self.hand = []
		self.bet = 0
		self.done = False
		
	def getCard(self, c):
		return self.hand[c - 1]
		
	def __len__(self):
		return len(self.hand)
		#replacing lenHand
		
	def getDone(self):
		'''
		Return: done
		Used for evaluating when the round is over
		'''
		return self.done
		
	def isDone(self):
		'''
		Set Done to true
		Used for evaluating when the round is over
		'''
		self.done = True
		
	def getCards(self):
		'''Return: list of card objects'''
		return self.hand
		
	def getCardFace(self, c):
		'''Return: card face'''
		return self.hand[c - 1].getFace()
		
	def getBet(self):
		'''Return: bet'''
		return self.bet
		
	def addBet(self, b):
		'''Increment: bet += b'''
		self.bet += b
		
	def addCard(self, card):
		'''Add object: hand += card'''
		self.hand = self.hand + [card]
		
	def removeCard(self, c):
		'''Remove object: hand -= card'''
		del self.hand[c - 1]
		
	def getCardValue(self, card):
		'''Return: Blackjack card value'''
		if card.getFace() == 'Ace':
			return 11
		elif card.getFace().isdigit():
			return int(card.getFace())
		else:
			return 10
	
	def getValue(self):
		'''Return: Sum of blackjack card values'''
		v = 0
		for c in self.hand:
			v += self.getCardValue(c)
		if v > 21:
			for c in self.hand:
				if c.getFace() == 'Ace':
					v -= 10
		return v
		
	def reset(self):
		'''Revert hand object to its original state'''
		self.bet = 0
		self.hand = []
		self.done = False
		
	def __repr__(self):
		h = str(self.hand) + ' '
		if self.bet != 0:
			h = '(' + str(self.bet) + ')  ' + h
		v = str(self.getValue())
		if self.getValue() == 21:
			return h + '<<' + v + '>>'
		elif self.getValue() > 21:
			return h + '>' + v + '<'
		else:
			return h + v
			
			

class Player():
	
	def __init__(self):
		self.hands = [BJHand()]
		self.money = 0
				
	def getMoney(self):
		'''Return: money'''
		return self.money
		
	def __len__(self):
		'''Return: number of hands'''
		return len(self.hands)
		#replacing howManyHands
		
	def getHand(self, h):
		'''Return: h hand object'''
		return self.hands[h - 1]
		
	def getHandCards(self, h=1):
		'''Return: list of cards from hand h'''
		return self.hands[h - 1].getCards()
		
	def getLenHand(self, h=1):
		'''Return: numbers of cards of hand h'''
		return len(self.hands[h - 1])
		
	def getHandValue(self, h=1):
		'''Return: sum of blackjack values from hand h'''
		return self.hands[h - 1].getValue()
		
	def getHandBet(self, h=1):
		'''Return: bet from hand h'''
		return self.hands[h - 1].getBet()
		
	def manageMoney(self, m):
		'''Increment money'''
		self.money += m
		
	def placeBet(self, b, h=1):
		'''
		Add b to the bet of hand h
		Used for placing the bet before the start and for splitting
		and doubling down
		'''
		self.hands[h - 1].addBet(b)
		
	def addHand(self):
		'''
		Add object: hands += Blackjack hand
		Used when splitting
		'''
		self.hands += [BJHand()]
		
	def draw(self, deck, n=1, h=1):
		'''Add object: add random n cards from the deck to hand h'''
		cards = deck.getRanTuple(n)
		for c in cards:
			self.hands[h - 1].addCard(c)
			
	def insertCard(self, h ,c):
		'''
		Add object: add a specific card to hand h
		Used for forcing a card and when splitting
		'''
		self.hands[h - 1].addCard(c)
			
	def testSplit(self, h=1):
		'''
		Bool: can the player split with hand h
		Test if the player can split with hand h
		'''
		if len(self.hands[h - 1]) == 2:
			if (self.hands[h - 1].getCardFace(1) ==
				self.hands[h - 1].getCardFace(2)):
					return True
		else:
			return False
			
	def splitAux(self, h):
		'''
		Remove the second card, add it to another hand
		Auxiliar method for splitting
		'''
		c = self.hands[h - 1].getCard(2)
		self.hands[h].addCard(c)
		self.hands[h - 1].removeCard(2)
		
	def handDone(self, h):
		'''
		Modify: h hand's Done = true
		Used for evaluating when the round is over
		Abstraction
		'''
		self.hands[h - 1].isDone()
		
	def getDone(self, h):
		'''
		Return: Done from hand h
		Checks if the hand is finished
		Abstraction
		'''
		return self.hands[h - 1].getDone()
		
	def reset(self):
		'''Clear the hands and add a fresh one'''
		self.hands = [BJHand()]
		
	def __repr__(self):
		r = 'Player {' + str(self.money) + '}' + '\n'
		for h in self.hands:
			r += '\t' + str(h) + '\n'
		return r
		


class Dealer(Player):
	
	
	def __init__(self):
		self.hidden = None
		super().__init__()
		
	def __repr__(self):
		r = 'Dealer\n'
		for h in self.hands:
			r += '\t' + str(h) + '\n'
		return r
		
	def addHidden(self, c):
		'''
		Used for implementing the dealer's faced-down card mechanic
		'''
		self.hidden = c
			
	def reveal(self):
		'''
		Reveals the faced-down card
		'''
		if self.hidden != None:
			self.insertCard(1, self.hidden)
			self.hidden = None		



class GameControl():
	'''Object for controlling the mechanical flow of the game'''

	def __init__(self):
		self.deck = Deck()
		self.player = Player()
		self.dealer = Dealer()
		self.roundFinished = False
		
	def testBroke(self):
		'''Bool: is the player out of money'''
		return self.player.getMoney() < 1
		
	def testBust(self, h):
		'''Bool: has the player's h hand busted'''
		return self.player.getHandValue(h) > 21
		
	def testDealerBust(self):
		'''Bool: has the dealer's hand busted'''
		return self.dealer.getHandValue() > 21
		
	def testBlackJack(self, h):
		'''Bool: test for blackjack on player's h hand'''
		return self.player.getHandValue(h) == 21
		
	def testTie(self, h):
		'''Bool: test if the player and dealer tied in hand value'''
		return (self.player.getHandValue(h) == 
			self.dealer.getHandValue() and not self.testBust(h))
			
	def winDealer(self, h):
		'''
		Bool: test if who has won the round
		The player wins when:
			Dealer's hand < Player's hand <= 21
			The dealer busts but not the player
		'''
		if (not self.testBust(h) and self.player.getHandValue() >
			self.dealer.getHandValue()) or (not self.testBust(h) and
			self.testDealerBust()):
				return True
		else:
			return False
			
	def lockBet(self, b, h=1):
		'''Add bet and remove that much money from the player'''
		self.player.manageMoney(-b)
		self.player.placeBet(b, h)
		
	def transfer(self):
		'''
		Give (or not) money to the player, depending on the
		bet on his hand and the board situation
		Win situation and received money according to bet:
			Normal win: 2x bet
			Tie: 1x bet
			Blackjack: 2.5x bet
		'''
		for i in range(1, len(self.player) + 1):
			m = self.player.getHandBet(i)
			if self.winDealer(i):
				if self.testBlackJack(i):
					self.player.manageMoney(math.trunc(m + 1.5*m))
				else:
					self.player.manageMoney(2*m)
			if self.testTie(i):
				self.player.manageMoney(m)
					
	def start(self):
		'''
		Starting routine: player draws 2, dealers draw 2, one of which
		is faced-down
		'''
		self.player.draw(self.deck, 2)
		self.dealer.draw(self.deck, 1)
		self.dealer.addHidden(self.deck.getRanCard())
		
	def checkBust(self, h):
		'''
		If h hand is busted, set its Done to true
		'''
		if self.testBust(h):
			self.player.handDone(h)
				
	def hit(self, h=1):
		'''Hit: draw 1 card'''
		self.player.draw(self.deck, 1, h)
		self.checkBust(h)
		
	def stand(self, h):
		'''Stand: hand is finished, no more cards are drawn'''
		self.player.handDone(h)
			
	def doubleDown(self, h=1):
		'''
		Double down: if possible, double your initial bet and draw 1 
		more card, after that the hand is finished
		'''
		self.hit()
		self.lockBet(self.player.getHandBet(h), h)
		self.player.handDone(h)
		
	def split(self, h=1):
		'''
		Split: if the hand has 2 cards with the same face, you may take
		one of the cards and transfer it to a new hand, betting the same
		as the initial bet
		'''
		self.player.addHand()
		self.lockBet(self.player.getHandBet(h), h + 1)
		self.player.splitAux(h)
		
	def getOptions(self, h=1):
		'''
		Return: tuple with characters that represent the available 
		options for a given hand
		h: Hit				s: Stand
		d: DoubleDown		2: Split
		'''
		options = ()
		if not self.testBust(h):
			options += ('h', 's')
			if self.player.getHandBet(h) <= self.player.getMoney():
				if (self.player.getHandValue(h) in (9, 10, 11) and
					self.player.getLenHand(h) == 2 and
						len(self.player) == 1):
						options += ('d',)
				if self.player.testSplit(h):
					options += ('2',)
		return options
		
	def dealerPlay(self):
		'''Dealer draws up to 17'''
		self.dealer.reveal()
		while self.dealer.getHandValue() < 17:
			self.dealer.draw(self.deck, 1, 1)
			
	def restart(self):
		'''Revert GameControl back to its original form'''
		self.player.reset()
		self.dealer.reset()
		
	def getPlayerCards(self, h=1):
		'''
		Return: player's cards from hand h
		Abstraction
		'''
		
		return self.player.getHandCards(h)
		
	def getPlayerHand(self, h=1):
		'''
		Return: h hand object
		Abstraction
		'''
		return self.player.getHand(h)
			
	def getDealerHand(self):
		'''
		Return: dealer's hand object
		Abstraction
		'''
		return self.dealer.getHand(0)
				
	def getDealerCards(self):
		'''
		Return: dealer's cards
		Abstraction
		'''
		return self.dealer.getHandCards(1)
		
	def addPlayerHand(self):
		'''
		Add object: give the player a new hand
		Abstraction
		'''
		self.player.addHand()
		
	def getPlayerMoney(self):
		'''
		Return: player's money
		Abstraction
		'''
		return self.player.getMoney()
		
	def controlWallet(self, m):
		'''
		Modify: player's money
		Abstraction
		'''
		self.player.manageMoney(m)
		
	def checkFinished(self):
		'''
		Bool: check if all the hands are finished
		Used for ending the round
		'''
		f = ()
		for i in range(1, len(self.player) + 1):
			f += (self.player.getDone(i),)
		return all(f)
			
	def __repr__(self):
		s = str(self.dealer) + '\n' + str(self.player)
		return s

#_________________________User Interface________________________________
#_______________________________________________________________________

class Button():
	'''Graphical representation for rectangular buttons'''
	
	def __init__(self, p1, p2, label, win):
		self.win = win
		self.body = Rectangle(p1, p2)
		self.body.setOutline('white')
		self.body.setWidth(5)
		self.label = Text(self.body.getCenter(), label)
		self.label.setTextColor('white')
		self.isDrawn = False
		
	def getLabel(self):
		'''Return: button's text'''
		return self.label.getText()
				
	def isClicked(self):
		'''Graphics: click animation'''
		self.body.setFill('white')
		self.label.setTextColor('black')
		time.sleep(0.1)
		self.body.setFill('black')
		self.label.setTextColor('white')
		
	def checkClick(self, click):
		'''
		Bool: Takes a Point object as an argument and verifies if the 
		button has been clicked
		'''
		p1 = self.body.getP1()
		p2 = self.body.getP2()
		if click == None or not self.isDrawn:
			return False
		elif (p1.getX() < click.getX() < p2.getX() and
			p2.getY() < click.getY() < p1.getY()):
				self.isClicked()
				return True
		else:
			return False
	
	def draw(self, win):
		'''Graphics: draws all button elements onto the window'''
		if not self.isDrawn:
			for e in (self.body, self.label):
				e.draw(win)
			self.isDrawn = True
			
	def undraw(self):
		'''Graphics: undraws all the button elements from the window'''
		if self.isDrawn:
			for e in (self.body, self.label):
				e.undraw()
			self.isDrawn = False



class ButtonCircle(Button):
	'''
	Graphical representation for circular buttons
	Inherits from rectangular buttons
	'''
	
	def __init__(self, c, r, label, win):
		self.win = win
		self.body = Circle(c, r)
		self.body.setOutline('white')
		self.body.setWidth(3)
		self.label = Text(c, label)
		self.label.setTextColor('white')
		self.isDrawn = False
		
	def checkClick(self, click):
		'''Bool: takes a Point object as an argument (for circles) and 
		verifies if the button has been clicked'''
		c = self.body.getCenter()
		if (((click.getX()-c.getX())**2 + (click.getY()-c.getY())**2)
			< self.body.getRadius()**2 and self.isDrawn):
				self.isClicked()
				return True
		else:
			return False



class Menu():
	'''Graphical representation for the menu window'''
	
	def __init__(self, win):
		self.win = win
		self.title = Text(Point(250, 150), '♠ ♥ ♣ ♦ Blackjack ♦ ♣ ♥ ♠')
		self.title.setSize(32)
		#self.title.setFace('arial') pq q isto n funciona 
		self.title.setTextColor('white')
		self.startButton = Button(Point(200, 300), Point(300, 250),
			'Start', self.win)
		self.isOpen = False
					
	def openMenu(self):
		'''Graphics: draw the elements in the menu'''
		if not self.isOpen:
			for e in (self.title,self.startButton):
				e.draw(self.win)
		self.isOpen = True
				
	def closeMenu(self):
		'''Graphics: undraw the elements in the menu'''
		if self.isOpen:
			for e in (self.title,self.startButton):
				e.undraw()
		self.isOpen = False
		
		

class HandSprite:
	'''Graphical representation for the BJHand object'''
	
	def __init__(self, center, n, win):
		self.center = center
		self.win = win	
		self.n = n
		self.bet = 0
		self.createBox()
		self.sprites = ()
		self.isDrawn = False
		self.isChosen = False
		
	def createBox(self):
		'''Graphics: creates a rectangle and text object, the bet box'''
		x = self.center.getX()
		y = self.center.getY()
		'''Box'''
		self.box = Circle(Point(x, y + 20), 15)
		self.box.setOutline('white')
		'''Bet Label'''
		self.bet_label = Text(Point(x, y + 20), str(self.bet))
		self.bet_label.setTextColor('white')
		'''Value Label'''
		self.value_label = Text(Point(x, y - 70), '')
		self.value_label.setTextColor('white')
		'''Chosen box'''
		self.chosen = Rectangle(Point(x - 40, y + 40),
			Point(x + 40, y - 80))
		self.chosen.setOutline('white')
		
	def drawBox(self):
		'''Graphics: draw the box'''
		if not self.isDrawn:
			self.box.draw(self.win)
			self.bet_label.draw(self.win)
			self.value_label.draw(self.win)
			self.isDrawn = True
			
	def undrawBox(self):
		'''Graphics: undraw the box'''
		if self.isDrawn:
			self.box.undraw()
			self.bet_label.undraw()
			self.value_label.undraw()
			if self.isChosen:
				self.chosen.undraw()
			self.isDrawn = False
			
	def setChosen(self, bool_):
		'''Changes isChosen to bool_'''
		self.isChosen = bool_
			
	def updateChosen(self):
		'''
		Graphics: update the chosen box to fit the number of cards 
		in hand
		'''
		x = self.center.getX()
		y = self.center.getY()
		l = len(self.sprites) - 2
		self.chosen = Rectangle(Point(x - 40 - 18*l, y + 40),
			Point(x + 40 + 18*l, y - 80))
		self.chosen.setOutline('white')		
		
	def getBet(self):
		'''Return: bet'''
		return self.bet
				
	def updateBet(self, b):
		'''
		Sets the hand bet to a specific value
		Graphics: update bet label
		'''
		self.bet = b
		self.bet_label.setText(str(self.bet))
		
	def doubleBet(self):
		'''
		Double bet value
		Graphics: update bet label
		'''
		self.updateBet(self.bet * 2)
				
	def cardPosition(self, len_hand):
		'''
		Returns a list containing Point objects corresponding
		to the positioning of the cards
		'''
		p1 = []
		p2 = []
		x = self.center.getX()
		y = self.center.getY() - 30
		if len_hand % 2 == 0:
			i = (len_hand / 2) - 1 
			while i > -1:
				p1 += [Point(x + 17.5 + 35 * i, y)]
				p2 += [Point(x - 17.5 - 35 * i, y)]
				i -= 1
			return p2 + p1[::-1]
		else:
			i = len_hand // 2
			while i > 0:
				p1 += [Point(x + 35 * i, y)]
				p2 += [Point(x - 35 * i, y)]
				i -= 1
			return p2 + [Point(x, y)] + p1[::-1]
		
	def update(self, gc):
		'''Graphics: updates the card sprites and the box position'''
		'''Draw Box'''
		self.drawBox()
		'''Cards'''
		if len(self.sprites) > 0:
			for sprite in self.sprites:
				sprite.undraw()
			self.sprites = ()
		cards = gc.getPlayerCards(self.n)#list
		for c, p in zip(cards, self.cardPosition(len(cards))):
			cs = CardSprite(c, self.win)
			self.sprites += (cs,)
			cs.teleport(p)
		'''Value label'''
		value = str(gc.getPlayerHand(self.n).getValue()) #ABSTRAÇÃO CARALHO
		self.value_label.setText(value)
		'''Chosen'''
		if self.isChosen:
			self.chosen.undraw()
			self.updateChosen()
			self.chosen.draw(self.win)
		elif not self.isChosen:
			self.chosen.undraw()
			
	def closeHand(self):
		'''Graphics: clean all the sprites associated with the hand'''
		for s in self.sprites:
			s.undraw()
		self.undrawBox()
		
		
		
class DealerSprite(HandSprite):
	'''Graphical representation for dealer's BJHand object'''
	
	def __init__(self, win):
		self.win = win
		self.center = Point(250, 100)
		self.createBox()
		self.sprites = ()
		self.isDrawn = False
		
	def createBox(self):
		'''Graphics: creates the value label'''
		self.value_label = Text(Point(self.center.getX(),
			self.center.getY() - 70), '')
		self.value_label.setTextColor('white')
		
	def drawLabel(self):
		'''Graphics: draw the value label'''
		if not self.isDrawn:
			self.value_label.draw(self.win)
		self.isDrawn = True
	
	def undrawLabel(self):
		'''Graphics: undraw the value label'''
		if self.isDrawn:
			self.value_label.undraw()
		self.isDrawn = False
				
	def update(self, gc):
		'''Graphics: update the dealer's sprites and his hidden card'''
		'''Value Label'''
		self.drawLabel()
		self.value_label.setText(gc.dealer.getHandValue(1))
		'''Cards and Flipped Card'''
		if len(self.sprites) > 0:
			for sprite in self.sprites:
				sprite.undraw()
			self.sprites = ()
		cards = gc.getDealerCards() #list
		h = 0
		if not gc.checkFinished():
			h += 1
		for c, p in zip(cards, self.cardPosition(len(cards) + h)):
			cs = CardSprite(c, self.win)
			self.sprites += (cs,)
			cs.teleport(p)
		if not gc.checkFinished(): #Esta parte ta meia estranha
			flipped_card = CardBack(self.win)
			self.sprites += (flipped_card,)
			l = len(self.sprites)
			flipped_card.teleport(self.cardPosition(l)[-1])
			
	def closeHand(self):
		'''Graphics: cleans all dealer's sprites'''
		for s in self.sprites:
			s.undraw()
		self.undrawLabel()
		


class BettingStage:
	'''
	Graphical representation for the betting stage that happens
	before every round
	'''
	
	def __init__(self, win):
		self.win = win
		self.isOpen = False
		self.money = 0
		'''Wallet'''
		self.wallet_label = Text(Point(50, 300), str(self.money))
		self.wallet_label.setTextColor('white')
		self.wallet_circle = Circle(Point(50, 300), 30)
		self.wallet_circle.setOutline('white')
		self.switch = False
		'''Bet buttons'''
		self.bets = (
			ButtonCircle(Point(50, 200), 15, '5', win),
			ButtonCircle(Point(50, 160), 15, '10', win),
			ButtonCircle(Point(50, 120), 15, '20', win),
			ButtonCircle(Point(50, 80), 15, '50', win))
		'''Cancel and Go buttons'''
		self.cancel = Button(Point(40, 250), Point(60, 230), 'X',
			self.win)
		self.go = Button(Point(30,40),Point(70,20),'Go',
			self.win)
		self.switch2 = False
		'''Bet Box'''
		self.bet = 0
		self.bet_box = Rectangle(Point(225, 225), Point(275, 275))
		self.bet_box.setOutline('white')
		self.bet_label = Text(Point(250, 250), str(self.bet))
		self.bet_label.setTextColor('white')
		
	def getDefaultBet(self):
		'''Return: initial bet'''
		return self.bet
		
	def resetBet(self):
		'''Sets the bet to zero and update its label'''
		self.bet = 0
		self.bet_label.setText(str(self.bet))
		
	def drawWallet(self):
		'''Graphics: draw the wallet'''
		if not self.switch:
			self.wallet_label.draw(self.win)
			self.wallet_circle.draw(self.win)
			self.switch = True
			
	def undrawWallet(self):
		'''Graphics: undraw the wallet'''
		if self.switch:
			self.wallet_label.undraw()
			self.wallet_circle.undraw()
			self.switch = False
			
	def drawBets(self):
		'''Graphics: draw bets'''
		if not self.isOpen:
			for e in ((self.bet_box, self.bet_label) + self.bets):
				e.draw(self.win)
			self.isOpen = True
	
	def undrawBets(self):
		'''Graphics: undraw bets'''
		if self.isOpen:
			for e in ((self.bet_box, self.bet_label) + self.bets):
				e.undraw()
			self.isOpen = False
		
	def updateBetAndMoney(self, b):
		'''
		Updates the wallet and the bet values after the user has
		clicked a bet button
		Graphics: update wallet and bet labels
		'''
		self.money -= b
		self.bet += b
		self.bet_label.setText(str(self.bet))
		self.wallet_label.setText(str(self.money))
						
	def clickedCancel(self):
		'''
		Graphics: when the user has clicked the cancel button, reverts
		the bet
		'''
		self.money += self.bet
		self.bet = 0
		self.bet_label.setText(str(self.bet))
		self.wallet_label.setText(str(self.money))
					
	def showGoCancel(self):
		'''Graphics: draws the go and cancel buttons'''
		self.go.draw(self.win)
		self.cancel.draw(self.win)
		self.switch2 = True
		
	def hideGoCancel(self):
		'''Graphics: undraws the go and cancel buttons'''
		self.go.undraw()
		self.cancel.undraw()
		self.switch2 = False
			
	def clickBet(self, click):
		'''
		Graphics: Waits for a click on the betting stage screen and 
		carries out events appropriately, then returns 1 or 0 to control
		the main loop
		'''
		if self.cancel.checkClick(click):
			self.clickedCancel()
			self.hideGoCancel()
		if self.go.checkClick(click):
			self.hideGoCancel()
			return 1
		for e in self.bets:
			if e.checkClick(click):
				if self.money >= int(e.getLabel()):
					self.updateBetAndMoney(int(e.getLabel()))
					self.showGoCancel()
		return 0
		
	def updateWallet(self, gc):
		'''
		Update money
		Graphics: update wallet label
		'''
		m = gc.getPlayerMoney()
		self.money = m
		self.wallet_label.setText(str(m))



class Table():
	'''
	Graphic representation of the cards on the table
	'''
	
	def __init__(self, win):
		self.win = win	
		self.hands = [HandSprite(Point(250,450), 1, win)]
		self.isOpen = False
		self.dealer_sprite = DealerSprite(win)
		self.currentHand = 1
		'''Option buttons'''
		self.opts = (
			Button(Point(430, 240), Point(490, 210), 'Hit', win),
			Button(Point(430, 200), Point(490, 170), 'Stand', win),
			Button(Point(430, 280), Point(490, 250), 'Double', win),
			Button(Point(430, 320), Point(490, 290), 'Split', win))
			
	def setDefaultBet(self, b):
		'''
		Transfer the betting stage bet into the table
		Abstraction
		'''
		self.hands[0].updateBet(b)
		
	def addHandSprite(self, gc):
		'''
		Graphics: Adds another hand sprite and updates the screen 
		accordingly, preparing for split
		'''
		l = len(self.hands)
		self.hands += [HandSprite(Point(250, 450 - l*130), l + 1, self.win)]
		self.hands[-1].updateBet(self.hands[0].getBet())
		for h in self.hands:
			h.update(gc)
		
	def update(self, gc):
		'''Update all hand, dealer sprites and option buttons'''
		'''Manage the chosen hand'''
		self.hands[self.currentHand - 1].setChosen(True)
		if gc.getPlayerHand(self.currentHand).getDone(): #ABSTRAÇÃO
			print('yay') 
			if gc.checkFinished():
				pass 
			else:
				self.hands[self.currentHand - 1].setChosen(False)
				self.hands[self.currentHand].setChosen(True)
				self.currentHand += 1
		'''Update hands'''
		for h in self.hands:
			h.update(gc)
		self.dealer_sprite.update(gc)
		'''Options'''
		opts = gc.getOptions(self.currentHand)
		for b in self.opts:
			b.undraw()
		if gc.checkFinished():
			return None
		if 'h' in opts:
			self.opts[0].draw(self.win)
		if 's' in opts:
			self.opts[1].draw(self.win)
		if 'd' in opts:
			self.opts[2].draw(self.win)
		if '2' in opts:
			self.opts[3].draw(self.win)
			
	def clickTable(self, click, gc):
		'''
		Graphics: takes a click and checks if any of the buttons 
		in the table were pressed, if so, carry events accordingly
		'''
		opts = gc.getOptions(self.currentHand)
		if self.opts[0].checkClick(click) and 'h' in opts:
			gc.hit(self.currentHand)
		if self.opts[1].checkClick(click) and 's' in opts:
			gc.stand(self.currentHand)
		if self.opts[2].checkClick(click) and 'd' in opts:
			gc.doubleDown(self.currentHand)
			self.hands[self.currentHand - 1].doubleBet()
		if self.opts[3].checkClick(click) and '2' in opts:
			gc.split(self.currentHand)
			self.addHandSprite(gc)
			
	def closeTable(self, gc):
		'''
		Graphics: Cleans all the sprites from the table screen
		'''
		for h in self.hands:
			h.closeHand()
		self.dealer_sprite.closeHand()
		self.dealer_sprite = DealerSprite(self.win)
		self.hands = [HandSprite(Point(250,450), 1, self.win)]
		self.currentHand = 1
		


class Main(): 
	
	def __init__(self):
		self.win = GraphWin('BlackJack', 500, 500)
		self.win.setBackground('black')
		self.menu = Menu(self.win)
		self.gc = GameControl()
		self.gc.controlWallet(100)
		self.bs = BettingStage(self.win)
		self.table = Table(self.win)
		self.flag = 0
		self.mainLoop()
		
	def menuLoop(self):
		'''Menu loop'''
		while True:
			self.menu.openMenu()
			click = self.win.getMouse()
			if self.menu.startButton.checkClick(click): #Abstração
				self.flag = 1
				self.menu.closeMenu()
				break
				
	def betLoop(self):
		'''Bet stage loop'''
		self.bs.updateWallet(self.gc)	
		self.bs.drawWallet()
		self.bs.drawBets()
		bet_flag = 0
		while bet_flag == 0:
			click = self.win.getMouse()
			bet_flag = self.bs.clickBet(click)
		self.table.setDefaultBet(self.bs.getDefaultBet())
		self.gc.lockBet(self.bs.getDefaultBet())
		self.bs.undrawBets()
		self.bs.resetBet()

	def tableLoop(self):
		'''Game stage loop'''
		self.gc.start()
		while True:
			self.table.update(self.gc)
			click = self.win.getMouse()
			self.table.clickTable(click, self.gc)
			print(self.gc)
			print(self.table.currentHand)
			print(self.gc.player.hands[0].done)
			print('\n---\n')
			self.bs.updateWallet(self.gc)
			if self.gc.checkFinished():
				self.gc.dealerPlay()
				self.table.update(self.gc)
				self.win.getMouse()
				self.gc.transfer()
				self.gc.restart()
				self.table.closeTable(self.gc)
				break
			
	def mainLoop(self):
		'''Main loop linking the various screens'''
		while True:
			self.menuLoop()
			if self.flag == 1:
				while True:
					self.betLoop()
					self.tableLoop()
					if self.gc.getPlayerMoney() < 5:
						broke = Text(Point(250,250),
							'You\'re out of money, better luck next time')
						broke.setTextColor('white')
						broke.draw(self.win)
						self.win.getMouse()
						break
				break
			elif self.flag == 0:
				break
	
	
				
Main()

