# Partie 2: Pokemon Yearbook  Projet Groupe2 (2021-2022)
# Membres du Groupe
# GOMEZ Jean-Baptiste Boris
# AUMAGY Léa
# BELLO Dhalil
# GUILLOTIN Nicolas
########################### LIBRARY ##############################################

import io  # ouverture de flux entrants et sortant
from json import decoder  # lecture de données json
from os import name
from io import BytesIO  # ouverture de flux entrants et sortant
import urllib3  # pour passer des url
import tempfile  # pour générer des fichiers temporaire
import json  # encodeur et decodeur jsonfile
import sys
import shutil
import zipfile as zp  # pour fichier zippé
import requests as rq
#from unidecode import unidecode

from urllib.request import urlopen, URLError  # lire des fichiers avec url
from fpdf import FPDF  # pdf
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont

#from validator_collection import validators, checkers

########################### Présentation du code ##########################################
# Remarque important: On a fait le projet en vscode mais il ne reconnait par la police 'Arial' mais plutôt 'helvetica' et les deux sont les même donc c'est seulement le nom qui change
# On arrive à accerder au logo et l'image placeholder sans extraire le fichier data.zip mais pas les polices donc il faut extraire les polices et le mettre dans le
# même emplacement que ce fichier pour que les fonts soit reconnu. Merci

# Arguments
url_json = 'https://adrianchifu.com/teachings/AMSE/MAG1/projpokedex/pokedex.json'
url_data = 'https://adrianchifu.com/teachings/AMSE/MAG1/projpokedex/depend/data.zip'
log_file = 'PYlog.txt'
pdf_file = 'PYearbook.pdf'


if (len(sys.argv) != 5):

    print(
        'usage: {} .  We need second argument equal to ==> <url : https://adrianchifu.com/teachings/AMSE/MAG1/projpokedex/pokedex.json>, third argument equal to ==> <url : https://adrianchifu.com/teachings/AMSE/MAG1/projpokedex/depend/data.zip, fourth argument equal to ==> PYlog.txt,  fifth argument equal to ==> PYearbook.pdf >'.format(sys.argv[0]))
    sys.exit()

