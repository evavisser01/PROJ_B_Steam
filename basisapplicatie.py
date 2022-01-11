import json
import tkinter
import matplotlib
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

root = tkinter.Tk()

# --------------------------------------------Berekeningen----------------------------------------------------------


def div(n):
    """
    Bepaal alle delers van een geheel getal.
    Het positieve gehele getal a is een deler van n, als er een positief geheel getal b is, zodat a × b = n.
    Args:
        n (int): Een geheel getal.
    Returns:
        list: Een gesorteerde lijst met alle delers van `n`.
    """
    divisors = []                       # De lijst divisors (waar we later delers in stoppen) wordt aangemaakt
    for getal in range(1, n+1):         # Voor elk getal tussen 1 en het ingevoerde getal
        if n % getal == 0:              # Er wordt gekeken of de rest van de deelsom 0 is.
            divisors.append(getal)      # Het deel getal wordt toegevoegd aan de divisors lijst.
    return sorted(divisors)             # De gesorteerde lijst divors wordt gereturned


def gcd(a, b):
    delers_a = sorted(div(a), reverse=True)
    delers_b = div(b)
    for deler in delers_a:
        if deler in delers_b:
            return deler


# --------------------------------------------Tkinter---------------------------------------------------------------

# logo_steam = Image.open('Steam_Logo.png')
# logo_steamtk = ImageTk.PhotoImage(logo_steam)
# logo_steam.show()


def sluit_scherm():
    regels = root.grid_slaves()
    for regel in regels:
        regel.destroy()


def steam_label():
    steam_label = tkinter.Label(root, text='STEAM', bg='#171a21', fg='white', font=('Trebuchet MS Vet', 40))
    steam_label.grid(row=0, columnspan=3, sticky='NSEW')


def weergeef_gui():
    canvas = tkinter.Canvas(root, width=800, height=400, bg='#1b2838')
    canvas.grid(columnspan=3, rowspan=4)
    steam_label()
    eerste_spel = tkinter.Button(root, text='Eerste spel van bronbestand', bg='#66c0f4', fg='white', command=\
        weergeef_spel_naam)
    eerste_spel.grid(row=1, column=0, sticky='NSEW')
    aantal_spellen_genre = tkinter.Button(root, text='Meest voorkomende genre', bg='#66c0f4', fg='white', command=\
        kwalitatieve_variabele)
    aantal_spellen_genre.grid(row=1, column=1, sticky='NSEW')
    ratings = tkinter.Button(root, text='ratings', bg='#66c0f4', fg='white', command=\
        kwantitatieve_variabele)
    ratings.grid(row=1, column=2, sticky='NSEW')
    zoeken_knop = tkinter.Button(root, text='zoeken', bg='#66c0f4', fg='white', command=\
        zoeken_data)
    zoeken_knop.grid(row=2, column=0, sticky='NSEW')
    return


def label(text, rij, columnspan):
    labeltje = tkinter.Label(root, text=text)
    labeltje.grid(row=rij, columnspan=columnspan, sticky='NSEW')


def terug_naar_dashboard(rij):
    naar_dashboard = tkinter.Button(root, text='terug naar dashboard', bg='#66c0f4', fg='white', command= \
        lambda: [sluit_scherm(), weergeef_gui()])
    naar_dashboard.grid(row=rij, columnspan=3, sticky='NSEW')


# --------------------------------------------Functies---------------------------------------------------------------


# --------Onderdeel 1------------ Basisapplicatie met data
def weergeef_spel_naam():
    """
    Een functie die de naam van het eerste spel uit het bronbestand weergeeft in het dashboard
    """
    data = inladen()
    for dictionary in data:
        if data.index(dictionary) == 0:
            label(dictionary['name'], 1, 3)
            terug_naar_dashboard(2)
            return dictionary['name']


def data_sorteren(dictionaries, sort_by):
    """
    Een functie waarmee de data uit het bronbestand gesorteerd kan worden (standaard sorteerfunctie van Python)
    """
    dictionaries_gesorteerd = sorted(dictionaries, key=lambda dictionary: dictionary[sort_by])
    return dictionaries_gesorteerd


