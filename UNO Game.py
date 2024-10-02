import random  # Importer random-modul for at generere tilfældige tal
from time import sleep  # Importer sleep-funktionen fra time-modul til at tilføje forsinkelse i spillet



class Card:
    def __init__(self, color, value):
        self.color = color  # Farven på kortet
        self.value = value  # Værdien på kortet

    def __str__(self):
        return f"{self.color} {self.value}"  # Returner en string værdien af kortet




# Klasse til succ kortet med en særlig effekt, nedarver fra Card-klassen
class Succ(Card):
    def __init__(self):
        super().__init__("Special", "Succ")  # Initialiser med farven "Special" og værdien "Succ"
    
    # Effekten af Succ kortet, som samler og alle kort og uddeler dem tilfældigt så alle får lige mange kort
    def effect(self, players):
        totalCards = sum(len(player.cards) for player in players)  # Totalt antal kort i alle spilleres hænder
        equalCards = totalCards // len(players)  # Antal kort hver spiller skal have efter omfordeling

        # Opret en liste med tomme lister til at holde de nye hænder for hver spiller
        newHands = [[] for _ in range(len(players))]

        # Saml alle kort fra spillerne
        allCards = []
        for player in players:
            allCards.extend(player.cards)
            player.cards.clear()

        # Bland de indsamlede kort
        random.shuffle(allCards)

        # Fordel lige mange kort (equalCards) til hver spiller
        playerIndex = 0
        for i in range(equalCards * len(players)):
            newHands[playerIndex].append(allCards.pop())
            playerIndex = (playerIndex + 1) % len(players)

        # Tildel de nye hænder tilbage til spillerne
        for i in range(len(players)):
            players[i].cards = newHands[i]

        # Hvis der er resterende kort, fordel dem en ad gangen
        playerIndex = 0
        while allCards:
            players[playerIndex].cards.append(allCards.pop())
            playerIndex = (playerIndex + 1) % len(players)

        print("\nSucc-kortet er blevet spillet. Kortene er blevet omfordelt.")




# Klasse til Random kortet med en særlig effekt, nedarver fra Card-klassen
class Random(Card):
    def __init__(self):
        super().__init__("Special", "Random")  # Initialiser med farven "Special" og værdien "Random"
    
    # Effekten af Random kortet: bytter et tilfældigt kort fra den næste spillers hånd med et tilfældigt kort fra bunken
    def effect(self, players, currentPlayerIndex):
        nextPlayerIndex = (currentPlayerIndex + 1) % len(players)  # Indekset for næste spiller
        nextPlayer = players[nextPlayerIndex]  # Næste spiller

        if nextPlayer.cards:  # Hvis næste spiller har kort på hånden
            # Fjern et tilfældigt kort fra næste spillers hånd
            selectedCard = random.choice(nextPlayer.cards)
            nextPlayer.cards.remove(selectedCard)

            # Træk et nyt tilfældigt kort fra bunken
            newCard = Deck().draw()

            # Tilføj det nye kort til næste spillers hånd
            nextPlayer.cards.append(newCard)

            print(f"\nEt tilfældigt kort i {nextPlayer.name}s hånd er blevet erstatet med et nyt kort.")

        else:  # Hvis næste spiller ikke har kort på hånden
            print(f"\nRandom kortet kan ikke spilles, da {nextPlayer.name} ikke har nogen kort på hånden.")




# Klasse til de forskellige normalle kort
class Deck:
    def __init__(self):
        self.cards = []  # Tom liste til at indeholde kortene i bunken
        colors = ['Red', 'Green', 'Blue', 'Yellow']  # Farverne på kortene
        values = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+2', '+4', 'Skip', 'Wildcard']  # Værdierne på kortene
        for color in colors:
            for value in values:
                self.cards.append(Card(color, value))  # Opret og tilføj et kort til bunken for hver kombination af farve og værdi
        self.cards.append(Succ())  # Inkluder Succ-kortet i bunken
        self.cards.append(Random())  # Inkluder Random-kortet i bunken

    # Bland kortene i bunken
    def shuffle(self):
        random.shuffle(self.cards)

    # Træk det øverste kort fra bunken
    def draw(self):
        return self.cards.pop()




# Klasse til spillernes hånd og de funktioner der er
class Hand:
    def __init__(self):
        self.cards = []  # Tom liste til at indeholde kortene på hånden

    # Tilføj et kort til hånden
    def addCard(self, card):
        self.cards.append(card)

    # Fjern et kort fra hånden
    def removeCard(self, card):
        if card in self.cards:
            self.cards.remove(card)
        else:
            pass # incase at der er en fejl

    # Vis kortene på hånden
    def show(self):
        for card in self.cards:
            print(card)