else:
    sys.argv.append(url_json)
    sys.argv.append(url_data)
    sys.argv.append(log_file)
    sys.argv.append(pdf_file)
    # On vérifie que le second argument est bien l'url qui nous donne les informations sur la cryptomonnaie ETH-USD
    if (sys.argv[1] != url_json):
        print(
            'usage: {} . We need second argument equal to ==> <url : https://adrianchifu.com/teachings/AMSE/MAG1/projpokedex/pokedex.json>'.format(sys.argv[1]))
        sys.exit()

    elif (sys.argv[2] != url_data):
        print(
            'usage: {} . We need third argument equal to ==> <url :https://adrianchifu.com/teachings/AMSE/MAG1/projpokedex/depend/data.zip>'.format(sys.argv[2]))
        sys.exit()
    elif (sys.argv[3] != log_file):
        print('usage: {} . We need fourth argument equal to ==> PYlog.txt>'.format(
            sys.argv[3]))
        sys.exit()
    elif (sys.argv[4] != pdf_file):
        print('usage: {} . We need fifth argument equal to ==> PYearbook.pdf>'.format(
            sys.argv[4]))
        sys.exit()
    # Lecture du fichier zippé
    else:
        zip_file_url = sys.argv[2]
        r = rq.get(zip_file_url)
        z = zp.ZipFile(io.BytesIO(r.content))
        logo = z.open('logo.png')  # recupération du logo pokemon pour l'entête
        # recupération du placeholder image pour l'entête
        placeholder_img = z.open('placeholder.png')

        policeBold = z.open('DejaVuSansCondensed-Bold.ttf')
        police = z.open('DejaVuSansCondensed.ttf', 'r')

        # fp = tempfile.NamedTemporaryFile('w+',dir='C:/Users/HP/Documents/Atest_Python/projet python',delete=False)
        # #fp1  = tempfile.TemporaryFile()
        # # shutil.copyfile(police,fp)
        # for line in police:
        #     fp.write(line)

        # fp=shutil.unpack_archive(r,'DejaVuSansCondensed.ttf',format="zip")
        #fp = shutil.copyfile(scr=zip_file_url,dst='DejaVuSansCondensed.ttf')
        # fp1=shutil.copyfile(scr=zip_file_url,dst='DejaVuSansCondensed-Bold.ttf')
        # DejavS=z.open('DejaVuSansCondensed.ttf', 'r')
        # DejavSbold=z.open('DejaVuSansCondensed-Bold.ttf','r')

        # clés necessaires pour l"affichage
        keys = ["name", "height", "weight", "img", "type", "weaknesses"]

        # fonction de filtrage des pokemons avec comme caractéristiques la liste des clés

        def filterPokemon(pok_element):
            values = {}
            for key in keys:
                values[key] = pok_element[key]
            return values

        # lecture des données json
        # remarque: les données json sont de type dict(dictionnaire)
        dat_json = sys.argv[1]
        with urlopen(dat_json) as f:
            data = json.loads(f.read().decode('utf8'))
            pokemon = data["pokemon"]
            # On créer une nouvelle base de données avec les pokemons mais avec seulement les clés utiles (keys)
            data = list(map(filterPokemon, pokemon))

        # on trie cette base de données selon la clés (name) # remarque : on a une liste de dictionnaire et chaque dictionnaire est un pokemon
        newlist = sorted(data, key=lambda k: k['name'])
        # print(newlist)
        # print(data[0]["img"])
        # for pok in data [2]:
        print("Nous commençons la création du pdf avec les données!!!")
        # classe  pdf pour la création du pdf
        class PDF(FPDF):

            def header(self):  # création de l'entête du pdf
                # Rendering logo:
                self.image(logo, 10, 10, 25)
                # text en couleur noir
                self.set_text_color(0, 0, 0)
                # Setting font: helvetica bold 15
                self.set_font("helvetica", "B", 15)
                # Moving cursor to the right:
                # self.cell(80)
                # Printing title:
                self.cell(0, 10, "Pokemon Yearbook - Gr.2",
                        border=True, ln=1, align='C')
                # Performing a line break:
                self.ln(5)  # decalage de 5mm vers le bas

            # fonction principale
            def create_table(self, data):
                pdf.add_page()  # ajout de page
                nbr_cellule = 0
                i = 0
                a = 27  # position ordonnées
                b = 25  # position ordonnées
                for pok in data[:50]:

                    # fonction de verification de l'url de l'image de chacune des pokemons pour savoir si on doit utiliser l'image placeholder ou pas
                    def validate_web_url(url):

                        try:
                            urlopen(url)
                            return self.image("{img}".format(img=pok["img"]), w=30, h=30)
                        except:
                            return self.image(placeholder_img, w=30, h=30)
                # cellule 1====> sur la ligne
                    pok = data[i]
                    self.set_text_color(0, 0, 0)
                    self.cell(93, 40, '', 1)
                    self.set_font('helvetica', 'B', 8)
                    self.set_xy(12, a)
                    img1 = pok['img']
                    validate_web_url(img1)
                    self.set_xy(0, a)
                    self.cell(50.5, 4.28, 'Type:', 0, 1, 'R')
                    self.set_font('helvetica', '', 8)
                    self.set_xy(41, a+3.5)
                    self.cell(42.5, 4.28, '{type}'.format(
                        type=",".join(pok["type"])), 0, 1)
                    self.set_font('helvetica', 'B', 8)
                    self.cell(42.5, 4.28, 'Height:', 0, 1, 'R')
                    self.set_font('helvetica', '', 8)
                    self.cell(41.5, 4.28, '{height}'.format(
                        height=pok["height"]), 0, 1, 'R')
                    self.set_font('helvetica', 'B', 8)
                    self.cell(43, 4.28, 'Weight:', 0, 1, 'R')
                    self.set_font('helvetica', '', 8)
                    self.set_xy(41, a+20)
                    self.cell(41, 4.28, '{weight}'.format(
                        weight=pok["weight"]), 0, 1)
                    self.set_font('helvetica', 'B', 8)
                    self.cell(50.5, 4.28, 'Weaknesses:', 0, 1, 'R')
                    self.set_font('helvetica', '', 8)
                    self.set_xy(41, a+29)
                    self.cell(50.5, 4.28, '{weaknesses}'.format(
                        weaknesses=",".join(pok['weaknesses'])), 0, 1)
                    self.add_font(
                        'DejaVuB', '', 'DejaVuSansCondensed-Bold.ttf', uni=True)
                    self.set_font('DejaVuB', '', 11)
                    #self.set_font('helvetica', 'B', 11)
                    self.set_text_color(255, 0, 0)
                    self.set_xy(11, a+32.5)
                    self.cell(28.5, 0, 'Name:', 0, 1)
                    #self.set_font('helvetica', '', 11)
                    self.set_xy(11, a+34)
                    self.add_font(
                        'DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
                    self.set_font('DejaVu', '', 11)
                    try:
                        self.cell(28.5, 5.28, '{name}'.format(
                            name=pok["name"]), 0, 0)
                    except:
                        continue
                    nbr_cellule += 1
                    i += 1

                    # cellule2 ====> sur la ligne
                    pok = data[i]
                    self.set_text_color(0, 0, 0)
                    self.set_xy(103, b)
                    self.cell(93, 40, border=1)
                    self.set_font('helvetica', 'B', 8)
                    self.set_xy(105, a)
                    img1 = pok['img']
                    validate_web_url(img1)
                    self.set_xy(90, a)
                    self.cell(53.5, 4.28, 'Type:', 0, 1, 'R')
                    self.set_font('helvetica', '', 8)
                    self.set_xy(134.5, a+3.5)
                    self.cell(146, 4.28, '{type}'.format(
                        type=",".join(pok["type"])), 0, 1)
                    self.set_font('helvetica', 'B', 8)
                    self.cell(136.5, 4.28, 'Height:', 0, 1, 'R')
                    self.set_font('helvetica', '', 8)
                    self.cell(136, 4.28, '{height}'.format(
                        height=pok["height"]), 0, 1, 'R')
                    self.set_font('helvetica', 'B', 8)
                    self.cell(137, 4.28, 'Weight:', 0, 1, 'R')
                    self.set_font('helvetica', '', 8)
                    self.set_xy(135, a+20)
                    self.cell(135, 4.28, '{weight}'.format(
                        weight=pok["weight"]), 0, 1)
                    self.set_font('helvetica', 'B', 8)
                    self.cell(145, 4.28, 'Weaknesses:', 0, 1, 'R')
                    self.set_font('helvetica', '', 8)
                    self.set_xy(135, a+29)
                    self.cell(145, 4.28, '{weaknesses}'.format(
                        weaknesses=",".join(pok['weaknesses'])), 0, 1)
                    #self.set_font('helvetica', 'B', 11)
                    self.add_font(
                        'DejaVuB', '', 'DejaVuSansCondensed-Bold.ttf', uni=True)
                    self.set_font('DejaVuB', '', 11)
                    self.set_text_color(255, 0, 0)
                    self.set_xy(103.5, a+32.5)
                    self.cell(105, 0, 'Name:', 0, 1)
                    #self.set_font('helvetica', '', 11)
                    self.set_xy(103.5, a+34)
                    self.add_font(
                        'DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
                    self.set_font('DejaVu', '', 11)
                    try:
                        self.cell(116, 5.28, '{name}'.format(
                            name=pok["name"]), 0, 0)
                    except:
                        continue

                    nbr_cellule += 1
                    i += 1

                    # cellule3 ====> sur la ligne
                    pok = data[i]
                    self.set_text_color(0, 0, 0)
                    self.set_xy(196, b)
                    self.cell(93, 40, border=1)
                    self.set_font('helvetica', 'B', 8)
                    self.set_xy(198, a)
                    img1 = pok['img']
                    validate_web_url(img1)
                    self.set_xy(183, a)
                    self.cell(53.5, 4.28, 'Type:', 0, 1, 'R')
                    self.set_font('helvetica', '', 8)
                    self.set_xy(227.5, a+3.5)
                    self.cell(239, 4.28, '{type}'.format(
                        type=",".join(pok["type"])), 0, 1)
                    self.set_font('helvetica', 'B', 8)
                    self.cell(229.5, 4.28, 'Height:', 0, 1, 'R')
                    self.set_font('helvetica', '', 8)
                    self.cell(229, 4.28, '{height}'.format(
                        height=pok["height"]), 0, 1, 'R')
                    self.set_font('helvetica', 'B', 8)
                    self.cell(230, 4.28, 'Weight:', 0, 1, 'R')
                    self.set_font('helvetica', '', 8)
                    self.set_xy(228, a+20)
                    self.cell(228, 4.28, '{weight}'.format(
                        weight=pok["weight"]), 0, 1)
                    self.set_font('helvetica', 'B', 8)
                    self.cell(238, 4.28, 'Weaknesses:', 0, 1, 'R')
                    self.set_font('helvetica', '', 8)
                    self.set_xy(228, a+29)
                    self.cell(238, 4.28, '{weaknesses}'.format(
                        weaknesses=",".join(pok['weaknesses'])), 0, 1)
                    #self.set_font('helvetica', 'B', 11)
                    self.add_font(
                        'DejaVuB', '', 'DejaVuSansCondensed-Bold.ttf', uni=True)
                    self.set_font('DejaVuB', '', 11)
                    self.set_text_color(255, 0, 0)
                    self.set_xy(196, a+32.5)
                    self.cell(198, 0, 'Name:', 0, 1)
                    #self.set_font('helvetica', '', 11)
                    self.set_xy(196, a+34)
                    self.add_font(
                        'DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
                    self.set_font('DejaVu', '', 11)
                    try:
                        self.cell(209, 5.28, '{name}'.format(
                            name=pok["name"]), 0, 0)
                    except:
                        continue

                    nbr_cellule += 1

                    self.ln(4)

                    if nbr_cellule <= 11:  # pour savoir si la page est pleine
                        i += 1
                        a += 40
                        b += 40
                    else:  # Dans le cas où c'est pleine
                        # pdf.add_page()
                        i += 1
                        self.set_text_color(0, 0, 0)
                        nbr_cellule = 0
                        a = 27
                        b = 25

            # génération du pdf
                name_pdf=sys.argv[4]
                pdf.output(name_pdf)

            # Bas de page
            def footer(self):
                # couleur noir pour le text
                self.set_text_color(0, 0, 0)
                self.set_y(-15)  # Position cursor at 1.5 cm from bottom:
                # Setting font: helvetica italic 8
                self.set_font("helvetica", "I", 8)
                # Printing page number:
                self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", 0, 0, "C")

        # print(data)

        # Appel de la classe PDF
        pdf = PDF('L', 'mm', 'A4')

        # pdf.add_font('DejaVuBold','',fp1,uni=True)
        # pdf.add_font('DejaVu','',fp,uni=True)
        # pdf.set_font("helvetica", '',size=4)

        # Appel de la fonction principale dans la classe PDF
        pdf.create_table(newlist)
        print("Fin de la création du pdf !!!")
        # suppression des fichiers temporraires
        # fp.close()
        # fp1.close()
        print("Nous commençons la création du logfile avec les données!!!")

    ############################################## Creation de fichier requirements.txt ########################################################

    # Commande pour la création du fichier requirements.txt dans le cmd (shell)
    # pip freeze > requirements.txt (pour voir tous les library utilisé ) après avoir installé le module freeze (pip install freeze) bien sûr

    ############################################## Creation de fichier logfile.txt ########################################################

        import logging

        # now we will Create and configure logger
        file_log=sys.argv[3]
        logging.basicConfig(filename=file_log,
                            format='%(message)s',
                            filemode='w')

        # on recupère le nombre de pokemons soit 151 au total
        def count_pokemon(pokemom):
            count = 0
            for nbr_pokemon in pokemom:
                count += 1
                # print(nbr_pokemon['name'])
            return count

        # print(count_pokemon(newlist))

        # vérification de l'url
        def check_web_url(url):
            try:
                urlopen(url)
                return True
            except URLError:
                return False
        # Affichage du traitement des pokemons par logging debug dans le fichier logfile.txt

        def treatments_pokemon(data):
            k = 0
            for pok in data:
                try:
                    logging.debug(
                        "Treating the pokemon: {name} ".format(name=pok["name"]))
                except:
                    continue

                if(check_web_url(data[k]["img"]) == False):
                    logging.debug("!!! The image file {} does not exist. It was replaced with the placeholder_img...!!!".format(
                        data[k]["img"]
                    ))
                k += 1
            logging.debug("All done.")
            k = 0

        # count_pokemon(newlist)

        # Let us Create an object
        logger = logging.getLogger()

        # Now we are going to Set the threshold of logger to DEBUG
        logger.setLevel(logging.DEBUG)

        # some messages to test
        logger.debug("We have {} pokemons. ".format(count_pokemon(newlist)))
        treatments_pokemon(newlist)

        print("Fin de la création du logfile !!!")
########################### Fin du code #########################################################################
