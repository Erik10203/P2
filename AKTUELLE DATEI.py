import datetime as d
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

global transaktionsliste
transaktionsliste = []
budgets = {}
budget = 0

global unterkategorie_liste
unterkategorie_liste = ("job", "verkehrsmittel", "essen", "freizeit", "urlaub", "sonstige")

#sorgt dafür, dass die alten Fenster nicht mehr offen sind wenn man einen neuen Menüpunkt anklickt. Popups bleiben weiterhin geöffnet!
def fenster_schließen():
    for widget in neue_transaktion_frame.winfo_children():
        widget.destroy
    
    for widget in transaktion_löschen_frame.winfo_children():
        widget.destroy

    for widget in budget_setzen_frame.winfo_children():
        widget.destroy
        
    for widget in budget_check_frame.winfo_children():
        widget.destroy
        
    for widget in zeitraumfilter_frame.winfo_children():
        widget.destroy
        
    for widget in grafische_auswertungen_frame.winfo_children():
        widget.destroy
        
    neue_transaktion_frame.pack_forget()
    transaktion_löschen_frame.pack_forget()
    budget_setzen_frame.pack_forget()
    budget_check_frame.pack_forget()
    zeitraumfilter_frame.pack_forget()
    grafische_auswertungen_frame.pack_forget()    

class Transaktion:
    nummerzähler = 0

    def __init__(self, betrag, unterkategorie, datum):
        if betrag == 0:
            tk.messagebox.showinfo("Fehler", "Wenn du nichts buchen willst, dann lass es")
            return
        Transaktion.nummerzähler += 1
        self.nummer = Transaktion.nummerzähler
        self.betrag = betrag
        self.kategorie = "Einnahme" if betrag > 0 else "Ausgabe"
        self.unterkategorie = unterkategorie
        self.datum = datum

    def getInfoTransaktion(self):
        return f"Nummer: {self.nummer}, Betrag: {self.betrag}, Kategorie: {self.kategorie}, Unterkategorie: {self.unterkategorie}, Datum: {self.datum.strftime('%d.%m.%Y')}"
   
    def getTransaktionspeicher(self):
        return f"{self.nummer}, {self.betrag}, {self.kategorie}, {self.unterkategorie}, {self.datum.strftime('%d.%m.%Y')}"
    
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
    def transaktion_speichern(cls, transaktion):
        with open("t.txt", "a") as file:
            file.write(transaktion.getTransaktionspeicher() + "\n")

    @classmethod
    def transaktion_lesen2(cls):
        tliste2 = []
        try:
            with open("t.txt", "r") as file:
                for line in file:
                    parts = line.strip().split(', ')
                    if len(parts) == 5:
                        nummer, betrag, kategorie, unterkategorie, datum_str = parts
                        datum_obj = d.datetime.strptime(datum_str, "%d.%m.%Y")
                        transaktion = cls(float(betrag), unterkategorie, datum_obj)
                        tliste2.append(transaktion)
                    global transaktionsliste
                    transaktionsliste = tliste2
            return tliste2
        except FileNotFoundError:
            tk.messagebox.showerror("Fehler", "Datei t.txt nicht gefunden.")
            return []

    @classmethod
    def neue_transaktion(cls, betrag, unterkategorie, datum):
        try:
            neue_transaktion = cls(betrag, unterkategorie, datum)
            cls.transaktion_speichern(neue_transaktion)
            transaktionsliste.append(neue_transaktion)
            
            n = neue_transaktion.nummer
            
            transaktion_ausgabe = tk.Label(neue_transaktion_frame, text= f"Erfolg, Transaktion {n} wurde hinzugefügt", font=('Arial', 12))
            transaktion_ausgabe.grid(row=5, column=2)
            
            cls.check_fuer_budget_ueberschreitung(neue_transaktion)
        except Exception as e:
            tk.messagebox.showerror("Fehler", f"Falsche Eingabe: {e}")

    @classmethod
    def check_fuer_budget_ueberschreitung(cls, transaktion):
        if transaktion.kategorie == "Ausgabe" and transaktion.unterkategorie in budgets:
            monat = transaktion.datum.month
            jahr = transaktion.datum.year
            ausgaben = sum(t.betrag for t in transaktionsliste if t.kategorie == "Ausgabe" and t.unterkategorie == transaktion.unterkategorie and t.datum.month == monat and t.datum.year == jahr)
            if abs(ausgaben) > budgets[transaktion.unterkategorie]:  # berücksichtige negative Beträge
                tk.messagebox.showwarning("Budget überschritten", f"Das Budget für '{transaktion.unterkategorie}' wurde überschritten. Geplantes Budget: {budgets[transaktion.unterkategorie]}, Aktuell ausgegeben: {ausgaben}")

    @classmethod
    def vorhandene_unterkategorien(cls):
        return set(transaktion.unterkategorie for transaktion in transaktionsliste)
    
