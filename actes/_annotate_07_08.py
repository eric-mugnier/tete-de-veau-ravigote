#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Applique les annotations \nf{…} dans acte_07.tex et acte_08.tex."""

# ──────────────────────────────────────────────────────────────
# ACTE 07
# ──────────────────────────────────────────────────────────────
with open('/Users/christophe.thiebaud/_Mugnier/actes/acte_07.tex', 'r', encoding='utf-8') as f:
    c07 = f.read()

subs07 = [

    # 1. Couvent des Ursulines + capitaine Broutin
    (
        "couvent des Ursulines de la Nouvelle-Orléans, œuvre du capitaine Broutin, ingénieur militaire, cartographe et architecte officiel de Louisiane dans les années 1700",
        r"couvent des Ursulines\nf{Le couvent des Ursulines de la Nouvelle-Orléans (Louisiane) est l'un des plus anciens édifices subsistants des États-Unis, construit entre 1745 et 1752. C'est la seule survivance intacte de l'architecture française coloniale en Amérique du Nord. Aujourd'hui classé monument historique, il abrite les archives de l'archidiocèse de La Nouvelle-Orléans. \textit{Source :} \textup{fr.wikipedia.org/wiki/Couvent\_des\_Ursulines\_de\_la\_Nouvelle-Orl\%C3\%A9ans}} de la Nouvelle-Orléans, œuvre du capitaine Broutin\nf{Ignace François Broutin (vers 1695--1751), ingénieur militaire, cartographe et architecte officiel de la colonie française de Louisiane à partir de 1728. Il est l'auteur des plans du couvent des Ursulines de la Nouvelle-Orléans (1745) et de nombreuses fortifications de la région. \textit{Source :} \textup{en.wikipedia.org/wiki/Ignace\_Fran\%C3\%A7ois\_Broutin}}, ingénieur militaire, cartographe et architecte officiel de Louisiane dans les années 1700"
    ),

    # 2. Ludwig Mies van der Rohe
    (
        "Ludwig Mies van der Rohe",
        r"Ludwig Mies van der Rohe\nf{Ludwig Mies van der Rohe (1886--1969), architecte germano-américain, l'une des figures majeures de l'architecture moderne et du style international. Dernier directeur du Bauhaus (1930--1933), il est notamment l'auteur du pavillon allemand de Barcelone (1929) et du complexe Seagram Building à New York (1958). \textit{Source :} \textup{fr.wikipedia.org/wiki/Ludwig\_Mies\_van\_der\_Rohe}}"
    ),

    # 3. Gustav Nachtigal
    (
        "un explorateur prussien du nom de Gustav Nachtigal, représentant de Bismarck",
        r"un explorateur prussien du nom de Gustav Nachtigal\nf{Gustav Nachtigal (1834--1885), médecin militaire et explorateur prussien. Envoyé par Bismarck en Afrique en 1884, il proclama les protectorats allemands sur le Togo, le Cameroun et le Sud-Ouest africain (actuelle Namibie). Il mourut en mer lors de son voyage de retour. \textit{Source :} \textup{fr.wikipedia.org/wiki/Gustav\_Nachtigal}}, représentant de Bismarck\nf{Otto von Bismarck (1815--1898), homme d'État prussien puis allemand, dit le «~Chancelier de fer~». Artisan de l'unification allemande (1871) et chancelier du Reich jusqu'en 1890, il fut à l'origine de la politique coloniale africaine de l'Allemagne dans les années 1880. \textit{Source :} \textup{fr.wikipedia.org/wiki/Otto\_von\_Bismarck}}"
    ),

    # 4. Heinrich Göring / Hermann Göring
    (
        "son successeur, Heinrich Göring, le père d'Hermann",
        r"son successeur, Heinrich Göring\nf{Heinrich Ernst Göring (1839--1913), juriste et haut fonctionnaire colonial allemand. Premier commissaire impérial du Sud-Ouest africain allemand (actuelle Namibie) à partir de 1885, il fut chargé de soumettre les populations locales. Il est le père du maréchal Hermann Göring. \textit{Source :} \textup{en.wikipedia.org/wiki/Heinrich\_Ernst\_G\%C3\%B6ring}}, le père d'Hermann\nf{Hermann Göring (1893--1946), maréchal du Reich et principal dirigeant nazi après Hitler. Fondateur de la Gestapo, commandant en chef de la Luftwaffe et responsable du plan quadriennal, il fut condamné à mort au procès de Nuremberg et se suicida la veille de son exécution. \textit{Source :} \textup{fr.wikipedia.org/wiki/Hermann\_G\%C3\%B6ring}}"
    ),

]

