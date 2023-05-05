from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from tools.Tools import Tools
from time import sleep
import os
import sys
import getopt
import json


# Lancement d'un webdriver
def init_webdriver(debug, firefox_location)-> webdriver:
    options = webdriver.FirefoxOptions()
    if not debug:
        options.headless = True

    # Les options du navigateur, ici Firefox
    # l'emplacement du navigateur
    options.binary_location = firefox_location

    # Lancement du browser
    # Options : -> emplacement exécutable geckodriver
    #           -> emplacement logs geckodriver
    #           -> options du navigateur
    # Créer un objet Service pour le pilote GeckoDriver
    gecko_path = 'selenium/geckodriver.exe'
    gecko_service = Service(executable_path=gecko_path, log_path='selenium/geckodriver.log')
    browser = webdriver.Firefox(service=gecko_service, options=options)

    # browser.maximize_window()

    return browser


def usage():
    print("Pour que l'outil se lance correctement, il faut définir au premier lancement :")
    print("     - Le nom d'utilisateur (exemple : jean.dupont@gmail.com)")
    print("     - Le mot de passe associe (exemple : tonmeilleurmotdepasse)")
    print("     - La location de l'exe de firefox (exemple : C:/Program Files/Mozilla Firefox/firefox)")
    print("Ces informations sont stockees dans le fichier conf.json")
    print("Vous n'aurez pas à les remplir à chaque utilisation\n")

    print("-h --help Affiche l'aide")
    print("-u --username Met à jour le nom d'utilisateur")
    print("-p --password Met à jour le mot de passe de l'utilisateur")
    print("-b --browser Met à jour la location de l'exe de firefox")
    print("-d --debug Affiche la fenetre du navigateur")

    sys.exit()


def main():
    # Vérification des arguments passés dans la ligne de commande
    try:
        opts, args = getopt.getopt(sys.argv[1:], "u:p:b:hd", ["user=", "password=", "browser=", "debug", "help"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)
        usage()
        sys.exit()

    # Argument optionnel
    debug = True

    # Argument obligatoire
    usr = ''
    pwd = ''
    browser_location = ''

    for o, a in opts:
        if o in ("-d", "--debug"):
            debug = True

        elif o in ("-h", "--help"):
            usage()

        elif o in ("-u", "--user"):
            usr = a

        elif o in ("-p", "--password"):
            pwd = a

        elif o in ("-b", "--browser"):
            browser_location = a

        else:
            assert False, "unhandled option"

    with open("conf.json", "r") as jsonFile:
        conf = json.load(jsonFile)

    if usr != '':
        conf["username"] = usr

    if pwd != '':
        conf["password"] = pwd

    if browser_location != '':
        conf["browser"]["location"] = browser_location

    with open("conf.json", "w") as jsonFile:
        json.dump(conf, jsonFile)

    if conf["browser"]["location"] == '' or conf["password"] == '' or conf["username"] == '':
        print("Il manque un element a configurer : nom d'utilisateur, mot de passe ou la location du navigateur")
        sys.exit()

    browser = init_webdriver(debug, conf["browser"]["location"])

    tools = Tools(browser)

    tools.connection(conf["username"], conf["password"])

    tools.go_to_assignement()
    sleep(2)
    courses = tools.get_all_cours()
    #courses = courses[15:]
    print(f'[+] {len(courses)} cours trouvés !')
    for course in courses:
        print('---------------------------------')
        print(course)
        if not tools.check_course(course):
            tools.get_cours(course)
            test_url = tools.check_for_test()
            if test_url != '':
                browser.get(test_url)
                tools.passing_test()
        else:
            print('100%')
    # Fin du programme
    browser.quit()


if __name__ == "__main__":
    main()