#Zeigt alle Transaktionen in einem txt Popup
def anzeigen_transaktionen():
    transactions_window = tk.Toplevel()
    transactions_window.title("Transaktionen anzeigen")

    tree = ttk.Treeview(transactions_window, columns=("Nummer", "Betrag", "Kategorie", "Unterkategorie", "Datum"), show="headings")
    tree.heading("Nummer", text="Nummer")
    tree.heading("Betrag", text="Betrag")
    tree.heading("Kategorie", text="Kategorie")
    tree.heading("Unterkategorie", text="Unterkategorie")
    tree.heading("Datum", text="Datum")

    for transaktion in transaktionsliste:
        tree.insert("", tk.END, values=(transaktion.getNummer(), transaktion.getBetrag(), transaktion.getKategorie(), transaktion.getUnterkategorie(), transaktion.getDatum().strftime('%d.%m.%Y')))

    tree.pack(fill=tk.BOTH, expand=True)

#Zeigt alle Transaktionen (im ausgewählten Zeitraumfilter) in einem txt Popup
def anzeigen_transaktionen_filter(gefilterte_transaktionen):
    anzeige_fenster = tk.Toplevel(root)
    anzeige_fenster.title("Gefilterte Transaktionen anzeigen")
    text_area = tk.Text(anzeige_fenster, wrap="word")
    text_area.pack(expand=True, fill="both")
    for transaktion in gefilterte_transaktionen:
        text_area.insert(tk.END, f"Transaktionsnummer: {transaktion.nummer}, Datum: {transaktion.datum.strftime('%d.%m.%Y')}, Betrag: {transaktion.betrag} €, Kategorie: {transaktion.kategorie}, Unterkategorie: {transaktion.unterkategorie}\n")

def loeschen_transaktionen():
    
    #alte fenster schließen
    fenster_schließen()
    
    #öffnet neues fenster
    transaktion_löschen_frame.pack(fill="both", expand=1)
    
    #Text und Eingabefelder
    welche_transaktion_löschen_text = tk.Label(transaktion_löschen_frame, text="welche Transaktion soll gelöscht werden?", font=('Arial', 12))
    welche_transaktion_löschen_text.grid(row=1, column=0)
    
    eingabe_loeschen_transaktion = tk.Entry(transaktion_löschen_frame, width=30, font=("Arial", 12))
    eingabe_loeschen_transaktion.grid(row=2, column=0)
    
    #Logig der Funktion (wird erst ausgeführt wenn der Kopf gedrückt wurde)
    def ausfuehren ():
        
        loeschauswahl = str(eingabe_loeschen_transaktion.get())
        
        
        if loeschauswahl is None:
            return
    
        transaktion_gefunden = False
        for transaktion in transaktionsliste:
            if str(transaktion.nummer) == loeschauswahl:
                transaktionsliste.remove(transaktion)
                transaktion_gefunden = True
                tk.messagebox.showinfo("Erfolg", f"Transaktion {loeschauswahl} gelöscht.")
                break
    
        if not transaktion_gefunden:
            tk.messagebox.showerror("Fehler", "Transaktion nicht gefunden.")
        else:
            with open("t.txt", "w") as file:
                for transaktion in transaktionsliste:
                    file.write(transaktion.getTransaktionspeicher() + "\n")
    
    #Button führt bei Betätigung Logig der Funktion aus
    button = tk.Button(transaktion_löschen_frame, text="Löschen", command=ausfuehren)
    button.grid(row=3, column=0, columnspan=2, pady=10)
    
    
    

