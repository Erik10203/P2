# Erste Ideen zum Konzept:
Grundsätzliche Idee von mir ist, dass wir mit verschiedenen Listen arbeiten. 
Dabei bauen wie die Listen so auf das die Stellen (Index) das Kriterium ist mit der wir die Listen zusammenführen.

Bsp.1: 
        import datetime as d
        ListeUmsatz = [200, 30, -45]
        x1 = d.datetime(2024, 2, 1)
        x2 = d.datetime(2024, 2, 3)
        x3 = d.datetime(2024, 2, 5)
        listeDatum = [x1.strftime("%x"), x2.strftime("%x"), x3.strftime("%x")]
        print (ListeUmsatz)
        print (listeDatum)

output: [200, 30, -45]
        ['02/01/24', '02/03/24', '02/05/24']

Alternativ könnte man auch so vorgehen: Wir machen also eine Liste in der Liste
Bsp.2:  
        import datetime as d
        x1 = d.datetime(2024, 2, 1)
        x2 = d.datetime(2024, 2, 3)
        x3 = d.datetime(2024, 2, 5)
        ListeAlles = [(200, x1.strftime("%x")), (30, x2.strftime("%x")), (-45, x3.strftime("%x"))]
        
        print(ListeAlles)

output: [(200, '02/01/24'), (30, '02/03/24'), (-45, '02/05/24')]

In beiden Fällen würde das Einspeisen der Daten über einen append Befehl und einer Input Abfrage funktionieren.
Ich kann mir aber auch vorstellen, dass es einfacher ist, wenn wir eine Liste mit nur zahlen haben ()Bsp.1). Dann kann man leichter die Summe ziehen etc. 
Es ist dann aber auch nicht so übersichtlich..

Datum kann über das Modul Datetime gelöst werden.
P.S. Wir sollen nur Python benutzen eine Datenbank mit SQL scheidet daher aus...