count07 = 0
for old, new in subs07:
    if old in c07:
        c07 = c07.replace(old, new, 1)
        count07 += 1
        print(f'07 ✓  {old[:65]}')
    else:
        print(f'07 ✗  NOT FOUND: {old[:65]}')

with open('/Users/christophe.thiebaud/_Mugnier/actes/acte_07.tex', 'w', encoding='utf-8') as f:
    f.write(c07)
print(f'\nacte_07.tex : {count07} substitutions appliquées\n')


# ──────────────────────────────────────────────────────────────
# ACTE 08
# ──────────────────────────────────────────────────────────────
with open('/Users/christophe.thiebaud/_Mugnier/actes/acte_08.tex', 'r', encoding='utf-8') as f:
    c08 = f.read()

subs08 = [

    # 1. Forest Whitaker / Ghost Dog
    (
        "tel Forest Whitaker dans Ghost Dog",
        r"tel Forest Whitaker\nf{Forest Whitaker (né en 1961), acteur américain, révélé par \textit{Bird} (Clint Eastwood, 1988) et oscarisé pour \textit{Le Dernier Roi d'Écosse} (2006). \textit{Source :} \textup{fr.wikipedia.org/wiki/Forest\_Whitaker}} dans \textit{Ghost Dog}\nf{\textit{Ghost Dog, la voie du samouraï} (1999), film de Jim Jarmusch avec Forest Whitaker dans le rôle d'un tueur à gages urbain vivant selon le code du bushido. La bande originale est de RZA (Wu-Tang Clan). \textit{Source :} \textup{fr.wikipedia.org/wiki/Ghost\_Dog,\_la\_voie\_du\_samoura\%C3\%AF}}"
    ),

    # 2. Corey «~Raekwon~» Woods
    (
        "Corey «\u00a0Raekwon\u00a0» Woods gravissant un par un les échelons menant à la salle des Cinq Dragons",
        r"Corey «\u00a0Raekwon\u00a0» Woods\nf{Corey Woods, dit Raekwon (né en 1970), rappeur américain, membre fondateur du Wu-Tang Clan. Son album solo \textit{Only Built 4 Cuban Linx\ldots} (1995) est considéré comme un classique du rap new-yorkais. La «~salle des Cinq Dragons~» renvoie au film \textit{La 36\up{e} Chambre de Shaolin} (Shaw Brothers, 1978), référence majeure dans l'univers du Wu-Tang Clan. \textit{Source :} \textup{fr.wikipedia.org/wiki/Raekwon}} gravissant un par un les échelons menant à la salle des Cinq Dragons"
    ),

    # 3. 36e Chambre de Shaolin
    (
        "San Te affrontant le général Sien Ta dans la 36e Chambre de Shaolin",
        r"San Te affrontant le général Sien Ta dans \textit{La 36\up{e} Chambre de Shaolin}\nf{\textit{La 36\up{e} Chambre de Shaolin} (1978), film de kung-fu hongkongais réalisé par Lau Kar-leung, produit par la Shaw Brothers, avec Gordon Liu dans le rôle de San Te. Considéré comme l'un des films d'arts martiaux les plus influents du XXe siècle, il a notamment inspiré le nom du groupe Wu-Tang Clan. \textit{Source :} \textup{fr.wikipedia.org/wiki/La\_36\%C3\%A8me\_chambre\_de\_Shaolin}}"
    ),

    # 4. GBU-57 / Lockheed Martin / Boeing / Northrop Grumman
    (
        "bombe anti-bunker GBU-57 de l'US Air Force, fascinant concentré de technologie développé par Lockheed Martin, Boeing et la Northrop Grumman Corporation",
        r"bombe anti-bunker GBU-57\nf{La GBU-57 \textit{Massive Ordnance Penetrator} (MOP) est la bombe conventionnelle la plus puissante de l'arsenal américain : 13\,600 kg, capable de pénétrer plus de 60 mètres de béton armé avant d'exploser. Conçue pour neutraliser des installations militaires souterraines fortifiées. \textit{Source :} \textup{en.wikipedia.org/wiki/GBU-57\_MOP}} de l'US Air Force, fascinant concentré de technologie développé par Lockheed Martin\nf{Lockheed Martin Corporation, géant américain de l'industrie de défense et de l'aérospatiale, né en 1995 de la fusion de Lockheed Corporation et Martin Marietta. Premier contractant de défense mondial, il est notamment le fabricant du chasseur furtif F-35. \textit{Source :} \textup{fr.wikipedia.org/wiki/Lockheed\_Martin}}, Boeing\nf{Boeing Company, constructeur aéronautique américain fondé en 1916, l'un des deux premiers fabricants mondiaux d'avions civils (avec Airbus) et important contractant de défense. \textit{Source :} \textup{fr.wikipedia.org/wiki/Boeing}} et la Northrop Grumman Corporation\nf{Northrop Grumman Corporation, entreprise américaine de défense et d'aérospatiale fondée en 1994. Fabricant notamment du bombardier furtif B-2 Spirit et des systèmes de détection spatiale. \textit{Source :} \textup{fr.wikipedia.org/wiki/Northrop\_Grumman}}"
    ),

    # 5. Lovecraft / Sheridan Le Fanu / Montague Rhodes James
    (
        "d'un Lovecraft, un Sheridan Le Fanu ou un Montague Rhodes James pour n'en citer que quelques-uns",
        r"d'un Lovecraft\nf{Howard Phillips Lovecraft (1890--1937), écrivain américain de fantastique et d'horreur cosmique, créateur du «~Mythe de Cthulhu~». Ses œuvres majeures comprennent \textit{L'Appel de Cthulhu} (1928) et \textit{Les Montagnes hallucinées} (1936). \textit{Source :} \textup{fr.wikipedia.org/wiki/H.\_P.\_Lovecraft}}, un Sheridan Le Fanu\nf{Joseph Sheridan Le Fanu (1814--1873), romancier et nouvelliste irlandais, maître du récit gothique victorien. Auteur de \textit{Carmilla} (1872), roman fondateur du genre vampire, et de \textit{L'Oncle Silas} (1864). \textit{Source :} \textup{fr.wikipedia.org/wiki/Sheridan\_Le\_Fanu}} ou un Montague Rhodes James\nf{Montague Rhodes James (1862--1936), érudit médiéviste et écrivain britannique. Ses recueils de \textit{Ghost Stories of an Antiquary} (1904 et suiv.) sont considérés comme des modèles du genre fantastique anglais. \textit{Source :} \textup{en.wikipedia.org/wiki/M.\_R.\_James}} pour n'en citer que quelques-uns"
    ),

    # 6. Raymond Maufrais / Mato Grosso
    (
        "dans la peau de Raymond Maufrais se frayant un chemin à coups de machette dans la jungle du Mato Grosso",
        r"dans la peau de Raymond Maufrais\nf{Raymond Maufrais (1926--1950 ?), aventurier et écrivain français, disparu lors d'une expédition solitaire en Guyane en 1950. Ses carnets de route, publiés à titre posthume, et les recherches désespérées de son père Edgar ont connu un grand retentissement en France. \textit{Source :} \textup{fr.wikipedia.org/wiki/Raymond\_Maufrais}} se frayant un chemin à coups de machette dans la jungle du Mato Grosso\nf{Le Mato Grosso (littéralement «~forêt épaisse~» en portugais) est un État du Brésil central, couvert en grande partie par la forêt amazonienne et le Pantanal. C'est l'une des régions les plus sauvages et les moins accessibles d'Amérique du Sud. \textit{Source :} \textup{fr.wikipedia.org/wiki/Mato\_Grosso}}"
    ),

    # 7. Fliess
    (
        "Fliess (je recommande à tous la lecture des «\u00a0relations entre le nez et les organes génitaux féminins présentés selon leur signification biologique\u00a0», indispensable)",
        r"Fliess\nf{Wilhelm Fliess (1858--1928), médecin oto-rhino-laryngologiste et biologiste allemand, ami intime et correspondant de Freud pendant une décennie. Son ouvrage \textit{Les Relations entre le nez et les organes génitaux féminins présentés selon leur signification biologique} (1897) défendait des théories sur les cycles biologiques aujourd'hui réfutées. \textit{Source :} \textup{fr.wikipedia.org/wiki/Wilhelm\_Fliess}} (je recommande à tous la lecture des «\u00a0relations entre le nez et les organes génitaux féminins présentés selon leur signification biologique\u00a0», indispensable)"
    ),

    # 8. Breuer / Bertha Pappenheim / Anna O.
    (
        "Breuer (ses remarquables travaux sur l'hystérie, notamment le cas de la militante féministe et polyglotte Bertha Pappenheim, alias Anna O.)",
        r"Breuer\nf{Josef Breuer (1842--1925), médecin viennois, pionnier de la psychanalyse. Ses \textit{Études sur l'hystérie} (1895), coécrites avec Freud, fondèrent la méthode cathartique à travers plusieurs cas cliniques dont celui d'Anna O. \textit{Source :} \textup{fr.wikipedia.org/wiki/Josef\_Breuer}} (ses remarquables travaux sur l'hystérie, notamment le cas de la militante féministe et polyglotte Bertha Pappenheim\nf{Bertha Pappenheim (1859--1936), femme juive allemande traitée par Breuer sous le pseudonyme d'«~Anna O.~» dans les \textit{Études sur l'hystérie} (1895). Guérie, elle devint une figure majeure du féminisme et du travail social allemand, fondatrice de la Ligue des femmes juives (1904). \textit{Source :} \textup{fr.wikipedia.org/wiki/Bertha\_Pappenheim}}, alias Anna O.)"
    ),

    # 9. La Voisin / Giulia Tofana / Hélène Jégado / Marie Besnard / Chisako Kakehi
    (
        "la Voisin, la Giulia Tofana, l'Hélène Jégado, la Marie Besnard, la Chisako Kakehi du sixième",
        r"la Voisin\nf{Catherine Deshayes, dite La Voisin (vers 1640--1680), empoisonneuse française, figure centrale de l'«~Affaire des poisons~» qui ébranla la cour de Louis XIV. Accusée de vendre des poisons, des philtres et de pratiquer des avortements, elle fut brûlée en place de Grève le 22 février 1680. \textit{Source :} \textup{fr.wikipedia.org/wiki/La\_Voisin}}, la Giulia Tofana\nf{Giulia Tofana (vers 1620--1659), empoisonneuse sicilienne célèbre pour avoir fabriqué l'\textit{Aqua Tofana}, poison arsenical dont elle aurait vendu la recette à des femmes souhaitant se débarrasser de leur mari. On lui attribue jusqu'à 600 victimes. Exécutée à Rome. \textit{Source :} \textup{fr.wikipedia.org/wiki/Giulia\_Tofana}}, l'Hélène Jégado\nf{Hélène Jégado (1803--1852), servante bretonne considérée comme l'une des plus grandes empoisonneuses de l'histoire de France. On lui attribue entre vingt-trois et trente-six meurtres à l'arsenic sur plusieurs décennies. Guillotinée à Rennes le 26 février 1852. \textit{Source :} \textup{fr.wikipedia.org/wiki/H\%C3\%A9l\%C3\%A8ne\_J\%C3\%A9gado}}, la Marie Besnard\nf{Marie Besnard (1896--1980), propriétaire terrienne charentaise soupçonnée d'avoir empoisonné à l'arsenic douze membres de son entourage entre 1929 et 1949. Surnommée «~la bonne dame de Loudun~», elle fut finalement acquittée en 1961 après trois procès très médiatisés. \textit{Source :} \textup{fr.wikipedia.org/wiki/Marie\_Besnard}}, la Chisako Kakehi\nf{Chisako Kakehi (née en 1946), femme japonaise condamnée à mort en 2017 pour avoir empoisonné au cyanure plusieurs compagnons et maris afin d'en percevoir les assurances-vie. Surnommée la «~veuve noire de Kyoto~». \textit{Source :} \textup{en.wikipedia.org/wiki/Chisako\_Kakehi}} du sixième"
    ),

    # 10. Marquis de Sade / Cent Vingt Journées
    (
        "Le Marquis de Sade, dans ses Cent Vingt Journées de Sodome ou l'École du Libertinage",
        r"Le Marquis de Sade\nf{Donatien Alphonse François, marquis de Sade (1740--1814), écrivain et philosophe français dont l'œuvre sulfureuse, longtemps censurée, explore les limites de la liberté individuelle à travers la violence et le libertinage. Son nom a donné le mot «~sadisme~». \textit{Source :} \textup{fr.wikipedia.org/wiki/Marquis\_de\_Sade}}, dans ses \textit{Cent Vingt Journées de Sodome ou l'École du Libertinage}\nf{\textit{Les Cent Vingt Journées de Sodome} (rédigé en 1785, publié en 1904), œuvre extrême de Sade rédigée sur un rouleau de parchemin de douze mètres à la Bastille. Catalogue systématique de perversions sexuelles, elle fut classée «~trésor national~» par la France en 2017 pour empêcher sa vente à l'étranger. \textit{Source :} \textup{fr.wikipedia.org/wiki/Les\_Cent\_Vingt\_Journ\%C3\%A9es\_de\_Sodome}}"
    ),

    # 11. Ernest Blum / Raoul Toché / Radiguet
    (
        "à ne pas confondre avec l'opéra bouffe d'Ernest Blum et Raoul Toché ou le chef-d'œuvre de Radiguet",
        r"à ne pas confondre avec l'opéra bouffe d'Ernest Blum\nf{Ernest Blum (1836--1907), auteur dramatique et librettiste français prolifique, connu pour ses vaudevilles et ses livrets d'opérettes. Il collabora notamment avec Raoul Toché sur plusieurs œuvres comiques. \textit{Source :} \textup{fr.wikipedia.org/wiki/Ernest\_Blum\_(auteur)}} et Raoul Toché\nf{Raoul Toché (1850--1895), journaliste, caricaturiste et auteur dramatique français, collaborateur régulier de Blum pour des vaudevilles et livrets d'opérettes de la Belle Époque. \textit{Source :} \textup{fr.wikipedia.org/wiki/Raoul\_Toch\%C3\%A9}} ou le chef-d'œuvre de Radiguet\nf{Raymond Radiguet (1903--1923), écrivain français mort à vingt ans, auteur de \textit{Le Diable au corps} (1923), roman d'un adolescent amoureux de la femme d'un soldat, considéré comme un chef-d'œuvre de la littérature française du XXe siècle. \textit{Source :} \textup{fr.wikipedia.org/wiki/Raymond\_Radiguet}}"
    ),

    # 12. Andréa de Nerciat
    (
        "Le Diable au corps du chevalier Andréa de Nerciat (aka «\u00a0docteur Cazzoné\u00a0»)",
        r"\textit{Le Diable au corps} du chevalier Andréa de Nerciat\nf{André-Robert Andréa de Nerciat (1739--1800), officier, musicien et romancier libertin français, également agent des services secrets. Son roman \textit{Le Diable au corps} (publié posthume en 1803) est considéré comme un chef-d'œuvre de la littérature érotique du XVIIIe siècle. \textit{Source :} \textup{fr.wikipedia.org/wiki/Andr\%C3\%A9a\_de\_Nerciat}} (aka «\u00a0docteur Cazzoné\u00a0»)"
    ),

    # 13. Marquise Henriette de Mannoury d'Ectot
    (
        "le Roman de Violette de la marquise Henriette de Mannoury d'Ectot (alias la Vicomtesse de Cœur Brûlant)",
        r"le \textit{Roman de Violette} de la marquise Henriette de Mannoury d'Ectot\nf{Henriette de Mannoury d'Ectot (1836--1885), femme de lettres française ayant publié sous divers pseudonymes dont «~la Vicomtesse de Cœur Brûlant~» plusieurs romans érotiques aujourd'hui devenus rarissimes. \textit{Source :} \textup{fr.wikipedia.org/wiki/Henriette\_de\_Mannoury\_d'Ectot}} (alias la Vicomtesse de Cœur Brûlant)"
    ),

    # 14. William Gull / Jack l'Éventreur / From Hell / frères Hughes / Stephen Knight
    (
        "mallette de chirurgien de sir William Gull, proche de la reine Victoria un temps suspecté d'être Jack l'Éventreur (voir From Hell des frères Hughes, inspiré des écrits de Stephen Knight, obscur complot mêlant franc-maçonnerie et famille royale d'Angleterre sur fond de misère sociale et prostitution)",
        r"mallette de chirurgien de sir William Gull\nf{Sir William Withey Gull (1816--1890), médecin personnel de la reine Victoria, pionnier de la description clinique de l'anorexie mentale. Certains théoriciens du complot l'ont désigné comme Jack l'Éventreur, sans aucune preuve convaincante. \textit{Source :} \textup{fr.wikipedia.org/wiki/William\_Withey\_Gull}}, proche de la reine Victoria un temps suspecté d'être Jack l'Éventreur (voir \textit{From Hell}\nf{\textit{From Hell} (2001), film des frères Albert et Allen Hughes adapté de la bande dessinée éponyme d'Alan Moore et Eddie Campbell (1989--1996). Le film développe la théorie conspirationniste de Stephen Knight impliquant la franc-maçonnerie et la famille royale dans les meurtres de Whitechapel (1888). \textit{Source :} \textup{fr.wikipedia.org/wiki/From\_Hell\_(film)}} des frères Hughes, inspiré des écrits de Stephen Knight\nf{Stephen Knight (1951--1985), journaliste britannique, auteur de \textit{Jack the Ripper: The Final Solution} (1976), dans lequel il développe une théorie conspirationniste liant les meurtres de Whitechapel à la franc-maçonnerie royale. \textit{Source :} \textup{en.wikipedia.org/wiki/Stephen\_Knight\_(author)}}, obscur complot mêlant franc-maçonnerie et famille royale d'Angleterre sur fond de misère sociale et prostitution)"
    ),

    # 15. Unité 731 / Zagorsk-6
    (
        "du genre Unité 731 (quand les Japs violaient des femmes à la chaîne et se livraient à des expériences horribles sur des êtres humains pour développer des armes bactériologiques) ou Zagorsk-6 (même chose pour les Russes, mais avec des babouins",
        r"du genre Unité 731\nf{L'Unité 731 était une unité secrète de l'armée impériale japonaise stationnée en Mandchourie (1937--1945). Elle mena des expériences biologiques et médicales mortelles sur des milliers de prisonniers de guerre pour développer des armes bactériologiques, faisant des dizaines de milliers de victimes. \textit{Source :} \textup{fr.wikipedia.org/wiki/Unit\%C3\%A9\_731}} (quand les Japs violaient des femmes à la chaîne et se livraient à des expériences horribles sur des êtres humains pour développer des armes bactériologiques) ou Zagorsk-6\nf{Zagorsk-6 (aujourd'hui Sergiev Possad-6), ville fermée soviétique abritant l'Institut de virologie militaire Zagorsk, l'une des principales installations secrètes du programme soviétique d'armes biologiques (\textit{Biopreparat}) pendant la Guerre froide. \textit{Source :} \textup{en.wikipedia.org/wiki/Sergiev\_Posad-6}} (même chose pour les Russes, mais avec des babouins"
    ),

    # 16. Lucien de Samosate / Fougeret de Monbron
    (
        "les Dialogues des courtisanes de Lucien de Samosate et Margot la ravaudeuse de Fougeret de Monbron",
        r"les \textit{Dialogues des courtisanes} de Lucien de Samosate\nf{Lucien de Samosate (vers 120--180 apr. J.-C.), écrivain satirique grec d'origine syrienne. Ses \textit{Dialogues des courtisanes} sont de brèves scènes mettant en scène les mœurs du monde de la prostitution dans l'Antiquité grecque. \textit{Source :} \textup{fr.wikipedia.org/wiki/Lucien\_de\_Samosate}} et \textit{Margot la ravaudeuse} de Fougeret de Monbron\nf{Louis-Charles Fougeret de Monbron (vers 1706--1760), écrivain libertin français. \textit{Margot la ravaudeuse} (1750) est un roman picaresque et érotique retraçant le parcours d'une prostituée parisienne, l'un des textes les plus représentatifs du libertinage littéraire du XVIIIe siècle. \textit{Source :} \textup{fr.wikipedia.org/wiki/Fougeret\_de\_Monbron}}"
    ),

    # 17. Théophile Gautier / Apollonie Sabatier / L'Origine du monde / Courbet
    (
        "une très rare édition originale de la Lettre à la Présidente de Théophile Gautier, une tenancière de bordel connue sous le nom d'Apollonie Sabatier qui a beaucoup inspiré Baudelaire et dont on dit qu'elle aurait servi de modèle à L'Origine du monde, le fameux tableau de Courbet",
        r"une très rare édition originale de la \textit{Lettre à la Présidente} de Théophile Gautier\nf{Théophile Gautier (1811--1872), poète, romancier et critique d'art français, théoricien de l'«~art pour l'art~» et chef de file du Parnasse. La \textit{Lettre à la Présidente} est un poème érotique clandestin adressé à Apollonie Sabatier, tiré à une cinquantaine d'exemplaires vers 1850. \textit{Source :} \textup{fr.wikipedia.org/wiki/Th\%C3\%A9ophile\_Gautier}}, une tenancière de bordel connue sous le nom d'Apollonie Sabatier\nf{Apollonie Sabatier (1822--1890), demi-mondaine et muse parisienne surnommée «~la Présidente~». Baudelaire lui dédia plusieurs poèmes des \textit{Fleurs du Mal}. Elle aurait servi de modèle à \textit{L'Origine du monde} de Courbet (1866), commandée par le diplomate ottoman Khalil Bey. \textit{Source :} \textup{fr.wikipedia.org/wiki/Apollonie\_Sabatier}} qui a beaucoup inspiré Baudelaire et dont on dit qu'elle aurait servi de modèle à \textit{L'Origine du monde}\nf{\textit{L'Origine du monde} (1866), peinture réaliste de Gustave Courbet (1819--1877) représentant le sexe féminin en gros plan. Longtemps dissimulée dans des collections privées, elle appartient aujourd'hui au musée d'Orsay, qui l'acquit en 1995. \textit{Source :} \textup{fr.wikipedia.org/wiki/L'Origine\_du\_monde}}, le fameux tableau de Courbet"
    ),

    # 18. Descartes / Passions de l'âme
    (
        "mon édition originale des Passions de l'âme de Descartes, datée de 1649, soit un an avant la mort de l'auteur à Stockholm",
        r"mon édition originale des \textit{Passions de l'âme} de Descartes\nf{René Descartes (1596--1650), philosophe, mathématicien et physicien français, fondateur du rationalisme moderne. \textit{Les Passions de l'âme} (1649) est son dernier ouvrage, une étude de la relation entre l'âme et le corps. Descartes mourut à Stockholm l'année suivante, où il avait été invité par la reine Christine de Suède. \textit{Source :} \textup{fr.wikipedia.org/wiki/Les\_Passions\_de\_l\%27\%C3\%A2me}}, datée de 1649, soit un an avant la mort de l'auteur à Stockholm"
    ),

    # 19. Paul Meurisse
    (
        "le sosie exact du grand acteur français Paul Meurisse, jusqu'au timbre de la voix, particulièrement savoureux",
        r"le sosie exact du grand acteur français Paul Meurisse\nf{Paul Meurisse (1912--1979), acteur français au style sec et élégant, révélé par Édith Piaf. Célèbre pour \textit{Les Diaboliques} (Clouzot, 1955) et \textit{L'Armée des ombres} (Melville, 1969). Il interpréta l'inspecteur Lamberton, dit «~le Monocle~», dans la série télévisée éponyme (1961--1964). \textit{Source :} \textup{fr.wikipedia.org/wiki/Paul\_Meurisse}}, jusqu'au timbre de la voix, particulièrement savoureux"
    ),

    # 20. L'Armée des ombres / Melville
    (
        "Si, je l'ai vu dans L'Armée des ombres, de Melville.",
        r"Si, je l'ai vu dans \textit{L'Armée des ombres}\nf{\textit{L'Armée des ombres} (1969), film de Jean-Pierre Melville (1917--1973), adapté du roman homonyme de Joseph Kessel (1943). Portrait sobre et implacable de la Résistance française, avec Lino Ventura, Simone Signoret et Paul Meurisse. Longtemps ignoré en France, il est aujourd'hui considéré comme l'un des plus grands films français. \textit{Source :} \textup{fr.wikipedia.org/wiki/L'Arm\%C3\%A9e\_des\_ombres\_(film)}}, de Melville."
    ),

    # 21. Le Cri du cormoran / Michel Audiard / Michel Serrault / Jean Carmet / Bernard Blier
    (
        "Et aussi dans Le Cri du cormoran le soir au-dessus des jonques, de Michel Audiard, avec Michel Serrault, Jean Carmet et Bernard Blier.",
        r"Et aussi dans \textit{Le Cri du cormoran le soir au-dessus des jonques}\nf{\textit{Le Cri du cormoran le soir au-dessus des jonques} (1971), film policier burlesque réalisé par Michel Audiard, avec Paul Meurisse, Michel Serrault, Jean Carmet, Bernard Blier et Gérard Depardieu dans son premier grand rôle au cinéma. \textit{Source :} \textup{fr.wikipedia.org/wiki/Le\_Cri\_du\_cormoran\_le\_soir\_au-dessus\_des\_jonques}}, de Michel Audiard\nf{Michel Audiard (1920--1985), dialoguiste et scénariste français, célèbre pour ses répliques ciselées et son style populaire gouailleur. Il travailla avec les plus grands réalisateurs français (Melville, Lautner, Verneuil) avant de passer à la réalisation. \textit{Source :} \textup{fr.wikipedia.org/wiki/Michel\_Audiard}}, avec Michel Serrault\nf{Michel Serrault (1928--2007), acteur français, l'un des plus populaires de sa génération. Révélé au théâtre et au cinéma comique, il s'imposa aussi dans des rôles dramatiques (\textit{Garde à vue}, 1981 ; \textit{Nelly et Monsieur Arnaud}, 1995). Trois fois César du meilleur acteur. \textit{Source :} \textup{fr.wikipedia.org/wiki/Michel\_Serrault}}, Jean Carmet\nf{Jean Carmet (1920--1994), acteur français spécialiste des seconds rôles savoureux, figure emblématique du cinéma populaire français. Inoubliable dans \textit{Buffet froid} (Bertrand Blier, 1979) et \textit{Violette Nozière} (Chabrol, 1978). \textit{Source :} \textup{fr.wikipedia.org/wiki/Jean\_Carmet}} et Bernard Blier\nf{Bernard Blier (1916--1989), acteur français au physique atypique, figure incontournable du cinéma populaire pendant cinq décennies. Père du réalisateur Bertrand Blier. \textit{Source :} \textup{fr.wikipedia.org/wiki/Bernard\_Blier}}."
    ),

    # 22. Gérard Depardieu (première apparition)
    (
        "C'est aussi la première apparition de Gérard Depardieu dans un long-métrage.",
        r"C'est aussi la première apparition de Gérard Depardieu\nf{Gérard Depardieu (né en 1948), acteur français, l'un des plus prolifiques et des plus internationalement reconnus du cinéma mondial. César et nomination aux Oscars pour \textit{Cyrano de Bergerac} (Jean-Paul Rappeneau, 1990). Il débuta dans des petits rôles au début des années 1970 avant d'exploser avec \textit{Les Valseuses} (Bertrand Blier, 1974). \textit{Source :} \textup{fr.wikipedia.org/wiki/G\%C3\%A9rard\_Depardieu}} dans un long-métrage."
    ),

    # 23. Félix Faure / Marguerite Japy
    (
        "Le président Félix Faure, par exemple, est mort à l'Élysée dans les bras de sa maîtresse, la demi-mondaine Marguerite Japy.",
        r"Le président Félix Faure\nf{Félix Faure (1841--1899), président de la République française de 1895 à sa mort. Il mourut d'une attaque cérébrale le 16 février 1899 à l'Élysée en compagnie de Marguerite Steinheil, née Japy. L'événement suscita de nombreux bons mots, dont le célèbre mot de Clemenceau : «~En entrant dans le néant, il a dû se sentir chez lui.~» \textit{Source :} \textup{fr.wikipedia.org/wiki/F\%C3\%A9lix\_Faure}}, par exemple, est mort à l'Élysée dans les bras de sa maîtresse, la demi-mondaine Marguerite Japy\nf{Marguerite Steinheil, née Japy (1869--1954), demi-mondaine française. Présente lors de l'agonie du président Félix Faure à l'Élysée (1899). Accusée quelques années plus tard du meurtre de son mari et de sa mère, elle fut acquittée en 1909 après un procès très médiatisé. \textit{Source :} \textup{fr.wikipedia.org/wiki/Marguerite\_Steinheil}}."
    ),

    # 24. Byrrh / Dubonnet / Cap Corse de Mattei
    (
        "C'est un peu comme Byrrh, Dubonnet ou le Cap Corse de Mattei, une mistelle de cépages locaux dans laquelle on fait macérer de l'écorce de quinquina et des plantes en proportions variables.",
        r"C'est un peu comme Byrrh\nf{Byrrh, apéritif à base de vin doux naturel et de quinquina créé en 1866 à Thuir (Pyrénées-Orientales) par les frères Violet. Très populaire en France dans la première moitié du XXe siècle, il reste produit par le groupe Pernod Ricard. \textit{Source :} \textup{fr.wikipedia.org/wiki/Byrrh}}, Dubonnet\nf{Dubonnet, apéritif au vin et au quinquina créé en 1846 par le chimiste Joseph Dubonnet, à la demande de la Légion étrangère pour rendre la quinine antimalarique plus agréable à consommer. Il fut notamment la boisson de prédilection de la reine Élisabeth II. \textit{Source :} \textup{fr.wikipedia.org/wiki/Dubonnet}} ou le Cap Corse de Mattei\nf{Le Cap Corse Mattei, quinquina corse créé en 1872 par Louis-Napoléon Mattei à Bastia, à base de muscat et d'écorces de quinquina. Emblème de la Corse, il est protégé par une appellation géographique. \textit{Source :} \textup{fr.wikipedia.org/wiki/Mattei\_(ap\%C3\%A9ritif)}}, une mistelle de cépages locaux dans laquelle on fait macérer de l'écorce de quinquina et des plantes en proportions variables."
    ),

    # 25. Les Pleins Pouvoirs / Clint Eastwood
    (
        "Vous avez vu Les Pleins Pouvoirs, de et avec Clint Eastwood ?",
        r"Vous avez vu \textit{Les Pleins Pouvoirs}\nf{\textit{Les Pleins Pouvoirs} (titre orig. : \textit{Absolute Power}, 1997), film policier réalisé et interprété par Clint Eastwood, d'après le roman de David Baldacci. Un cambrioleur témoin d'un crime commis par le président des États-Unis. \textit{Source :} \textup{fr.wikipedia.org/wiki/Les\_Pleins\_Pouvoirs}}, de et avec Clint Eastwood\nf{Clint Eastwood (né en 1930), acteur et réalisateur américain. Révélé par le western spaghetti (\textit{Le Bon, la Brute et le Truand}, Leone, 1966), il est devenu l'un des cinéastes les plus respectés d'Hollywood, oscarisé pour \textit{Impitoyable} (1992) et \textit{Million Dollar Baby} (2004). \textit{Source :} \textup{fr.wikipedia.org/wiki/Clint\_Eastwood}} ?"
    ),

]

count08 = 0
for old, new in subs08:
    if old in c08:
        c08 = c08.replace(old, new, 1)
        count08 += 1
        print(f'08 ✓  {old[:65]}')
    else:
        print(f'08 ✗  NOT FOUND: {old[:65]}')

with open('/Users/christophe.thiebaud/_Mugnier/actes/acte_08.tex', 'w', encoding='utf-8') as f:
    f.write(c08)
print(f'\nacte_08.tex : {count08} substitutions appliquées\n')
print(f'TOTAL : {count07 + count08} annotations')