def budget_setzen():
    
    #alte fenster schließen
    fenster_schließen()
    
    #öffnet neues fenster
    budget_setzen_frame.pack(fill="both", expand=1)
    
    #Text und Eingabefelder
    
    
    welche_kategorie_text = tk.Label(budget_setzen_frame, text="Für welche Kategorie soll ein Budget festgelegt werden?", font=('Arial', 12))
    welche_kategorie_text.grid(row=1, column=0)
    
    welche_kategorie_eingabe = ttk.Combobox(budget_setzen_frame, values=unterkategorie_liste)
    welche_kategorie_eingabe.grid(row=1, column=1, padx=10)
    
    hoehe_budget_text = tk.Label(budget_setzen_frame, text="Wie hoch ist das Budget?", font=('Arial', 12))
    hoehe_budget_text.grid(row=2, column=0)
    
    hoehe_budget_eingabe = tk.Entry(budget_setzen_frame, width=30, font=("Arial", 12))
    hoehe_budget_eingabe.grid(row=2, column=1, padx=10)
    
    #Logig der Funktion (wird erst ausgeführt wenn der Kopf gedrückt wurde)
    def ausfuehren ():
        vorhandene_unterkategorien = Transaktion.vorhandene_unterkategorien()
        if not vorhandene_unterkategorien:
            tk.messagebox.showinfo("Info", "Es gibt keine vorhandenen Unterkategorien.")
            return
        kategorie = welche_kategorie_eingabe.get()
        if kategorie is None or kategorie not in vorhandene_unterkategorien:
            tk.messagebox.showerror("Fehler", f"Die Kategorie '{kategorie}' existiert nicht.")
            return
        try:
            betrag = hoehe_budget_eingabe.get()
            if betrag is None:
                return
            budgets[kategorie] = betrag
            tk.messagebox.showinfo("Erfolg", f"Das Budget für {kategorie} wurde auf {betrag} gesetzt.")
        except ValueError:
            tk.messagebox.showerror("Fehler", "Ungültiger Betrag")
    
    #Button führt bei Betätigung Logig der Funktion aus
    button = tk.Button(budget_setzen_frame, text="Budget setzen", command=ausfuehren)
    button.grid(row=3, column=1, columnspan=2, pady=10) 
    
    
#BUG: check_budget ruft keine gespeicherten Daten auf. Transaktionen und Budgets aus vorherigen Sitzungen werden nicht abgerufen.
#BUG: check_budget ruft keine gespeicherten Daten auf. Transaktionen und Budgets aus vorherigen Sitzungen werden nicht abgerufen.
#BUG: check_budget ruft keine gespeicherten Daten auf. Transaktionen und Budgets aus vorherigen Sitzungen werden nicht abgerufen.