# Klasse til spilleren
class Player(Hand):
    def __init__(self, name):
        super().__init__()  # Initialiser spillers hånd
        self.name = name  # Spillerens navn

    # Træk et kort fra bunken og tilføj det til spillerens hånd
    def drawCard(self, Deck):
        card = Deck.draw()
        self.addCard(card)

    # Vis spillerens hånd, medmindre det er en computer, hvor kun den resterende mængde kort vises
    def showHand(self):
        if self.name == "Spiller":  # Hvis det er en menneskelig spiller
            self.show()  # Vis kortene på hånden
        else:  # Hvis det er en computerstyret spiller
            print(f"{self.name}: {len(self.cards)} kort tilbage")  # Vis antallet af kort på hånden




# Klasse til at vise spillets oplysninger
class GameInfo:
    # Vis det øverste kort på bunken
    def showTopCard(self, topCard):
        print("Øverste kort:", topCard)

    # Vis information om den nuværende spillers tur
    def displayTurnInfo(self, currentPlayer, topCard):
        print("\n" + "=" * 20)
        print(f"Det er {currentPlayer.name}s tur!")  # skriver den nuværende spillers navn
        self.showTopCard(topCard)  # Vis det øverste kort på bunken
        self.showHand(currentPlayer)  # Vis den nuværende spillers hånd

    # Vis spillerens hånd
    def showHand(self, player):
        if player.name == "Spiller":
            print(f"\n{player.name}erens hånd:")
        else:
            print(f"\n{player.name}'s hånd:")
        player.showHand()





# Klasse til at håndtere gyldige kort
class ValidCardHandler:
    # Tjek om et kort er gyldigt i forhold til det øverste kort på bunken
    def validCard(self, card, topCard):
        if card.value in ['+4', 'Wildcard', 'Succ', 'Random']:  # Inkluder 'Succ' og 'Random' som gyldige kort
            return True
        return card.color == topCard.color or card.value == topCard.value

    # Få de gyldige kort for den nuværende spiller
    def getValidCards(self, currentPlayer, topCard):
        return [card for card in currentPlayer.cards if self.validCard(card, topCard)]

    # Håndter tilfælde hvor en spiller ikke har gyldige kort
    def noValidCardsHandler(self, currentPlayer, Deck, topCard):
        print("Ingen kort kan spilles. Trækker fra bunken...")  # Informer om at spilleren trækker et kort fra bunken
        currentPlayer.drawCard(Deck)  # Træk et kort fra bunken til spillerens hånd
        currentPlayer.showHand()  # Vis den nuværende spillers hånd

        # Tjek om det truket kort er gyldigt, hvis ikke, gå videre til næste spiller
        if not self.validCard(currentPlayer.cards[-1], topCard):
            print(f"Et gyldigt kort er ikke blevet trukket. {currentPlayer.name} mister deres tur.")  # Udskriv at spilleren passer
            return True  # Returnwr True for at indikere at turen blev passeret
        else:
            return False  # Returner False for at indikere at turen ikke blev passeret




# Klasse til at håndtere en spillers tur
class TurnHandler(ValidCardHandler):
    def __init__(self):
        super().__init__()

    # Udfør en spillers tur
    def playTurn(self, currentPlayer, validCards, Deck):
        return self.playHumanTurn(validCards) if currentPlayer.name == "Spiller" else self.playComputerTurn(currentPlayer, validCards)

    # Udfør en menneskelig spillers tur
    def playHumanTurn(self, validCards):
        print("Kort der kan spilles:")
        for i in range(len(validCards)):
            print(f"{i+1}: {validCards[i]}")
        choice = int(input("Skriv nummeret på kortet du vil spille: ")) - 1
        return validCards[choice]

    # Udfør en computerspillerstur
    def playComputerTurn(self, currentPlayer, validCards):
        if validCards:  # Hvis der er gyldige kort at spille
            playedCard = random.choice(validCards)  # Vælg et tilfældigt gyldigt kort
            print(f"{currentPlayer.name} spiller: {playedCard}")  # Udskriv hvilket kort der blev spillet
            return playedCard
        else:  # Hvis der ikke er gyldige kort at spille
            print("Ingen kort kan spilles. Trækker fra bunken...")  # Informer om at spilleren trækker et kort fra bunken
            currentPlayer.drawCard(Deck)  # Træk et kort fra bunken til spillerens hånd
            currentPlayer.showHand()  # Vis den nuværende spillers hånd
            return None  # Returnér None for at indikere at ingen kort blev spillet

    # Tjek om der er en vinder af spillet
    def checkWinner(self, currentPlayer):
        if len(currentPlayer.cards) == 0:  # Hvis den nuværende spiller ikke har flere kort på hånden
            print(f"{currentPlayer.name} vinder!")  # Print at den nuværende spiller har vundet
            return True  # Returner True for at indikere at der er en vinder
        return False  # Returner False for at indikere at der ikke er en vinder




