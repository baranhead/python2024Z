def tekstPowitania(jezyk):
    dict = {}

    dict["en"] = "Hello!"
    dict["de"] = "Hallo!"
    dict["fr"] = "Bonjour!"
    dict["it"] = "Buongiorno!"

    if jezyk not in dict:
        print(f"\nNie znam jezyka {jezyk}.")
    else:
        print(f"\n{dict[jezyk]}")

def powitaj():
    dict = {}

    #angielski: https://pl.pons.com/t%C5%82umaczenie-2/polski-angielski/cze%C5%9B%C4%87?q=cze%C5%9B%C4%87%21
    dict["en"] = "angielski"

    #niemiecki: https://pl.pons.com/t%C5%82umaczenie-2/polski-niemiecki/cze%C5%9B%C4%87?q=cze%C5%9B%C4%87%21
    dict["de"] = "niemiecki"

    #francuski: https://pl.pons.com/t%C5%82umaczenie-2/polski-francuski/dzie%C5%84+dobry?q=dzie%C5%84+dobry
    dict["fr"] = "francuski"

    #wloski: https://pl.pons.com/t%C5%82umaczenie/polski-w%C5%82oski/dzie%C5%84+dobry
    dict["it"] = "wloski"

    print("Dostepne jezyki:")

    for key in dict.keys():
        print(f"\n{key} - {dict[key]}")

    language = input("\nPodaj wybrany jezyk:")
    tekstPowitania(language)

    dict.clear()


powitaj()