def check_budget():
    
    #alte fenster schließen
    fenster_schließen()
    
    #öffnet neues fenster
    budget_check_frame.pack(fill="both", expand=1)
    
    #Text und Eingabefelder
    jahr_text = tk.Label(budget_check_frame, text="Jahr:", font=('Arial', 12))
    jahr_text.grid(row=1, column=0)
    
    jahr_eingabe = tk.Entry(budget_check_frame, width=30, font=("Arial", 12))
    jahr_eingabe.grid(row=1, column=1, padx=10)
    
    monat_text = tk.Label(budget_check_frame, text="Monat:", font=('Arial', 12))
    monat_text.grid(row=2, column=0)
    
    monat_eingabe = tk.Entry(budget_check_frame, width=30, font=("Arial", 12))
    monat_eingabe.grid(row=2, column=1, padx=10)
    
    #Logig der Funktion (wird erst ausgeführt wenn der Kopf gedrückt wurde)
    def ausfuehren ():
        
        jahr = int(jahr_eingabe.get())
        monat = int(monat_eingabe.get())
        
        total_income = 0
        total_expenses = 0
        for tran in transaktionsliste:
            if tran.datum.year == jahr and tran.datum.month == monat:
                if tran.kategorie == "Einnahme":
                    total_income += tran.betrag
                elif tran.kategorie == "Ausgabe":
                    total_expenses += tran.betrag
    
        info = f"Total Einnahmen: {total_income}€, Total Ausgaben: {total_expenses}€ für {jahr}-{monat}"
    
        for unterkategorie, budget in budgets.items():
            spent = sum(tran.betrag for tran in transaktionsliste if tran.unterkategorie == unterkategorie and tran.datum.year == jahr and tran.datum.month == monat)
            if int(spent) > int(budget):
                info += f"\n{unterkategorie}: Budget: {budget}€, Ausgaben: {spent}€ für {jahr}-{monat}, Budget überschritten"
            else:
                info += f"\n{unterkategorie}: Budget: {budget}€, Ausgaben: {spent}€ für {jahr}-{monat}, Im Budget"
        
        tk.messagebox.showinfo("Budget Info", info)
    
    #Button führt bei Betätigung Logig der Funktion aus
    button = tk.Button(budget_check_frame, text="Budget checken", command=ausfuehren)
    button.grid(row=3, column=1, columnspan=2, pady=10) 
    
def budget_ueberwachung():
    fenster_schließen()
    
    grafische_auswertungen_frame.pack(fill="both", expand=1)
    
    def create_budget_comparison_chart():
        if not budgets:
            tk.messagebox.showinfo("Information", "Es sind keine Budgets festgelegt.")
            return
        
        budget_values = []
        expense_values = []
        categories = list(budgets.keys())
        
        for category in categories:
            budget_values.append(float(budgets[category]))
            expenses = sum(
                t.betrag for t in transaktionsliste
                if t.kategorie == "Ausgabe" and t.unterkategorie == category
            )
            expense_values.append(abs(expenses))

        if not budget_values:
            tk.messagebox.showinfo("Information", "Keine Ausgaben verfügbar, um ein Diagramm zu erstellen.")
            return

        chart_window = tk.Toplevel()
        chart_window.title("Budgetüberwachung")

        fig, ax = plt.subplots()
        bar_width = 0.35
        index = range(len(categories))
        
        bars1 = ax.bar(index, budget_values, bar_width, label='Budget')
        bars2 = ax.bar([i + bar_width for i in index], expense_values, bar_width, label='Ausgaben')

        ax.set_xlabel('Kategorien')
        ax.set_ylabel('Beträge (€)')
        ax.set_title('Budget vs. Ausgaben')
        ax.set_xticks([i + bar_width / 2 for i in index])
        ax.set_xticklabels(categories)
        ax.legend()

        for bar in bars1 + bars2:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.05, round(yval, 2), ha='center', va='bottom')

        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    # Button zur Anzeige des Diagramms
    button = tk.Button(grafische_auswertungen_frame, text="Budgetüberwachung anzeigen", command=create_budget_comparison_chart)
    button.grid(row=1, column=0, pady=10)
 

def neue_transaktion_fenster():
    
    #alte fenster schließen
    fenster_schließen()
    
    #öffnet neues fenster
    neue_transaktion_frame.pack(fill="both", expand=1)
    
    #Logig der Funktion (wird erst ausgeführt wenn der Kopf gedrückt wurde)
    def ausfuehren():
        try:
            betrag = float(entry_betrag.get())
            unterkategorie = entry_unterkategorie.get()
            datum = d.datetime.strptime(entry_datum.get(), "%d%m%Y")
            Transaktion.neue_transaktion(betrag, unterkategorie, datum)

        except ValueError:
            tk.messagebox.showerror("Fehler", "Ungültige Eingabe")
    
    #Text und Eingabefelder
    tk.Label( neue_transaktion_frame, text="Betrag (+/-):").grid(row=0, column=0)
    entry_betrag = tk.Entry( neue_transaktion_frame)
    entry_betrag.grid(row=0, column=1)

    tk.Label(neue_transaktion_frame, text="Unterkategorie:").grid(row=1, column=0)
    entry_unterkategorie = ttk.Combobox(neue_transaktion_frame, values=unterkategorie_liste)
    entry_unterkategorie.grid(row=1, column=1)

    tk.Label( neue_transaktion_frame, text="Datum (TTMMJJJJ):").grid(row=2, column=0)
    entry_datum = tk.Entry( neue_transaktion_frame)
    entry_datum.insert(0, d.datetime.now().strftime("%d%m%Y"))
    entry_datum.grid(row=2, column=1)
    
    #Button führt bei Betätigung Logig der Funktion aus
    button = tk.Button( neue_transaktion_frame, text="Hinzufügen", command=ausfuehren)
    button.grid(row=3, column=0, columnspan=2, pady=10)
    
    