# Klasse til at håndtere kort effekter
class CardEffectHandler:
    # håndtere succ effekten
    def succEffectHandler(self, playedCard, players):
        if playedCard.value == 'Succ':  # Hvis der blev spillet et Succ kort
            playedCard.effect(players)  # Udfør effekten af Succ kortet

    def randomEffectHandler(self, playedCard, players, currentPlayerIndex):
        if playedCard.value == 'Random':  # If a "Random" card is played
            playedCard.effect(players, currentPlayerIndex)

    # Opdater den nuværende spillers tur og retning
    def skipAndRotationHandler(self, currentPlayerIndex, direction, playedCard, players, Deck):
        nextPlayerIndex = (currentPlayerIndex + direction) % len(players)  # Indekset for næste spiller
        nextPlayer = players[nextPlayerIndex]  # Næste spiller

        if playedCard is not None:  # Hvis der blev spillet et kort
            if playedCard.value == '+4':  # Hvis der blev spillet et +4 kort
                for i in range(4):
                    nextPlayer.drawCard(Deck)  # Træk 4 kort og tilføj dem til næste spillers hånd
                
                currentPlayerIndex = (currentPlayerIndex + (2 * direction)) % len(players)  # Spring over den næste spillers tur
                print(f"\n{nextPlayer.name} får 4 kort og springer deres tur over.")  # print informationen

            elif playedCard.value == '+2':  # Hvis der blev spillet et +2 kort
                for i in range(2):
                    nextPlayer.drawCard(Deck)  # Træk 2 kort og tilføj dem til næste spillers hånd
                
                currentPlayerIndex = (currentPlayerIndex + direction) % len(players)  # Fortsæt med næste spillers tur
                print(f"\n{nextPlayer.name} får 2 kort.")  # print informationen

            elif playedCard.value == 'Skip':  # Hvis der blev spillet et 'Skip'-kort
                currentPlayerIndex = (currentPlayerIndex + (2 * direction)) % len(players)  # Spring over næste spillers tur
                print(f"\n{nextPlayer.name} springer deres tur over.")  # print informationen

            else:  # Hvis der blev spillet et almindeligt kort
                currentPlayerIndex = (currentPlayerIndex + direction) % len(players)  # Fortsæt med næste spillers tur
        else:  # Hvis ingen kort blev spillet
            currentPlayerIndex = (currentPlayerIndex + direction) % len(players)  # Fortsæt med næste spillers tur
        
        return currentPlayerIndex, direction  # Returner det opdaterede indeks og retning




# Klasse til at styre spillet
class Game(GameInfo, TurnHandler, ValidCardHandler, CardEffectHandler, Deck):
    def __init__(self):
        super().__init__()  # Initialiser overklasserne
        self.Deck = Deck()  # Opret en bunke af kort
        self.Deck.shuffle()  # Bland kortene i bunken
        self.players = [Player("Spiller"), Player("Computer 1"), Player("Computer 2")]  # Opret en liste over spillere
        for i in range(7):  # Giv hver spiller 7 kort for at starte spillet
            for player in self.players:
                player.drawCard(self.Deck)
        self.topCard = self.Deck.draw()  # Træk det øverste kort fra bunken og gem det som det topkortet

    # Start spillet
    def start(self):
        currentPlayerIndex = 0  # Indekset for den nuværende spiller
        direction = 1  # Retningen af spillet (1 for normal, -1 for modsat)

        # Kør spillet indtil der er en vinder
        while True:
            sleep(1)  # Vent i et sekund for at give en visuel forsinkelse
            currentPlayer = self.players[currentPlayerIndex]  # Find den nuværende spiller
            self.displayTurnInfo(currentPlayer, self.topCard)  # Vis information om den nuværende spillers tur
            
            validCards = self.getValidCards(currentPlayer, self.topCard)  # Find gyldige kort for den nuværende spiller
            if not validCards:  # Hvis der ikke er gyldige kort at spille
                if self.noValidCardsHandler(currentPlayer, self.Deck, self.topCard):  # Håndter situationen hvor spilleren ikke har gyldige kort
                    currentPlayerIndex, direction = self.skipAndRotationHandler(currentPlayerIndex, direction, None, self.players, self.Deck)  # Opdater den nuværende spiller og retningen af spillet
                continue  # Fortsæt til næste iteration af løkken
            
            playedCard = self.playTurn(currentPlayer, validCards, self.Deck)  # Udfør den nuværende spillers tur og få det kort der blev spillet
            self.succEffectHandler(playedCard, self.players)  # Opdater spillet hvis succ kortet er blevet spillet
            self.randomEffectHandler(playedCard, self.players, currentPlayerIndex)  # Opdater spillet hvis random kortet er blevet spillet
            currentPlayer.removeCard(playedCard)

            if self.checkWinner(currentPlayer):  # Tjek om den nuværende spiller har vundet
                break  # Hvis der er en vinder, afslut spillet
            
            currentPlayerIndex, direction = self.skipAndRotationHandler(currentPlayerIndex, direction, playedCard, self.players, self.Deck)  # Opdater den nuværende spiller og retningen af spillet



if __name__ == "__main__":
    game = Game()  # Initialiser et nyt spil
    game.start()  # Start spille


    