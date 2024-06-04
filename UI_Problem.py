import datetime as d

import tkinter as tk

from tkinter import messagebox


def fenster_schließen():
    for widget in neue_transaktion_frame.winfo_children():
        widget.destroy
    
    for widget in transaktion_löschen_frame.winfo_children():
        widget.destroy
        
    neue_transaktion_frame.pack_forget()
    transaktion_löschen_frame.pack_forget()

def neue_transaktion():
    fenster_schließen()
    
    neue_transaktion_frame.pack(fill="both", expand=1)
    
    text1 = tk.Label(neue_transaktion_frame, text="Betrag:", font=('Arial', 12))
    text1.grid(row=1, column=0)
    
    global neue_transaktion_betrag
    neue_transaktion_betrag = tk.Entry(neue_transaktion_frame, width=30, font=("Arial", 12))
    neue_transaktion_betrag.grid(row=1, column=1, padx=10)
  
    text2 = tk.Label(neue_transaktion_frame, text="Kategorie:", font=('Arial', 12))
    text2.grid(row=2, column=0)
  
    global neue_transaktion_kategorie
    neue_transaktion_kategorie = tk.Entry(neue_transaktion_frame, width=30, font=("Arial", 12))
    neue_transaktion_kategorie.grid(row=2, column=1, padx=10)
    
    text3 = tk.Label(neue_transaktion_frame, text="Datum:", font=('Arial', 12))
    text3.grid(row=3, column=0)
    
    global neue_transaktion_datum
    neue_transaktion_datum = tk.Entry(neue_transaktion_frame, width=30, font=("Arial", 12))
    neue_transaktion_datum.grid(row=3, column=1, padx=10)
    
    #Wie kann man funktionen mit dem commandbefehl ansprechen???????
    #Wie kann man funktionen mit dem commandbefehl ansprechen???????
    #Wie kann man funktionen mit dem commandbefehl ansprechen???????
    
    button = tk.Button( neue_transaktion_frame, text="Transaktion hinzufügen", font=('Arial', 12), command=nachricht_neue_transaktion)
    button.grid(row=4, column=1, pady=20)
    

def nachricht_neue_transaktion(cls):
    
    nachricht = tk.Text(neue_transaktion_frame, height=5, width=30, font=('Arial', 12))
    nachricht.grid(row=5, column=1, pady=20)
    
    while True:
        try:
            betrag = int(neue_transaktion_betrag.get())
            unterkategorie = neue_transaktion_kategorie.get()
            datum_str = neue_transaktion_datum.get()
            datum_obj = d.datetime.strptime(datum_str, "%d%m%Y")

            neue_transaktion = cls(betrag, unterkategorie, datum_obj)
            cls.transaktion_speichern(neue_transaktion)
            transaktionsliste.append(neue_transaktion)
            print(f"Transaktion {neue_transaktion.nummer} hinzugefügt.")
            cls.check_fuer_budget_ueberschreitung(neue_transaktion)

            wasnu = input("Weitere Transaktion hinzufügen? (Ja/Nein) ")
            if wasnu.lower() != "ja":
                break
        except Exception as e:
            print(f"Falsche Eingabe: {e}")


def transaktion_löschen():
    fenster_schließen()
    
    transaktion_löschen_frame.pack(fill="both", expand=1)
    
    welche_transaktion_löschen_text = tk.Label(transaktion_löschen_frame, text="welche Transaktion soll gelöscht werden?", font=('Arial', 12))
    welche_transaktion_löschen_text.grid(row=1, column=0)
    
    welche_transaktion_löschen_eingabe = tk.Entry(transaktion_löschen_frame, font=("Arial", 12))
    welche_transaktion_löschen_eingabe.grid(row=1, column=1, padx=10)


    

    

def test():
    pass



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
reiter_transaktion.add_command(label="Neue Transaktion hinzufügen", command=neue_transaktion)
reiter_transaktion.add_command(label="Transaktion löschen", command=transaktion_löschen)
reiter_transaktion.add_command(label="Transaktion anzeigen", command=test)

reiter_budget.add_command(label="Budget planen")
reiter_budget.add_command(label="Budget checken")

reiter_sonstiges.add_command(label="Konten anzeigen")
reiter_sonstiges.add_command(label="Zeitraumfilter")

#Menükomponenten in der Menüleiste platzieren
menuleiste.add_cascade(label="Transaktion", menu=reiter_transaktion)
menuleiste.add_cascade(label="Budget", menu=reiter_budget)
menuleiste.add_cascade(label="Sonstiges", menu=reiter_sonstiges)

#Menüleiste an Fenster übergeben
root.config(menu=menuleiste)

#Frames erstellen
neue_transaktion_frame = tk.Frame(root, width=800, height=800)
transaktion_löschen_frame = tk.Frame(root, width=800, height=800)
transaktion_anzeigen_frame = tk.Frame(root, width=800, height=800)
budget_planen_frame = tk.Frame(root, width=800, height=800)
budget_checken_frame = tk.Frame(root, width=800, height=800)
konten_anzeigen_frame = tk.Frame(root, width=800, height=800)
Zeitraumfilter_frame = tk.Frame(root, width=800, height=800)




root.mainloop()