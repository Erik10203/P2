import datetime as d

transaktionsliste = []
budgets = {}

class Transaktion:
    nummerzähler = 0

    def __init__(self, betrag, unterkategorie, datum):
        if betrag == 0:
            print("Wenn du nichts buchen willst dann lass es")
            return
        Transaktion.nummerzähler += 1
        self.nummer = Transaktion.nummerzähler
        self.betrag = betrag
        self.kategorie = "Einnahme" if betrag > 0 else "Ausgabe"
        self.unterkategorie = unterkategorie
        self.datum = datum

    def getInfoTransaktion(self):
        return f"Nummer: {self.nummer}, Betrag: {self.betrag}, Kategorie: {self.kategorie}, Unterkategorie: {self.unterkategorie}, Datum: {self.datum.strftime('%d.%m.%Y')}"

    def getNummer(self):
        return self.nummer

    def getBetrag(self):
        return self.betrag

    def getKategorie(self):
        return self.kategorie

    def getUnterkategorie(self):
        return self.unterkategorie

    def getDatum(self):
        return self.datum

    @classmethod
    def neue_transaktion(cls):
        while True:
            try:
                betrag = float(input("Betrag (+/-): "))
                unterkategorie = input("Woher kommt das Geld?: ") if betrag > 0 else input("Für was hast du das Geld ausgegeben?: ")
                datum_str = input("Datum (TTMMJJJJ): ")
                datum_obj = d.datetime.strptime(datum_str, "%d%m%Y")

                neue_transaktion = cls(betrag, unterkategorie, datum_obj)
                transaktionsliste.append(neue_transaktion)
                print(f"Transaktion {neue_transaktion.nummer} hinzugefügt.")

                wasnu = input("Weitere Transaktion hinzufügen? (Ja/Nein) ")
                if wasnu.lower() != "ja":
                    break
            except Exception as e:
                print(f"Falsche Eingabe: {e}")
        
    @classmethod
    def vorhandene_unterkategorien(cls):
        return set(transaktion.unterkategorie for transaktion in transaktionsliste)

def anzeigen_transaktionen():
    for transaktion in transaktionsliste:
        print(f"Transaktionsnummer: {transaktion.getNummer()}, Datum: {transaktion.getDatum().strftime('%d.%m.%Y')}, Betrag: {transaktion.getBetrag()} €, Kategorie: {transaktion.getKategorie()}, Unterkategorie: {transaktion.getUnterkategorie()}")

def anzeigen_transaktionen_filter(gefilterte_transaktionen):
    for transaktion in gefilterte_transaktionen:
        print(f"Transaktionsnummer: {transaktion.getNummer()}, Datum: {transaktion.getDatum().strftime('%d.%m.%Y')}, Betrag: {transaktion.getBetrag()} €, Kategorie: {transaktion.getKategorie()}, Unterkategorie: {transaktion.getUnterkategorie()}")

def loeschen_transaktionen():
    anzeigen_transaktionen()
    loeschauswahl = int(input("Gib die Transaktionsnummer der Transaktion ein, die du löschen möchtest: "))
    for transaktion in transaktionsliste:
        if transaktion.getNummer() == loeschauswahl:
            transaktionsliste.remove(transaktion)
            print(f"Transaktion {loeschauswahl} gelöscht.")
            break
    else:
        print("Transaktion nicht gefunden.")

def budget_setzen():
    vorhandene_unterkategorien = Transaktion.vorhandene_unterkategorien()
    if not vorhandene_unterkategorien:
        print("Gibt keine")
        return
    kategorie = input("Welche Kategorie?: ")
    if kategorie not in vorhandene_unterkategorien:
        print(f"Die Kategorie '{kategorie}' existiert nicht.")
        return
    try:
        betrag = float(input(f"Welches Budget für {kategorie} setzen?: "))
        budgets[kategorie] = betrag
        print(f"Das Budget für {kategorie} wurde auf {betrag} gesetzt.")
    except ValueError:
        print("Ungültiger Betrag")

def check_budget():
    jahr = int(input("Gib das Jahr ein: ")) 
    monat = int(input("Gib den Monat ein: "))
    
    total_income = 0
    total_expenses = 0
    for tran in transaktionsliste:
        if tran.datum.year == jahr and tran.datum.month == monat:
            if tran.kategorie == "Einnahme":
                total_income += tran.betrag
            elif tran.kategorie == "Ausgabe":
                total_expenses += tran.betrag

    print(f"Total Einnahmen: {total_income}€, Total Ausgaben: {total_expenses}€ für {jahr}-{monat}")

    for unterkategorie, budget in budgets.items():
        spent = sum(tran.betrag for tran in transaktionsliste if tran.unterkategorie == unterkategorie and tran.datum.year == jahr and tran.datum.month == monat)
        print(f"{unterkategorie}: Budget: {budget}€, Ausgaben: {spent}€ für {jahr}-{monat}, {'Im Budget' if abs(spent)<= budget else 'Budget überschritten'}")

