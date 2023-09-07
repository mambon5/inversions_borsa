PROGRAMA PER FER BONES INVERSIONS A BORSA

# Descarregar tots els ticks names de cada acció de borsa usant yahoo finance

Aquest programa:

1. Descarrega els tickers de yahoo per totes les accions que yahoo té excepte els indexos.
2. Els descarrega en un fitxer diferent cada cop que s'obra el programa
3. Guarda l'ultim grup de tickers descarregat per si hi ha un error d'execució, no es repeteixi la feina.

## Com descarregar i executar-lo?

Per tal d'executar el programa i descarregar tots els tick names de totes les accions que yahoo té a borsa, cal:

1. Descargar el repository de github https://github.com/mambon5/inversions_borsa.git
```
git clone https://github.com/mambon5/inversions_borsa.git
```

2. Instalar python
3. Podeu canviar el contingut de l'arxiu `last_save_ticks.txt` a `AAA` perquè comenci de a descargat tots els ticks de yahoo començant per la primera. Opcionalment podeu borrar tots els arxius `ticks_X.csv` per descartar els ticks ja descarregats i reusar tots els noms d'arxiu.
4. Executar desde una terminal de linux (o windows) el programa principal que és `yh_get_all_sym.py`
   
```
python3 yh_get_all_sym.py
```

4. Els tick names es guardaran automàticament en els fitxers "ticks_X.csv" on X és un número que va incrementant cada cop que executeu el programa per tal de no sobreescriure els arxius de ticks i que no es perdi informació que potser voleu conservar.

5. Si durant l'execució del programa, hi ha algun error de conexió o el servidor de yahoo cancela la demanada, el software guarda automàticament l'últim grup de tickers on us havíeu quedat i torna a començar la descàrrega en l'últim punt i no repeteix la feina. Així que tranquiles, és normal que falli el programa i hagueu d'executar-lo més d'un cop per descarregar tots els tickers de yahoo.

## Altres arxius inclosos

Incloc tots els arxius que he anat generant al executar el programa, hi ha molts tickers ja descarregats i guardats en format .csv per si voleu usar-los ja. 

Jo no he trobat enlloc una llista complerta de tots els tickers de les accions de yahoo i per això he fet un programa que usant el mètode de webscrapping, els troba un a un i els va escrivint a l'ordinador.

És un programa d'execució de força bruta.

## Crèdits

Originalment el programa ha estat elaborat per > https://github.com/mlapenna7/yh_symbol_universe/blob/main/yh_get_all_sym.py però no funciona, ni troba cap ticker realment. Jo he fet una sèria de modificacions que fan que le programa:
1. Funcioni i trobi els tickers de yahoo
2. els descarregi en un fitxer diferent cada cop que s'obra el programa
3. Guardi l'ultim grup de tickers descarregat per si hi ha un error d'execució, no es repeteixi la feina.