def inladen():
    """
    Een functie waarmee jullie het .json bronbestand (zie GitHub (Koppelingen naar een externe site.)) inladen
    in een passende datastructuur; houd er rekening mee dat je in de volgende opdracht de datapunten moet kunnen
    sorteren en er beschrijvende statistiek op moet gaan toepassen, dus kies een handig datatype
    waarbij dit mogelijk is;
    """
    steam_file = open("steam.json")
    regels = json.load(steam_file)
    return regels


# --------Onderdeel 3------------ Statistiekfuncties - NOG NIET DOOR TEAM GEZIEN
def kwalitatieve_variabele():
    """
    Een functie die de het meest voorkomende genre weergeeft.
    """
    data = inladen()
    freqs = {}
    for dictionary in data:
        genres = dictionary['genres']
        if genres in freqs:
            freqs[genres] += 1
        else:
            freqs[genres] = 1

    modi = []
    hoogstefreq = 0
    for getal, aantal in freqs.items():
        if aantal > hoogstefreq:
            hoogstefreq = aantal
            modi.clear()
            modi.append(getal)
        elif aantal == hoogstefreq:
            modi.append(getal)
    label(modi, 1, 3)
    terug_naar_dashboard(2)
    return modi


def kwantitatieve_variabele():
    """
    Een functie die de verhouding van positive_ratings / negative_ratings weergeeft.
    """
    def verstuur_spelnaam():
        spelnaam = invoer.get()
        data = data_sorteren(inladen(), 'name')
        for dictionary in data:
            if dictionary['name'] == spelnaam:
                positieve_rating = dictionary['positive_ratings']
                negatieve_rating = dictionary['negative_ratings']
                totale_rating = dictionary['positive_ratings'] + dictionary['negative_ratings']
                #grootste_deler = gcd(positieve_rating, totale_rating)
                #positieve_rating_vereenvoudigd = int(positieve_rating / grootste_deler)
                #totale_rating_vereenvoudigd = int(totale_rating / grootste_deler)
                #if positieve_rating_vereenvoudigd > 1:
                label(f'Van de {totale_rating} gebruikers vinden {positieve_rating} het spel leuk.', 1, 3)
                return positieve_rating, negatieve_rating
        else:
            label(f'"{spelnaam}" niet gevonden.', 1, 3)

    invoer = tkinter.Entry(root)
    invoer.grid(row=1, column=0, columnspan=2, sticky='NSEW')
    verstuur = tkinter.Button(root, text='Verstuur', bg='#1C2E4A', fg='white', command=verstuur_spelnaam)
    verstuur.grid(row=1, column=2, sticky='NSEW')
    terug_naar_dashboard(2)
    return


# --------Onderdeel 10------------ Steam API - NOG NIET GEMAAKT / API AANVRAGEN
def live_data():
    """
    Breid het dashboard uit met functionaliteit die de data live uit de Steam API haalt in plaats van uit het
    bronbestand (bij voorkeur zo gestructureerd dat er géén code tussen functies is gekopieerd).
    """


# --------Onderdeel 11------------ Sorteren - Langzaam werkt enkel op required_age en appid


def sorteren(data, sort_by):
    """
     Breid het dashboard uit met functionaliteit waarmee de data gesorteerd wordt teruggegeven. Gebruik hiervoor één van
     de sorteeralgoritmen die tijdens Oriëntatie op AI is behandeld.

         Zorg dat componenten in het dashboard (oftewel de GUI) gebruik maken van de sorteerfunctie, bijvoorbeeld
         een lijst met twee kolommen waarop je kunt sorteren. Jullie mogen je eigen creativiteit gebruiken
         om nuttige functionaliteit toe te voegen.
     """
    # sorteren op prijs en jaartal????
    dictionaries = []
    for dictje in data:
        dictionaries.append(dictje)
    verwisselingen = True
    while verwisselingen:
        verwisselingen = False
        for index_dict in range(len(dictionaries)-1):
            dictionary = dictionaries[index_dict][sort_by]
            buurdict_index = index_dict + 1
            buurdict = dictionaries[buurdict_index][sort_by]
            if dictionary > buurdict:
                dictionaries[buurdict_index], dictionaries[index_dict] = dictionaries[index_dict], dictionaries[buurdict_index]
                verwisselingen = True
    return dictionaries


