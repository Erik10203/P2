import datetime as d

transaktionsliste = []

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
                else:
                    continue
            except Exception as e:
                print(f"Falsche Eingabe: {e}")
                continue
    
        
    def anzeigen_transaktionen():
        [print(f"Transaktionsnummer: {transaktion.getNummer()}, Datum: {transaktion.getDatum().strftime('%d.%m.%Y')}, Betrag: {transaktion.getBetrag()} €, Kategorie: {transaktion.getKategorie()}, Unterkategorie: {transaktion.getUnterkategorie()}") for transaktion in transaktionsliste]
        
    def loeschen_transaktionen():
        Transaktion.anzeigen_transaktionen()
        loeschauswahl = int(input("Gib die Transaktionsnummer der Transaktion ein, die du löschen möchtest: "))
        for transaktion in transaktionsliste:
            if transaktion.getNummer() == loeschauswahl:
                transaktionsliste.remove(transaktion)
                print(f"Transaktion {loeschauswahl} wurde gelöscht.")
                break
        else:
            print("Transaktion nicht gefunden.")
        
    
    def getInfoTransaktion(self):
        return str(self.nummer) + str(self.betrag) + self.kategorie + self.unterkategorie + str(self.datum)
    
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

# Neue Transaktionen hinzufügen
#Transaktion.neue_transaktion()
while True:
    print ("1. Anzeigen")
    print ("2. Hinzu")
    print ("3. Löschen")
    print ("4. Stopp")
    
    auswahl = int(input("Was willst? "))
    if auswahl == 1:
        Transaktion.anzeigen_transaktionen()
        
    elif auswahl == 2:
        Transaktion.neue_transaktion()
        
    elif auswahl == 3: 
        Transaktion.loeschen_transaktionen()
        
    elif auswahl == 4:
        False 
# Kontostand, Ausgaben, Einnahmen etc. berechnen
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

# Ausgaben pro Unterkategorie berechnen
unterkategorieliste = [transaktion.getUnterkategorie() for transaktion in transaktionsliste if transaktion.getKategorie() == "Ausgabe"]
eindeutige_unterkategorienliste = list(set(unterkategorieliste))

def ausgaben_fuer_unterkategorie(unterkategorie):
    summe = sum(transaktion.getBetrag() for transaktion in transaktionsliste if transaktion.getKategorie() == "Ausgabe" and transaktion.getUnterkategorie() == unterkategorie)
    return summe

for unterkategorie in eindeutige_unterkategorienliste:
    betrag = ausgaben_fuer_unterkategorie(unterkategorie)
    print("\nAusgaben für", unterkategorie, "betragen:", betrag)
