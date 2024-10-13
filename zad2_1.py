#Funkcja dodajaca aktywnosc do slownika
def add_activity(dict):

    act = input("Wpisz nazwe aktywnosci: ")
    time = float(input("Wpisz, ile czasu poswieciles tej aktywnosci (w godzinach): "))
    
    if act not in dict:
        dict[act] = [time]
    else:
        dict[act] += [time]

#Funkcja pozwalajaca sprawdzic, ile czasu uzytkownik spedzil na danej aktywnosci
def show_time(dict):
    act = input("Wpisz, jakiej aktywnosci laczny czas chcialbys sprawdzic:")

    if act in dict:
        total = 0
        for elm in dict[act]:
            total += elm
        print(f"\nNa aktywnosci {act} spedziles lacznie {total} godzin.")
    else:
        print("\nNie uprawiales takiej aktywnosci")

#Funkcja pokazujaca 3 najbardziej czasochlonne aktywnosci uzytkownika
def top_activities(dict):

    lst = []
    for key in dict:
        total = 0
        for elm in dict[key]:
            total += elm
        lst += [(total, key)]

    lst = sorted(lst, reverse=True)
    
    if len(lst) == 0:
        print("\nNie uprawiales zadnych aktywnosci")
    else:
        if len(lst) < 3:
            print (f"\nNie uprawiales co najmniej trzech roznych aktywnosci, pokazmy wszystkie")

        for i in range(0, min(len(lst), 3)):
            print(lst[i][1])
        

# Program wypisuje na ekran menu wyboru i konczy sie po wybraniu opcji nr 4
dict = {}
loop = True
while(loop):

    print("\nMenu:")
    print("1. Dodaj aktywność")
    print("2. Pokaż czas")
    print("3. Pokaż topowe aktywności")
    print("4. Zakoncz")


    choice = input("Wybierz opcje (wpisz odpowiednia cyfre): ")

    if choice == '1':
        add_activity(dict)
    elif choice == '2':
        show_time(dict)
    elif choice == '3':
        top_activities(dict)
    elif choice == '4':
        loop = False
    else:
        print("Prosze wpisac liczbe od 1 do 4")

dict.clear()