def menu_anzeigen():
    print("\n-------------------------------------------")
    print("Menü:")
    print("1. Neue Transaktion hinzufügen")
    print("2. Transaktion löschen")
    print("3. Transaktionen anzeigen")
    print("4. Budget planen")
    print("5. Budget checken")
    print("6. Konten anzeigen")
    print("7. Zeitraumfilter")
    print("8. Programm beenden")
    print("-------------------------------------------")

def Kontostand_Umsatz():
    anzeigen_transaktionen()
    Kontostand = 0
    Ausgaben = 0
    Einnahmen = 0

    for transaktion in transaktionsliste:
        if transaktion.getKategorie() == "Ausgabe":
            Ausgaben += transaktion.getBetrag()
        elif transaktion.getKategorie() == "Einnahme":
            Einnahmen += transaktion.getBetrag()
    Kontostand = Einnahmen + Ausgaben

    print("\nKontostand beträgt:", Kontostand)
    print("\nAusgaben betragen:", Ausgaben)
    print("\nEinnahmen betragen:", Einnahmen)

def ausgaben_fuer_unterkategorie(unterkategorie, gefilterte_transaktionen):
    summe = sum(transaktion.getBetrag() for transaktion in gefilterte_transaktionen if transaktion.getKategorie() == "Ausgabe" and transaktion.getUnterkategorie() == unterkategorie)
    return summe

def unterkategorie(gefilterte_transaktionen):
    unterkategorieliste = [transaktion.getUnterkategorie() for transaktion in gefilterte_transaktionen if transaktion.getKategorie() == "Ausgabe"]
    eindeutige_unterkategorienliste = list(set(unterkategorieliste))

    for unterkategorie in eindeutige_unterkategorienliste:
        betrag = ausgaben_fuer_unterkategorie(unterkategorie, gefilterte_transaktionen)
        print("\nAusgaben für", unterkategorie, "betragen:", betrag)

def Kontostand_Zeitraum(gefilterte_transaktionen):
    Kontostand = 0
    Ausgaben = 0
    Einnahmen = 0

    for transaktion in gefilterte_transaktionen:
        if transaktion.getKategorie() == "Ausgabe":
            Ausgaben += transaktion.getBetrag()
        elif transaktion.getKategorie() == "Einnahme":
            Einnahmen += transaktion.getBetrag()
    Kontostand = Einnahmen + Ausgaben

    print("\nKontostand beträgt:", Kontostand)
    print("\nAusgaben betragen:", Ausgaben)
    print("\nEinnahmen betragen:", Einnahmen)

def Zeitraumfilter():
    startdatum_str = input("Startdatum des Zeitraums (TTMMJJJJ): ")
    enddatum_str = input("Enddatum des Zeitraums (TTMMJJJJ): ")
    startdatum = d.datetime.strptime(startdatum_str, "%d%m%Y")
    enddatum = d.datetime.strptime(enddatum_str, "%d%m%Y")

    gefilterte_transaktionen = [transaktion for transaktion in transaktionsliste if startdatum <= transaktion.datum <= enddatum]
    
    anzeigen_transaktionen_filter(gefilterte_transaktionen)
    unterkategorie(gefilterte_transaktionen)
    Kontostand_Zeitraum(gefilterte_transaktionen)

def programm_starten():
    while True:
        menu_anzeigen()
        auswahl = input("Wähl mal eine Option: ")

        if auswahl == "1":
            Transaktion.neue_transaktion()
        elif auswahl == "2":
            loeschen_transaktionen()
        elif auswahl == "3":
            anzeigen_transaktionen()
        elif auswahl == "4":
            budget_setzen()
        elif auswahl == "5":
            check_budget()
        elif auswahl == "6":
            Kontostand_Umsatz()
            unterkategorie(transaktionsliste)
        elif auswahl == "7":
            Zeitraumfilter()
        elif auswahl == "8":
            print("Tschüss. Alles Gute.")
            break
        else:
            print("Eingabe muss zwischen 1 und 7 sein.")

budget = 0  # beim Start

# Beispieltransaktionen
transaktion01 = Transaktion(-45, "Lebensmittel", d.datetime.strptime("12022024", "%d%m%Y"))
transaktion02 = Transaktion(-23, "Lebensmittel", d.datetime.strptime("15022024", "%d%m%Y"))
transaktion03 = Transaktion(-28, "Handy", d.datetime.strptime("16022024", "%d%m%Y"))
transaktion04 = Transaktion(-15, "Puff", d.datetime.strptime("20022024", "%d%m%Y"))
transaktion05 = Transaktion(2000, "Puff", d.datetime.strptime("20022024", "%d%m%Y"))

transaktionsliste.append(transaktion01)
transaktionsliste.append(transaktion02)
transaktionsliste.append(transaktion03)
transaktionsliste.append(transaktion04)
transaktionsliste.append(transaktion05)

programm_starten()

