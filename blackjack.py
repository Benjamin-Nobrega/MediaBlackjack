import math
from random import shuffle, sample
from numba import jit, cuda

deck2 = ["Ah", "Ad", "Ac", "As",
            "2h", "2d", "2c", "2s",
            "3h", "3d", "3c", "3s",
            "4h", "4d", "4c", "4s",
            "5h", "5d", "5c", "5s",
            "6h", "6d", "6c", "6s",
            "7h", "7d", "7c", "7s",
            "8h", "8d", "8c", "8s",
            "9h", "9d", "9c", "9s",
            "10h", "10d", "10c", "10s",
            "Jh", "Jd", "Jc", "Js",
            "Qh", "Qd", "Qc", "Qs",
            "Kh", "Kd", "Kc", "Ks"]

def prepararDeck():
    return(deck2.copy())


deck = prepararDeck()




def deckInit(deck):
   
    card_values = {
    'A': 11,  # Ás pode ser 1 ou 11, mas vou definir como 11 por padrão
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'J': 10,
    'Q': 10,
    'K': 10
}

    deck_values = {card: card_values[card[:-1]] for card in deck}
    return(deck_values)

deck_values = deckInit(deck)

class Jogador():
    def __init__(self, money) -> None:
        self.value = 0
        self.money = money
        self.deck = []
        self.continuar = True
        for card in self.deck:
            self.value += deck_values[card]
        pass
    def stop(self):
        self.continuar = False
    def more(self):
        novacarta = darCarta(deck, 1)[0]
        self.value += deck_values[novacarta] 
        self.deck.append(novacarta)
    def double(self):
        novacarta = darCarta(deck, 1)[0]
        self.value += deck_values[novacarta] * 2
        self.deck.append(novacarta)
        
    def jogar(self):
        self.deck = darCarta(deck, 2)
        while self.continuar:
            if self.value == 10:
                self.double()
            elif self.value <= 15:
                self.more()
            else:
                self.stop()
    def reiniciar(self):
        self.value = 0
        self.continuar = True
        global deck
        deck = prepararDeck()


    def ganharDinheiro(self, dinheiro):
        self.money += dinheiro
    def perderDinheiro(self, dinheiro):
        self.money -= dinheiro
    
def darCarta(deck, numCards):
    shuffle(deck)
    newArr = sample(deck, numCards)
    for card in newArr:
        if card in deck:
            deck.remove(card)
    return(newArr)

def displayCard(card):
    cardFullName = ""
    match(card[0]):
        case "A":
            cardFullName += "Ace of "
        case "J":
            cardFullName += "Jack of "
        case "Q": 
            cardFullName += "Queen of "
        case "K":
            cardFullName += "King of "
        case "1":
            cardFullName += "10 of "
        case default:
            cardFullName += f"{card[0]} of "

    match(card[-1]):
        case "h":
            cardFullName += "hearts"
        case "d":
            cardFullName += "diamonds"
        case "c":
            cardFullName += "clubs"
        case "s":
            cardFullName += "spades"
    return(cardFullName)

def perto21(value):
    if value > 21:
        return 99
    else:
        return 21-value

def comecoDoJogo():
    dinheiroDoCaba = 100
    quantidadeApostada = 1
    eu = Jogador(dinheiroDoCaba)
    num_jogos = 0
    while eu.money >0:
        num_jogos+=1
        eu.perderDinheiro(quantidadeApostada)
        eu.jogar()
        #print(eu.value)
        #print(eu.deck)
        
        
        dealer = Jogador(9999)
        dealer.jogar()
       # print(dealer.value)
        #print(dealer.deck)
        #ver que tirou mais perto de 21
        
        
        eu21 = perto21(eu.value)
        dealer21 = perto21(dealer.value)
        
        if dealer21 == eu21:
            if eu21 > 90:
                #dealer ganhou
                #print("A casa ganhou")
                pass
            else:
                #dinheiro de volta
                #print("Tome seu dinheiro de volta")
                eu.ganharDinheiro(quantidadeApostada)
        elif dealer21 < eu21:
            #dealer ganhou
            #print("A casa ganhou")
            pass
        elif dealer21 > eu21:
            #eu ganhei
           #print("Você ganhou")
            eu.ganharDinheiro(quantidadeApostada*2)
        eu.reiniciar()
        dealer.reiniciar()
    return num_jogos
    

def main():
    lista = []
    for i in range(1000):
    #lista com números de jogos até perder
        lista.append(comecoDoJogo())
    media = sum(lista)/len(lista)
    print(media)
    
if __name__ == "__main__":
    main()
 