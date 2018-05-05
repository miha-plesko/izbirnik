# Izbirnik

Izbirnik je program, ki omogoča iskanje datoteke v vhodni mapi in ponudi gumb
za hitro kopiranje v izhodno mapo.

Program išče datoteko glede na vnešeno ime (regularni izraz). Datoteko išče v
vhodni mapi ali podmapi vhodne mape na neomejeni globini. Najdeni zadetki se
prikažejo v obliki novih gumbov. Ob kliku na takšen gumb se datoteka skopira v
izhodno mapo.

## Konfiguracija
Poleg samega programa (izbirnik.exe) je potrebno ustvariti konfiguracijsko datoteko
z imenom `izbirnik.yaml` in jo shraniti v isto mapo kot program. Vsebina datoteke mora
biti sledeče oblike:

```yaml
vhodne_mape:
- C:\Users\Janez\Projekti\naročila1
- C:\Users\Janez\Projekti\naročila2
- C:\Users\Janez\Projekti\naročila3

koncnice:
- .txt
- .docx

izhodna_mapa: C:\Users\Janez\Projekti\začasno
```

Parameter `vhodne_mape` definira poti do vhodnih map. V zgornjem primeru so to
`C:\Users\Janez\Projekti\naročila1`, `C:\Users\Janez\Projekti\naročila2` in
`C:\Users\Janez\Projekti\naročila3`. To pomeni, da se bo datoteko iskalo po teh treh mapah
in vseh njenih podmapah.

Parameter `koncince` omeji prikaz datotek le na tiste z ujemajočo se končnico. V zgornjem
primeru sta to končnici `.txt` in `.docx`. Če želimo prikazati vse datoteke ne glede na
končnico, lahko uporabimo vrednost

```yaml
koncnice:
- .*
```

Parameter `izhodna_mapa` definira pot do izhodne mape. V zgornjem primeru je to
`C:\Users\Janez\Projekti\začasno`. To pomeni, da se bo najdeno datoteko skopiralo
v to mapo.

# Dokumentacija za razvijalce

## Prevajanje
Najprej namestim pyinstaller:

```bash
pip install pyinstaller
```

Nato ga uporabim:

```bash
pyinstaller -wF izbirnik.py
```
