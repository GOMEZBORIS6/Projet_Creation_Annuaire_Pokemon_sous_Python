#Partie 1: Stock Trends   Projet Groupe2 (2021-2022)
# Membres du Groupe
# GOMEZ Jean-Baptiste Boris
# AUMAGY Léa
# BELLO Dhalil
# GUILLOTIN Nicolas
########################### LIBRARY ##############################
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import dates
import matplotlib.ticker as ticker
from matplotlib.ticker import MultipleLocator
import yfinance as yf
import sys
import urllib.request

########################### Présentation du code ##############################


#Url pour la verification du deuxième argument passée dans la ligne de commande (shell)
myurl='https://adrianchifu.com/teachings/AMSE/MAG1/stocktrends/stock_parameters.txt' 

#On vérifie que exactement deux arguments sont passées dans la ligne de commmande
if (len(sys.argv) != 2): 
    
    print('usage: {} .  We need second argument equal to ==> <url : https://adrianchifu.com/teachings/AMSE/MAG1/stocktrends/stock_parameters.txt>'.format(sys.argv[0]))
    sys.exit()
    
else:
    sys.argv.append(myurl)
    #On vérifie que le second argument est bien l'url qui nous donne les informations sur la cryptomonnaie ETH-USD
    if (sys.argv[1] != myurl):
        print('usage: {} . We need second argument equal to ==> <url : https://adrianchifu.com/teachings/AMSE/MAG1/stocktrends/stock_parameters.txt>'.format(sys.argv[1]))
        sys.exit()
    else:
        # si c'est le cas alors on commence par la lecture des informations dans l'url
        url = sys.argv[1]

        req = urllib.request.urlopen(url)
       
        dat=req.read().splitlines()
        
        lines=[]
        values_cripto=[]
        values_start_date=[]
        values_end_date=[]
        
        # Lecture ligne par ligne puis ajout dans la liste lines
        for line in dat:  
            lines.append(line)
        #On recupere dans la liste la ligne qui nous donne le nom du devise, la date du début et la date de fin
        lign_du_cripto=lines[1]
        lign_start_date=lines[2]
        lign_end_date=lines[3]

        # On effectue une liste de chacune de ses lignes en séparant les chaînes par des espaces
        # ainsi chaque caractère sur une ligne formera une liste pour la ligne indiqué 
        liste_cripto=lign_du_cripto.split()
        liste_start_date=lign_start_date.split()
        liste_end_date=lign_end_date.split()
        
        for a in liste_cripto:
            values_cripto.append(a)
        #print(values_cripto)
        
        for b in liste_start_date:
            values_start_date.append(b)
        #print(values_start_date)
        
        for c in liste_end_date:
            values_end_date.append(c)
        #print(values_end_date)
        
        # On recupère le nom de la devise, la date de début ainsi que la date de fin et on enlève le "b" devant en 
        #utilisant decode().
        # le b signifie bytes donc utilisé pour représenter les données en binaire alors que nous on a besoin de caractère
        # Pour cela on enlève avec decode()
        cripto= values_cripto[2].decode()
        Begin_date=values_start_date[2].decode()
        End_date=values_end_date[2].decode()
              
        #Passage des informations pour recupérer la base de données
        data=yf.Ticker(cripto) 
        frequency='1wk'
        dataDF=data.history(start=Begin_date, end= End_date,interval=frequency)
        df=dataDF.loc[ '2021-07-26':'2021-11-08']

        #dataDF
        
        #titre du graphique
        plt.title("Stock prices for Ethereum (USD)")

        #paramètres axe x
        axes = plt.gca()
        axes.set_xlabel('Date')

        xaxes = plt.gca().get_xaxis()
        xaxes.set_major_locator(MultipleLocator(7))
        xaxes.set_major_formatter(dates.DateFormatter('%Y-%m-%d'))

        plt.xticks(rotation='vertical')


        #paramètres axe y
        axes=plt.gca()
        axes.set_ylabel('Price')
        axes.set_yticks(range(2054,5055,250))
        axes.set_ylim(1900,5100)

        yaxes = plt.gca().get_yaxis()
        fmt = '${x:.0f}' #spécification du format dollars pour les prix à l'ordonnées
        tick = ticker.StrMethodFormatter(fmt)
        yaxes.set_major_formatter(tick)


        # représentation des différentes courbes a afficher
        plt.plot(df['Open'],label='Open', color='steelblue')
        plt.plot(df['Close'], label='Close', color='orange')
        plt.plot(df['Low'], label='Low Price', linestyle=':', color='green')
        plt.plot(df['High'], label='High Price', linestyle=':', color='red')
        plt.legend()

        #Visualisation du graphique
        plt.show()


########################### Fin du code ##############################