def kontostand_umsatz():
    Kontostand = 0
    Ausgaben = 0
    Einnahmen = 0

    for transaktion in transaktionsliste:
        if transaktion.kategorie == "Ausgabe":
            Ausgaben += transaktion.betrag
        elif transaktion.kategorie == "Einnahme":
            Einnahmen += transaktion.betrag
    Kontostand = Einnahmen + Ausgaben

    info = f"Kontostand beträgt: {Kontostand}\nAusgaben betragen: {Ausgaben}\nEinnahmen betragen: {Einnahmen}"

    tk.messagebox.showinfo("Kontostand und Umsatz", info)
    
    

def zeitraumfilter():
    
    #alte fenster schließen
    fenster_schließen()
    
    #öffnet neues fenster
    zeitraumfilter_frame.pack(fill="both", expand=1)
    
    #Text und Eingabefelder
    start_text = tk.Label(zeitraumfilter_frame, text="Startdatum (TTMMJJJ):", font=('Arial', 12))
    start_text.grid(row=1, column=0)
    
    start_eingabe = tk.Entry(zeitraumfilter_frame, width=30, font=("Arial", 12))
    start_eingabe.grid(row=1, column=1, padx=10)
    
    ende_text = tk.Label(zeitraumfilter_frame, text="Enddatum (TTMMJJJ):", font=('Arial', 12))
    ende_text.grid(row=2, column=0)
    
    ende_eingabe = tk.Entry(zeitraumfilter_frame, width=30, font=("Arial", 12))
    ende_eingabe.grid(row=2, column=1, padx=10)
    
    #Logig der Funktion (wird erst ausgeführt wenn der Kopf gedrückt wurde)
    def ausfuehren ():
        try:
            startdatum_str = start_eingabe.get()
            enddatum_str = ende_eingabe.get()
            startdatum = d.datetime.strptime(startdatum_str, "%d%m%Y")
            enddatum = d.datetime.strptime(enddatum_str, "%d%m%Y")
    
            gefilterte_transaktionen = [transaktion for transaktion in transaktionsliste if startdatum <= transaktion.datum <= enddatum]
    
            anzeigen_transaktionen_filter(gefilterte_transaktionen)
        except ValueError:
            tk.messagebox.showerror("Fehler", "Ungültige Eingabe!")

    #Button führt bei Betätigung Logig der Funktion aus
    button = tk.Button(zeitraumfilter_frame, text="Zeitraumfilter anwenden", command=ausfuehren)
    button.grid(row=3, column=1, columnspan=2, pady=10) 