# print(sorteren(inladen(), 'appid'))

# --------Onderdeel 12------------ Zoeken - KLEINE PROBLEMEN OPLOSSEN
def zoeken(data, zoek_categorie, zoekopdracht):
    """
    Breid het dashboard uit met functionaliteit die in de data zoekt naar bepaald waardes. Gebruik hiervoor het binaire
    zoekalgoritme dat tijdens Oriëntatie op AI is behandeld. De functionaliteiten van onderdeel 3. hierboven bevatte ook
    al zoekfuncties, maar dan met behulp van standaardfuncties uit Python. Deze vervang je nu door jouw eigen code.
    Voeg componenten in het dashboard toe om de zoekfunctie te kunnen gebruiken.
    """
    # Code voor binair zoeken.
    gevonden_data = []
    gesorteerde_data = merge_sort(data, zoek_categorie)
    laag = 0
    hoog = len(gesorteerde_data) - 1

    while laag <= hoog:
        gem = int((laag + hoog) / 2)
        if gesorteerde_data[gem][zoek_categorie] == zoekopdracht:
            gevonden_data.append(gesorteerde_data[gem])
            gesorteerde_data.remove(gesorteerde_data[gem])
            hoog -= 1
        elif zoekopdracht > gesorteerde_data[gem][zoek_categorie]:
            laag = gem + 1
        else:
            hoog = gem - 1

    sluit_scherm()
    canvas = tkinter.Canvas(root, width=800, height=400, bg='#1b2838')
    canvas.grid(columnspan=3, rowspan=3)
    steam_label()

    if not gevonden_data:
        label('niks gevonden', 1, 3)
        terug_naar_dashboard(2)
        return False
    else:
        gevonden = Listbox(root, width=100)
        gevonden.grid(row=1, column=0, columnspan=2, sticky='NSEW')

        for g_data in gevonden_data:
            gevonden.insert(END, f"{g_data['name']}")

        # Scrollbalk y-as
        scrollbary = ttk.Scrollbar(root, orient='vertical')
        scrollbary.grid(row=1, sticky='nse', column=1)
        scrollbary.config(command=gevonden.yview)

        # Scrollbalk x-as
        scrollbarx = ttk.Scrollbar(root, orient='horizontal')
        scrollbarx.grid(row=1, sticky='sew', columnspan=2)
        scrollbarx.config(command=gevonden.xview)

        # Configureren scrollbalk in gevonden games box.
        gevonden.config(yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        terug_naar_dashboard(2)

        def select_item():
            geselecteerd = gevonden.get(ANCHOR)
            for gev_data in gevonden_data:
                gevonden.delete(0)

                if gev_data['name'] == geselecteerd:
                    for key, value in gev_data.items():
                        gevonden.insert(END, f"{key}: {value}")
                    verstuur_knop.configure(text='terug', command=lambda: [zoeken_data()])

        verstuur_knop = tkinter.Button(root, text='Info', bg='#66c0f4', fg='white', command=select_item)
        verstuur_knop.grid(row=1, sticky='nsew', column=2)
        return gevonden_data


def zoekwoord(categorie, formaat):
    sluit_scherm()
    canvas = tkinter.Canvas(root, width=800, height=400, bg='#1b2838')
    canvas.grid(columnspan=3, rowspan=4)
    steam_label = tkinter.Label(root, text='STEAM', bg='#171a21', fg='white', font=('Trebuchet MS Vet', 40))
    steam_label.grid(row=0, columnspan=3, sticky='NSEW')
    invoer = tkinter.Entry(root)
    invoer.grid(row=1, column=0, columnspan=2, sticky='NSEW')
    knop_1 = tkinter.Button(root, text='Zoeken', bg='#1C2E4A', fg='white', command=lambda: [zoeken(inladen(), categorie, formaat(invoer.get()))])
    knop_1.grid(row=1, column=2, sticky='NSEW')
    terug_naar_dashboard(2)


def zoeken_data():
    sluit_scherm()
    canvas = tkinter.Canvas(root, width=800, height=400, bg='#1b2838')
    canvas.grid(columnspan=3, rowspan=4)
    steam_label()
    
    def zoek_categorie():
        def zoek_categorie_2():
            def zoek_categorie_3():
                def zoek_categorie_4():
                    knop_1.configure(text='<', command=zoek_categorie_3)
                    knop_2.configure(text='negative_ratings', command=lambda: [zoekwoord('negative_ratings', int)])
                    knop_3.configure(text='average_playtime', command=lambda: [zoekwoord('average_playtime', int)])
                    knop_4.configure(text='median_playtime', command=lambda: [zoekwoord('median_playtime', int)])
                    knop_5.configure(text='owners', command=lambda: [zoekwoord('owners', str)])
                    volgende_knop.configure(text='price', command=lambda: [zoekwoord('price', int)])
                knop_1.configure(text='<', command=zoek_categorie_2)
                knop_2.configure(text='genres', command=lambda: [zoekwoord('genres', str)])
                knop_3.configure(text='steamspy_tags', command=lambda: [zoekwoord('steamspy_tags', str)])
                knop_4.configure(text='achievements', command=lambda: [zoekwoord('achievements', int)])
                knop_5.configure(text='positive_ratings', command=lambda: [zoekwoord('positive_ratings', int)])
                volgende_knop.configure(text='>', command=zoek_categorie_4)
            knop_1.configure(text='<', command=zoek_categorie)
            knop_2.configure(text='publisher', command=lambda: [zoekwoord('publisher', str)])
            knop_3.configure(text='platforms', command=lambda: [zoekwoord('platforms', str)])
            knop_4.configure(text='required_age', command=lambda: [zoekwoord('required_age', int)])
            knop_5.configure(text='categories', command=lambda: [zoekwoord('categories', str)])
            volgende_knop.configure(text='>', command=zoek_categorie_3)

        knop_1 = tkinter.Button(root, text='appid', bg='#1C2E4A', fg='white', command=lambda: [zoekwoord('appid', int)])
        knop_1.grid(row=1, column=0, sticky='NSEW')
        knop_2 = tkinter.Button(root, text='name', bg='#1C2E4A', fg='white', command=lambda:[zoekwoord('name', str)])
        knop_2.grid(row=1, column=1, sticky='NSEW')
        knop_3 = tkinter.Button(root, text='release_date', bg='#1C2E4A', fg='white', command=lambda: [zoekwoord('release_date', str)])
        knop_3.grid(row=1, column=2, sticky='NSEW')
        knop_4 = tkinter.Button(root, text='english', bg='#1C2E4A', fg='white', command=lambda: [zoekwoord('english', int)])
        knop_4.grid(row=2, column=0, sticky='NSEW')
        knop_5 = tkinter.Button(root, text='developer', bg='#1C2E4A', fg='white', command=lambda: [zoekwoord('developer', str)])
        knop_5.grid(row=2, column=1, sticky='NSEW')
        volgende_knop = tkinter.Button(root, text='>', bg='#1C2E4A', fg='white', command=zoek_categorie_2)
        volgende_knop.grid(row=2, column=2, sticky='NSEW')
        terug_naar_dashboard(3)
    zoek_categorie()


# --------Onderdeel 13------------ Sorteren (geavanceerd) - OP DASHBOAD ZETTEN (merge sort werkt)
def quick_sort(data, sort_by):
    """
    Implementeer een geavanceerde variant van een sorteeralgoritme, zoals merge sort of quick sort (deze zijn niet
    uitgebreid behandeld tijdens Oriëntatie op AI). Gebruik hiervoor een aparte functie.
    """
    lengte_data = len(data)
    if lengte_data <= 1:
        return data
    else:
        vergelijk_getal = data.pop()[sort_by]
        vergelijk_dict = data.pop()
        kleiner_vergelijking = []
        groter_vergelijking = []
        for dictionary in data:
            if dictionary[sort_by] < vergelijk_getal:
                kleiner_vergelijking.append(dictionary)
            elif dictionary[sort_by] >= vergelijk_getal:
                groter_vergelijking.append(dictionary)
    return quick_sort(kleiner_vergelijking, sort_by) + [vergelijk_dict] + quick_sort(groter_vergelijking, sort_by)


def merge_sort(data, sort_by):
    if len(data) > 1:
        # Als er meer dan een item in data zit dan splits je de data in 2e.
        eerste_helft_data = data[:len(data) // 2]
        tweede_helft_data = data[len(data) // 2:]

        # Het sorteren van de eerste en tweede helft van de data
        merge_sort(eerste_helft_data, sort_by)
        merge_sort(tweede_helft_data, sort_by)

        # Sorteer indexen
        index_eerste_helft = 0
        index_tweede_helft = 0
        index_gesorteerde_data = 0

        # Het vergelijken van de eerste lijst met de tweede lijst.
        while index_eerste_helft < len(eerste_helft_data) and index_tweede_helft < len(tweede_helft_data):
            if eerste_helft_data[index_eerste_helft][sort_by] < tweede_helft_data[index_tweede_helft][sort_by]:
                data[index_gesorteerde_data] = eerste_helft_data[index_eerste_helft]
                index_eerste_helft += 1

            else:
                data[index_gesorteerde_data] = tweede_helft_data[index_tweede_helft]
                index_tweede_helft += 1

            index_gesorteerde_data += 1

        # Als er een lijst helemaal gesorteerd is, dan moet het overige van de andere lijst nog in de lijst.
        while index_eerste_helft < len(eerste_helft_data):
            data[index_gesorteerde_data] = eerste_helft_data[index_eerste_helft]
            index_eerste_helft += 1
            index_gesorteerde_data += 1

        while index_tweede_helft < len(tweede_helft_data):
            data[index_gesorteerde_data] = tweede_helft_data[index_tweede_helft]
            index_tweede_helft += 1
            index_gesorteerde_data += 1

    return data


# --------Onderdeel 14------------ Zoeken (geavanceerd) - NOG NIET GEMAAKT
def zoeken_geavanceerd():
    """
    Pas het principe van binair zoeken toe op een datastructuur die complexer is dan een lijst. Denk hierbij aan het
    bijhouden van een binary search tree, die wordt hergebruikt bij het herhaaldelijk inlezen van nieuwe data.
    """
# --------Onderdeel 15------------ Grafieken & diagrammen - NOG NIET GEMAAKT
    """
    Voeg grafieken of diagrammen toe aan je dashboard die interessante kenmerken van de brondata tonen. Je kan hiervoor
    gebruik maken van bestaande libraries van Python, zoals Matplotlib (https://matplotlib.org/ (Koppelingen naar een
    externe site.)).
    -Top 5 (goedbeoordeelde spellen, meest voorkomende genres)
    -Statistiek uitgebrachten spellen.
    
    
    """
# --------Onderdeel 16------------ Normaalverdeling - NOG NIET GEMAAKT
    """
    Pas de statistieken en kansverdelingen van de normaalverdeling toe. Onderzoek daarvoor eerst welk van de variabelen
    in de brondata normaal verdeeld zijn. Maak vervolgens gebruik van de eigenschappen van de normaalverdeling om
    uitspraken te doen over specifieke waarden in deze variabele, bijvoorbeeld “Dit spel behoort tot de 10% populairste
    spellen”. Beeld dit af in het dashboard.
    """


# -----------------------TEST-------------------------

# Onderdeel 1 ****************
    # print(weergeef_spel_naam())
    # print(data_sorteren(inladen(), 'name'))
    # print(inladen())

# Onderdeel 3****************
    # print(kwalitatieve_variabele())
    # print(kwantitatieve_variabele())


# print(sorteren(inladen(), 'appid'))
# print(zoeken(inladen(), 'name', 'Rune Lord'))
# print(quick_sort(inladen(), 'price'))
# print(merge_sort(inladen(), 'name'))
weergeef_gui()


root.mainloop()
