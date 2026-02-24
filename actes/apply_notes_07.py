#!/usr/bin/env python3
# -*- coding: utf-8 -*-

with open('/Users/christophe.thiebaud/_Mugnier/actes/acte_07.tex', 'r', encoding='utf-8') as f:
    content = f.read()

substitutions = [
    # 1. Couvent des Ursulines + capitaine Broutin
    (
        "couvent des Ursulines de la Nouvelle-Orléans, œuvre du capitaine Broutin",
        r"couvent des Ursulines\nf{Le couvent des Ursulines de la Nouvelle-Orléans (Louisiane) est l'un des plus anciens bâtiments subsistants des États-Unis, construit entre 1745 et 1752 par l'ingénieur militaire français Ignace François Broutin (vers 1690--1751), architecte officiel de la colonie française de Louisiane. Il abrita d'abord l'École des Ursulines, puis servit de diverses fonctions administratives et religieuses. \textit{Source :} \textup{fr.wikipedia.org/wiki/Couvent\_des\_Ursulines\_de\_La\_Nouvelle-Orl\%C3\%A9ans}} de la Nouvelle-Orléans, œuvre du capitaine Broutin\nf{Ignace François Broutin (vers 1690--1751), ingénieur militaire, cartographe et architecte officiel de la colonie française de Louisiane, est notamment l'auteur des plans du couvent des Ursulines de la Nouvelle-Orléans, l'un des plus anciens édifices conservés des États-Unis. \textit{Source :} \textup{fr.wikipedia.org/wiki/Ignace\_Fran\%C3\%A7ois\_Broutin}}"
    ),
    # 2. Ludwig Mies van der Rohe
    (
        "Ludwig Mies van der Rohe",
        r"Ludwig Mies van der Rohe\nf{Ludwig Mies van der Rohe (1886--1969), architecte allemand naturalisé américain, figure majeure du mouvement moderne et du style international. Codirecteur du Bauhaus (1930--1933), il est notamment l'auteur du pavillon allemand de Barcelone (1929) et de la Seagram Building à New York (1958). \textit{Source :} \textup{fr.wikipedia.org/wiki/Ludwig\_Mies\_van\_der\_Rohe}}"
    ),
    # 3. Gustav Nachtigal
    (
        "Gustav Nachtigal, représentant de Bismarck",
        r"Gustav Nachtigal\nf{Gustav Nachtigal (1834--1885), explorateur et diplomate prussien, fut chargé par Bismarck d'établir des protectorats allemands en Afrique occidentale et méridionale. En 1884, il proclama le protectorat allemand sur le Togo et le Cameroun, puis sur le Sud-Ouest africain (actuelle Namibie). \textit{Source :} \textup{fr.wikipedia.org/wiki/Gustav\_Nachtigal}}, représentant de Bismarck"
    ),
    # 4. Heinrich Göring
    (
        "Heinrich Göring, le père d'Hermann",
        r"Heinrich Göring\nf{Heinrich Ernst Göring (1839--1913), juriste et fonctionnaire colonial allemand, fut le premier gouverneur général du Sud-Ouest africain allemand (Namibie actuelle) à partir de 1885. Il est le père du maréchal Hermann Göring, futur dirigeant nazi. \textit{Source :} \textup{fr.wikipedia.org/wiki/Heinrich\_Ernst\_G\%C3\%B6ring}}, le père d'Hermann"
    ),
]

count = 0
for old, new in substitutions:
    if old in content:
        content = content.replace(old, new, 1)
        count += 1
        print(f'✓ {old[:60]}')
    else:
        print(f'✗ NOT FOUND: {old[:60]}')

with open('/Users/christophe.thiebaud/_Mugnier/actes/acte_07.tex', 'w', encoding='utf-8') as f:
    f.write(content)
print(f'\nApplied {count} substitutions to acte_07.tex')