def grafische_auswertungen():
    
    fenster_schließen()
    
    grafische_auswertungen_frame.pack(fill="both", expand=1)
    
    def create_pie_chart_window():
        categories = {}
        for tran in transaktionsliste:
            if tran.getKategorie() == "Ausgabe":
                if tran.getUnterkategorie() in categories:
                    categories[tran.getUnterkategorie()] += abs(tran.getBetrag())
                else:
                    categories[tran.getUnterkategorie()] = abs(tran.getBetrag())
        
        if not categories:
            messagebox.showinfo("Information", "Keine Ausgaben verfügbar, um ein Diagramm zu erstellen.")
            return

        chart_window = tk.Toplevel()
        chart_window.title("Ausgaben-Diagramm")

        fig, ax = plt.subplots()
        ax.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Gleichmäßige Darstellung

        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        
        
    def create_bar_chart_window():
        # Сбор данных для гистограммы
        monthly_expenses = {}
        for tran in transaktionsliste:
            if tran.getKategorie() == "Ausgabe":
                key = tran.getDatum().strftime('%Y-%m')
                if key in monthly_expenses:
                    monthly_expenses[key] += abs(tran.getBetrag())
                else:
                    monthly_expenses[key] = abs(tran.getBetrag())

        if not monthly_expenses:
            messagebox.showinfo("Information", "Keine Ausgaben verfügbar, um ein Diagramm zu erstellen.")
            return

        months = list(monthly_expenses.keys())
        expenses = list(monthly_expenses.values())

        chart_window = tk.Toplevel()
        chart_window.title("Monatliche Ausgaben")

        fig, ax = plt.subplots()
        ax.bar(months, expenses)
        ax.set_xlabel("Monat")
        ax.set_ylabel("Ausgaben (€)")
        ax.set_title("Monatliche Ausgaben")

        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    #Button führt bei Betätigung Logig der Funktion aus
    button = tk.Button(grafische_auswertungen_frame, text="Pie Chart", command=create_pie_chart_window)
    button.grid(row=3, column=1, columnspan=2, pady=10) 
    
    #Button führt bei Betätigung Logig der Funktion aus
    button2 = tk.Button(grafische_auswertungen_frame, text="Bar Chart", command=create_bar_chart_window)
    button2.grid(row=3, column=3, columnspan=2, pady=10) 
    
    #hier gerne die Grafiken einfügen und schauen wie es aussieht. Können uns gerne abprechen wie das UI hier aussehen soll.
    #Beachte: die Grafiken müssen in "grafische_auswertungen_frame" eingefügt werden damit sie sichtbar sind.





transaktionsliste = Transaktion.transaktion_lesen2()

#Startfenster
root = tk.Tk()
root.geometry("800x800")
root.title('Finanzrechner der Codemasters')

#Menüleiste erstellen
menuleiste = tk.Menu(root)

#Menükomponenten erstellen
reiter_transaktion = tk.Menu(menuleiste)
reiter_budget = tk.Menu(menuleiste)
reiter_sonstiges = tk.Menu(menuleiste)

#Menüeinträge erstellen
reiter_transaktion.add_command(label="Neue Transaktion hinzufügen", command=neue_transaktion_fenster)
reiter_transaktion.add_command(label="Transaktion löschen", command=loeschen_transaktionen)
reiter_transaktion.add_command(label="Transaktion anzeigen", command=anzeigen_transaktionen)

reiter_budget.add_command(label="Budget planen", command=budget_setzen)
reiter_budget.add_command(label="Budget checken", command=check_budget)
reiter_budget.add_command(label="Budget überwachen", command=budget_ueberwachung)


reiter_sonstiges.add_command(label="Konten anzeigen", command=kontostand_umsatz)
reiter_sonstiges.add_command(label="Zeitraumfilter", command=zeitraumfilter)
reiter_sonstiges.add_command(label="Grafische Auswertungen", command=grafische_auswertungen)

#Menükomponenten in der Menüleiste platzieren
menuleiste.add_cascade(label="Transaktion", menu=reiter_transaktion)
menuleiste.add_cascade(label="Budget", menu=reiter_budget)
menuleiste.add_cascade(label="Sonstiges", menu=reiter_sonstiges)

#Menüleiste an Fenster übergeben
root.config(menu=menuleiste)

#Frames erstellen
neue_transaktion_frame = tk.Frame(root, width=800, height=800)
transaktion_löschen_frame = tk.Frame(root, width=800, height=800)
budget_setzen_frame = tk.Frame(root, width=800, height=800)
budget_check_frame = tk.Frame(root, width=800, height=800)
zeitraumfilter_frame = tk.Frame(root, width=800, height=800)
grafische_auswertungen_frame = tk.Frame(root, width=800, height=800)

Transaktion.transaktion_lesen2()
root.mainloop()
