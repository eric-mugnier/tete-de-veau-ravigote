#!/usr/bin/env python3
# -*- coding: utf-8 -*-

with open('/Users/christophe.thiebaud/_Mugnier/actes/acte_08.tex', 'r', encoding='utf-8') as f:
    content = f.read()

substitutions = [
    # 1. Forest Whitaker / Ghost Dog
    (
        "Forest Whitaker dans Ghost Dog",
        r"Forest Whitaker\nf{Forest Whitaker (né en 1961), acteur américain oscarisé pour \textit{Le Dernier Roi d'Écosse} (2006). Il incarne le personnage principal de \textit{Ghost Dog, la voie du samouraï} (Jim Jarmusch, 1999), tueur à gages solitaire s'inspirant du code bushido. \textit{Source :} \textup{fr.wikipedia.org/wiki/Forest\_Whitaker}} dans \textit{Ghost Dog}\nf{\textit{Ghost Dog, la voie du samouraï} (1999), film américain réalisé par Jim Jarmusch, avec Forest Whitaker. Le film s'inspire du \textit{Hagakure}, traité japonais du XVIIIe siècle sur le code du samouraï. \textit{Source :} \textup{fr.wikipedia.org/wiki/Ghost\_Dog,\_la\_voie\_du\_samoura\%C3\%AF}}"
    ),
    # 2. Corey "Raekwon" Woods
    (
        "Corey «\u00a0Raekwon\u00a0» Woods",
        r"Corey «\u00a0Raekwon\u00a0» Woods\nf{Corey Woods, dit Raekwon (né en 1970), rappeur américain membre du Wu-Tang Clan. Son album solo \textit{Only Built 4 Cuban Linx\ldots} (1995) est considéré comme l'un des chefs-d'œuvre du rap new-yorkais des années 1990. \textit{Source :} \textup{fr.wikipedia.org/wiki/Raekwon}}"
    ),
    # 3. 36e Chambre de Shaolin
    (
        "San Te affrontant le général Sien Ta dans la 36e Chambre de Shaolin",
        r"San Te affrontant le général Sien Ta dans \textit{La 36\up{e} Chambre de Shaolin}\nf{\textit{La 36\up{e} Chambre de Shaolin} (1978), film de kung-fu hongkongais réalisé par Lau Kar-leung et produit par la Shaw Brothers, avec Gordon Liu dans le rôle de San Te. Considéré comme l'un des films d'arts martiaux les plus influents de l'histoire du cinéma. \textit{Source :} \textup{fr.wikipedia.org/wiki/La\_36\%C3\%A8me\_Chambre\_de\_Shaolin}}"
    ),
    # 4. GBU-57 / Lockheed Martin / Boeing / Northrop Grumman
    (
        "bombe anti-bunker GBU-57 de l'US Air Force, fascinant concentré de technologie développé par Lockheed Martin, Boeing et la Northrop Grumman Corporation",
        r"bombe anti-bunker GBU-57\nf{La GBU-57 Massive Ordnance Penetrator (MOP) est la bombe conventionnelle la plus puissante de l'arsenal américain, pesant environ 13\,600 kg et capable de pénétrer plus de 60 mètres de béton armé. Développée par Boeing en collaboration avec le Pentagone, elle est conçue pour détruire des installations militaires souterraines fortifiées. \textit{Source :} \textup{en.wikipedia.org/wiki/GBU-57\_MOP}} de l'US Air Force, fascinant concentré de technologie développé par \textit{Lockheed Martin}\nf{Lockheed Martin Corporation, entreprise américaine de défense et d'aérospatiale fondée en 1995 par la fusion de Lockheed Corporation et Martin Marietta. Premier contractant de défense mondial, elle est notamment le fabricant du chasseur F-35. \textit{Source :} \textup{fr.wikipedia.org/wiki/Lockheed\_Martin}}, Boeing et la \textit{Northrop Grumman Corporation}\nf{Northrop Grumman Corporation, entreprise américaine de défense et d'aérospatiale fondée en 1994. Quatrième contractant mondial de défense, elle fabrique notamment le bombardier furtif B-2 Spirit. \textit{Source :} \textup{fr.wikipedia.org/wiki/Northrop\_Grumman}}"
    ),
    # 5. Lovecraft / Sheridan Le Fanu / Montague Rhodes James
    (
        "d'un Lovecraft, un Sheridan Le Fanu ou un Montague Rhodes James pour n'en citer que quelques-uns",
        r"d'un Lovecraft\nf{Howard Phillips Lovecraft (1890--1937), écrivain américain de fantastique et d'horreur cosmique, créateur du Mythe de Cthulhu. Son œuvre majeure comprend \textit{L'Appel de Cthulhu} (1928) et \textit{Les Montagnes hallucinées} (1936). \textit{Source :} \textup{fr.wikipedia.org/wiki/H.\_P.\_Lovecraft}}, un Sheridan Le Fanu\nf{Joseph Sheridan Le Fanu (1814--1873), romancier et nouvelliste irlandais, maître du récit gothique et fantastique victorien, auteur de \textit{Carmilla} (1872) et de \textit{L'Oncle Silas} (1864). \textit{Source :} \textup{fr.wikipedia.org/wiki/Sheridan\_Le\_Fanu}} ou un Montague Rhodes James\nf{Montague Rhodes James (1862--1936), médiéviste et écrivain britannique, auteur de nouvelles fantastiques dont les \textit{Ghost Stories of an Antiquary} (1904), considérées comme des modèles du genre. \textit{Source :} \textup{en.wikipedia.org/wiki/M.\_R.\_James}} pour n'en citer que quelques-uns"
    ),
    # 6. Raymond Maufrais / Mato Grosso
    (
        "Raymond Maufrais se frayant un chemin à coups de machette dans la jungle du Mato Grosso",
        r"Raymond Maufrais\nf{Raymond Maufrais (1926--1950 ?), explorateur et aventurier français, disparu dans la jungle de Guyane lors d'une expédition solitaire. Son journal posthume \textit{Aventures en Guyane} (1952) et les recherches ultérieures de son père Edgar Maufrais ont connu un grand retentissement. \textit{Source :} \textup{fr.wikipedia.org/wiki/Raymond\_Maufrais}} se frayant un chemin à coups de machette dans la jungle du Mato Grosso"
    ),
    # 7. Fliess
    (
        "Fliess (je recommande à tous la lecture des «\u00a0relations entre le nez et les organes génitaux féminins présentés selon leur signification biologique\u00a0»",
        r"Fliess\nf{Wilhelm Fliess (1858--1928), médecin oto-rhino-laryngologiste allemand, ami proche de Freud dont il fut l'interlocuteur privilégié pendant une décennie. Son ouvrage \textit{Les Relations entre le nez et les organes génitaux féminins} (1897) exposait des théories biologiques aujourd'hui réfutées. \textit{Source :} \textup{fr.wikipedia.org/wiki/Wilhelm\_Fliess}} (je recommande à tous la lecture des «\u00a0relations entre le nez et les organes génitaux féminins présentés selon leur signification biologique\u00a0»"
    ),
    # 8. Breuer / Bertha Pappenheim / Anna O.
    (
        "Breuer (ses remarquables travaux sur l'hystérie, notamment le cas de la militante féministe et polyglotte Bertha Pappenheim, alias Anna O.)",
        r"Breuer\nf{Josef Breuer (1842--1925), médecin autrichien, pionnier de la psychanalyse et collaborateur de Freud. Leur ouvrage commun \textit{Études sur l'hystérie} (1895) fonda les bases de la psychanalyse à travers plusieurs cas cliniques. \textit{Source :} \textup{fr.wikipedia.org/wiki/Josef\_Breuer}} (ses remarquables travaux sur l'hystérie, notamment le cas de la militante féministe et polyglotte Bertha Pappenheim\nf{Bertha Pappenheim (1859--1936), militante féministe et philanthrope juive allemande, connue sous le pseudonyme d'Anna O. dans les \textit{Études sur l'hystérie} de Breuer et Freud (1895). Guérie, elle devint une figure majeure du mouvement féministe et du travail social en Allemagne. \textit{Source :} \textup{fr.wikipedia.org/wiki/Bertha\_Pappenheim}}, alias Anna O.)"
    ),
    # 9. la Voisin
    (
        "la Voisin, la Giulia Tofana, l'Hélène Jégado, la Marie Besnard, la Chisako Kakehi",
        r"la Voisin\nf{Catherine Deshayes, dite La Voisin (1640--1680), célèbre empoisonneuse française impliquée dans l'Affaire des poisons, scandale judiciaire qui ébranla la cour de Louis XIV. Brûlée en place de Grève le 22 février 1680. \textit{Source :} \textup{fr.wikipedia.org/wiki/La\_Voisin}}, la Giulia Tofana\nf{Giulia Tofana (vers 1620--1659), empoisonneuse sicilienne célèbre pour avoir fabriqué l'Aqua Tofana, poison à base d'arsenic dont on lui attribue jusqu'à six cents victimes. Exécutée à Rome en 1659. \textit{Source :} \textup{fr.wikipedia.org/wiki/Giulia\_Tofana}}, l'Hélène Jégado\nf{Hélène Jégado (1803--1852), servante bretonne considérée comme l'une des plus grandes empoisonneuses de l'histoire de France. On lui attribue jusqu'à trente-six meurtres à l'arsenic. Guillotinée à Rennes le 26 février 1852. \textit{Source :} \textup{fr.wikipedia.org/wiki/H\%C3\%A9l\%C3\%A8ne\_J\%C3\%A9gado}}, la Marie Besnard\nf{Marie Besnard (1896--1980), propriétaire terrienne charentaise soupçonnée d'avoir empoisonné à l'arsenic douze membres de son entourage entre 1929 et 1949. Acquittée faute de preuves en 1961 après trois procès, elle fut surnommée «~la bonne dame de Loudun~». \textit{Source :} \textup{fr.wikipedia.org/wiki/Marie\_Besnard}}, la Chisako Kakehi\nf{Chisako Kakehi (née en 1946), femme japonaise condamnée à mort en 2017 pour avoir empoisonné au cyanure plusieurs compagnons et maris pour s'approprier leurs assurances-vie. Surnommée la «~veuve noire de Kyoto~». \textit{Source :} \textup{en.wikipedia.org/wiki/Chisako\_Kakehi}}"
    ),
    # 10. Marquis de Sade / Cent Vingt Journées
    (
        "Le Marquis de Sade, dans ses Cent Vingt Journées de Sodome ou l'École du Libertinage",
        r"Le Marquis de Sade\nf{Donatien Alphonse François de Sade (1740--1814), écrivain et philosophe français dont l'œuvre, longtemps censurée, explore les thèmes de la violence, de la liberté et du libertinage. Il donna son nom au sadisme. \textit{Source :} \textup{fr.wikipedia.org/wiki/Marquis\_de\_Sade}}, dans ses \textit{Cent Vingt Journées de Sodome ou l'École du Libertinage}\nf{\textit{Les Cent Vingt Journées de Sodome} (rédigé en 1785, publié en 1904) est l'œuvre la plus extrême du marquis de Sade, rédigée sur un rouleau de papier de douze mètres alors qu'il était emprisonné à la Bastille. Elle fut classée en 2017 parmi les «~trésors nationaux~» de France. \textit{Source :} \textup{fr.wikipedia.org/wiki/Les\_Cent\_Vingt\_Journ\%C3\%A9es\_de\_Sodome}}"
    ),
    # 11. Paul Meurisse
    (
        "grand acteur français Paul Meurisse, jusqu'au timbre de la voix",
        r"grand acteur français Paul Meurisse\nf{Paul Meurisse (1912--1979), acteur français au style sec et élégant, célèbre pour ses rôles dans \textit{Les Diaboliques} (Clouzot, 1955) et \textit{L'Armée des ombres} (Melville, 1969). Il interpréta également l'inspecteur Dumont dans la série télévisée \textit{Le Monocle} (1961--1964). \textit{Source :} \textup{fr.wikipedia.org/wiki/Paul\_Meurisse}}, jusqu'au timbre de la voix"
    ),
    # 12. L'Armée des ombres / Melville
    (
        "je l'ai vu dans L'Armée des ombres, de Melville",
        r"je l'ai vu dans \textit{L'Armée des ombres}\nf{\textit{L'Armée des ombres} (1969), film français de Jean-Pierre Melville (1917--1973), adapté du roman de Joseph Kessel (1943). Portrait de la Résistance française, avec Lino Ventura, Simone Signoret et Paul Meurisse. Considéré comme l'un des plus grands films français. \textit{Source :} \textup{fr.wikipedia.org/wiki/L'Arm\%C3\%A9e\_des\_ombres\_(film)}}, de Melville"
    ),
    # 13. Le Cri du cormoran / Michel Audiard
    (
        "Le Cri du cormoran le soir au-dessus des jonques, de Michel Audiard, avec Michel Serrault, Jean Carmet et Bernard Blier",
        r"\textit{Le Cri du cormoran le soir au-dessus des jonques}\nf{\textit{Le Cri du cormoran le soir au-dessus des jonques} (1971), film policier français réalisé et dialogué par Michel Audiard (1920--1985), avec Paul Meurisse, Michel Serrault, Jean Carmet, Bernard Blier et Gérard Depardieu dans l'un de ses premiers rôles au cinéma. \textit{Source :} \textup{fr.wikipedia.org/wiki/Le\_Cri\_du\_cormoran\_le\_soir\_au-dessus\_des\_jonques}}, de Michel Audiard\nf{Michel Audiard (1920--1985), scénariste et dialoguiste français, célèbre pour ses répliques ciselées et son style populaire impertinent. Il réalisa une dizaine de films, dont \textit{Le Cri du cormoran\ldots} (1971). \textit{Source :} \textup{fr.wikipedia.org/wiki/Michel\_Audiard}}, avec Michel Serrault\nf{Michel Serrault (1928--2007), acteur français polyvalent, célèbre pour \textit{La Cage aux folles} (1978) et \textit{Garde à vue} (1981). César du meilleur acteur à trois reprises. \textit{Source :} \textup{fr.wikipedia.org/wiki/Michel\_Serrault}}, Jean Carmet\nf{Jean Carmet (1920--1994), acteur français spécialiste des seconds rôles pittoresques, inoubliable dans \textit{Buffet froid} (Blier, 1979) et \textit{Dupont Lajoie} (Boisset, 1975). César du meilleur second rôle en 1983. \textit{Source :} \textup{fr.wikipedia.org/wiki/Jean\_Carmet}} et Bernard Blier\nf{Bernard Blier (1916--1989), acteur français au physique atypique, figure incontournable du cinéma populaire français des années 1950 aux années 1980. Père du réalisateur Bertrand Blier. \textit{Source :} \textup{fr.wikipedia.org/wiki/Bernard\_Blier}}"
    ),
    # 14. Gérard Depardieu
    (
        "C'est aussi la première apparition de Gérard Depardieu dans un long-métrage.",
        r"C'est aussi la première apparition de Gérard Depardieu\nf{Gérard Depardieu (né en 1948), acteur français le plus internationalement reconnu de sa génération, César du meilleur acteur pour \textit{Le Dernier Métro} (1981). Sa carrière compte plus de deux cents films, dont \textit{Cyrano de Bergerac} (1990), pour lequel il fut nommé aux Oscars. \textit{Source :} \textup{fr.wikipedia.org/wiki/G\%C3\%A9rard\_Depardieu}} dans un long-métrage."
    ),
    # 15. Andréa de Nerciat
    (
        "Le Diable au corps du chevalier Andréa de Nerciat (aka «\u00a0docteur Cazzoné\u00a0»)",
        r"\textit{Le Diable au corps} du chevalier Andréa de Nerciat\nf{André-Robert Andréa de Nerciat (1739--1800), officier, musicien et romancier libertin français, également agent secret. Son roman \textit{Le Diable au corps} (1803, posthume) est considéré comme un chef-d'œuvre de la littérature érotique du XVIIIe siècle. \textit{Source :} \textup{fr.wikipedia.org/wiki/Andr\%C3\%A9a\_de\_Nerciat}} (aka «\u00a0docteur Cazzoné\u00a0»)"
    ),
    # 16. Marquise Henriette de Mannoury d'Ectot
    (
        "Roman de Violette de la marquise Henriette de Mannoury d'Ectot (alias la Vicomtesse de Cœur Brûlant)",
        r"\textit{Roman de Violette} de la marquise Henriette de Mannoury d'Ectot\nf{Henriette de Mannoury d'Ectot (1836--1885), femme de lettres française ayant publié sous divers pseudonymes, dont «~la Vicomtesse de Cœur Brûlant~», plusieurs romans érotiques de la fin du XIXe siècle aujourd'hui devenus rarissimes. \textit{Source :} \textup{fr.wikipedia.org/wiki/Henriette\_de\_Mannoury\_d'Ectot}} (alias la Vicomtesse de Cœur Brûlant)"
    ),
    # 17. Théophile Gautier / Apollonie Sabatier / L'Origine du monde / Courbet
    (
        "une très rare édition originale de la Lettre à la Présidente de Théophile Gautier, une tenancière de bordel connue sous le nom d'Apollonie Sabatier qui a beaucoup inspiré Baudelaire et dont on dit qu'elle aurait servi de modèle à L'Origine du monde, le fameux tableau de Courbet",
        r"une très rare édition originale de la \textit{Lettre à la Présidente} de Théophile Gautier\nf{Théophile Gautier (1811--1872), poète, romancier et critique d'art français, chef de file du mouvement parnassien et de l'art pour l'art. Sa \textit{Lettre à la Présidente} (vers 1850), poème érotique licencieux adressé à Apollonie Sabatier, ne fut tirée qu'à une cinquantaine d'exemplaires. \textit{Source :} \textup{fr.wikipedia.org/wiki/Th\%C3\%A9ophile\_Gautier}}, une tenancière de bordel connue sous le nom d'Apollonie Sabatier\nf{Apollonie Sabatier (1822--1890), demi-mondaine et muse parisienne, surnommée «~la Présidente~». Elle inspira Baudelaire (le cycle des «~poèmes à la Présidente~» dans \textit{Les Fleurs du Mal}) et aurait servi de modèle à \textit{L'Origine du monde} de Gustave Courbet (1866). \textit{Source :} \textup{fr.wikipedia.org/wiki/Apollonie\_Sabatier}} qui a beaucoup inspiré Baudelaire et dont on dit qu'elle aurait servi de modèle à \textit{L'Origine du monde}\nf{\textit{L'Origine du monde} (1866), tableau de Gustave Courbet (1819--1877) représentant le sexe féminin de façon frontale et réaliste. Commandé par le diplomate ottoman Khalil Bey, il appartient aujourd'hui au musée d'Orsay à Paris. \textit{Source :} \textup{fr.wikipedia.org/wiki/L'Origine\_du\_monde}}, le fameux tableau de Courbet"
    ),
    # 18. Descartes / Passions de l'âme
    (
        "les Passions de l'âme de Descartes, datée de 1649, soit un an avant la mort de l'auteur à Stockholm",
        r"les \textit{Passions de l'âme} de Descartes\nf{René Descartes (1596--1650), philosophe, mathématicien et physicien français, père du rationalisme moderne. \textit{Les Passions de l'âme} (1649) est son dernier ouvrage majeur, dédié à la princesse Élisabeth de Bohême, et traite de la relation entre l'âme et le corps. Descartes mourut à Stockholm l'année suivante. \textit{Source :} \textup{fr.wikipedia.org/wiki/Les\_Passions\_de\_l'âme}}, datée de 1649, soit un an avant la mort de l'auteur à Stockholm"
    ),
    # 19. Félix Faure / Marguerite Japy
    (
        "Le président Félix Faure, par exemple, est mort à l'Élysée dans les bras de sa maîtresse, la demi-mondaine Marguerite Japy.",
        r"Le président Félix Faure\nf{Félix Faure (1841--1899), président de la République française de 1895 à sa mort. Il mourut d'une attaque cérébrale le 16 février 1899 à l'Élysée en compagnie de sa maîtresse Marguerite Steinheil, née Japy. L'événement alimenta de nombreux bons mots, dont le mot de Clemenceau : «~En entrant dans le néant, il a dû se sentir chez lui.~» \textit{Source :} \textup{fr.wikipedia.org/wiki/F\%C3\%A9lix\_Faure}}, par exemple, est mort à l'Élysée dans les bras de sa maîtresse, la demi-mondaine Marguerite Japy\nf{Marguerite Steinheil, née Japy (1869--1954), demi-mondaine française, maîtresse du président Félix Faure dont elle fut présente lors de l'agonie à l'Élysée en 1899. Plus tard accusée du meurtre de son mari et de sa mère, elle fut acquittée en 1909. \textit{Source :} \textup{fr.wikipedia.org/wiki/Marguerite\_Steinheil}}."
    ),
    # 20. William Gull / Jack l'Éventreur / From Hell / frères Hughes / Stephen Knight
    (
        "mallette de chirurgien de sir William Gull, proche de la reine Victoria un temps suspecté d'être Jack l'Éventreur (voir From Hell des frères Hughes, inspiré des écrits de Stephen Knight, obscur complot mêlant franc-maçonnerie et famille royale d'Angleterre sur fond de misère sociale et prostitution)",
        r"mallette de chirurgien de sir William Gull\nf{Sir William Withey Gull (1816--1890), médecin personnel de la reine Victoria, soignant notamment le prince de Galles. Sa compétence chirurgicale et ses contacts royaux ont conduit certains à le suspecter, sans preuve convaincante, d'être Jack l'Éventreur. \textit{Source :} \textup{fr.wikipedia.org/wiki/William\_Withey\_Gull}}, proche de la reine Victoria un temps suspecté d'être Jack l'Éventreur (voir \textit{From Hell}\nf{\textit{From Hell} (2001), film des frères Albert et Allen Hughes, adapté de la bande dessinée éponyme d'Alan Moore et Eddie Campbell (1989--1996). Le film reprend la théorie conspirationniste de Stephen Knight impliquant la franc-maçonnerie et la famille royale dans les meurtres de Whitechapel. \textit{Source :} \textup{fr.wikipedia.org/wiki/From\_Hell\_(film)}} des frères Hughes, inspiré des écrits de Stephen Knight\nf{Stephen Knight (1951--1985), journaliste britannique auteur de \textit{Jack the Ripper: The Final Solution} (1976), ouvrage dans lequel il développa la théorie conspirationniste liant les meurtres de Whitechapel à la franc-maçonnerie et à la famille royale. \textit{Source :} \textup{en.wikipedia.org/wiki/Stephen\_Knight\_(author)}}, obscur complot mêlant franc-maçonnerie et famille royale d'Angleterre sur fond de misère sociale et prostitution)"
    ),
    # 21. Unité 731
    (
        "du genre Unité 731 (quand les Japs violaient des femmes à la chaîne et se livraient à des expériences horribles sur des êtres humains pour développer des armes bactériologiques)",
        r"du genre Unité 731\nf{L'Unité 731 était une unité secrète de l'armée impériale japonaise stationnée en Mandchourie (1937--1945), responsable d'expériences biologiques et médicales mortelles sur des prisonniers de guerre et des civils. Ses travaux sur les armes bactériologiques firent des dizaines de milliers de victimes. \textit{Source :} \textup{fr.wikipedia.org/wiki/Unit\%C3\%A9\_731}} (quand les Japs violaient des femmes à la chaîne et se livraient à des expériences horribles sur des êtres humains pour développer des armes bactériologiques)"
    ),
    # 22. Zagorsk-6
    (
        "ou Zagorsk-6 (même chose pour les Russes, mais avec des babouins",
        r"ou Zagorsk-6\nf{Zagorsk-6 (aujourd'hui Serguiev Possad-6), ville fermée soviétique abritant le Centre de virologie et de biotechnologie Vektor ainsi qu'un laboratoire militaire de recherche sur les agents biologiques. L'une des principales installations soviétiques de développement d'armes bactériologiques pendant la Guerre froide. \textit{Source :} \textup{en.wikipedia.org/wiki/Zagorsk}} (même chose pour les Russes, mais avec des babouins"
    ),
    # 23. Lucien de Samosate
    (
        "les Dialogues des courtisanes de Lucien de Samosate",
        r"les \textit{Dialogues des courtisanes} de Lucien de Samosate\nf{Lucien de Samosate (vers 120 -- vers 180 apr. J.-C.), écrivain satirique grec d'origine syrienne, auteur des \textit{Dialogues des courtisanes}, brèves scènes de mœurs mettant en scène le monde de la prostitution dans l'Antiquité grecque. \textit{Source :} \textup{fr.wikipedia.org/wiki/Lucien\_de\_Samosate}}"
    ),
    # 24. Fougeret de Monbron
    (
        "Margot la ravaudeuse de Fougeret de Monbron",
        r"\textit{Margot la ravaudeuse} de Fougeret de Monbron\nf{Louis-Charles Fougeret de Monbron (vers 1706--1760), écrivain libertin français, auteur du roman picaresque \textit{Margot la ravaudeuse} (1750), chronique des mœurs du demi-monde parisien du XVIIIe siècle. \textit{Source :} \textup{fr.wikipedia.org/wiki/Fougeret\_de\_Monbron}}"
    ),
    # 25. Les Pleins Pouvoirs de Clint Eastwood
    (
        "Vous avez vu Les Pleins Pouvoirs, de et avec Clint Eastwood ?",
        r"Vous avez vu \textit{Les Pleins Pouvoirs}\nf{\textit{Les Pleins Pouvoirs} (titre original : \textit{Absolute Power}, 1997), film policier réalisé et interprété par Clint Eastwood. Le héros y incarne un cambrioleur qui vole par amour de l'art, assistant à un crime commis par le président des États-Unis. \textit{Source :} \textup{fr.wikipedia.org/wiki/Les\_Pleins\_Pouvoirs}}, de et avec Clint Eastwood\nf{Clint Eastwood (né en 1930), acteur et réalisateur américain, figure emblématique du western spaghetti (\textit{Le Bon, la Brute et le Truand}, 1966) devenu l'un des cinéastes les plus respectés d'Hollywood (\textit{Million Dollar Baby}, 2004 ; \textit{Gran Torino}, 2008). \textit{Source :} \textup{fr.wikipedia.org/wiki/Clint\_Eastwood}} ?"
    ),
    # 26. Bisset / Byrrh / Dubonnet / Cap Corse de Mattei
    (
        "C'est un peu comme Byrrh, Dubonnet ou le Cap Corse de Mattei, une mistelle de cépages locaux dans laquelle on fait macérer de l'écorce de quinquina et des plantes en proportions variables.",
        r"C'est un peu comme Byrrh\nf{Byrrh, apéritif à base de vin doux et de quinquina créé en 1866 à Thuir (Pyrénées-Orientales) par les frères Violet. Très populaire en France au début du XXe siècle, il reste produit par la maison Pernod Ricard. \textit{Source :} \textup{fr.wikipedia.org/wiki/Byrrh}}, Dubonnet\nf{Dubonnet, apéritif à base de vin doux et de quinquina créé en 1846 par le chimiste Joseph Dubonnet à la demande de la Légion étrangère française. Il fut notamment la boisson de prédilection de la reine Elizabeth II. \textit{Source :} \textup{fr.wikipedia.org/wiki/Dubonnet}} ou le Cap Corse de Mattei\nf{Le Cap Corse Mattei, quinquina corse à base de muscat et d'écorces de quinquina, créé en 1872 par Louis-Napoléon Mattei à Bastia. Véritable emblème de la Corse, il est protégé par une appellation géographique. \textit{Source :} \textup{fr.wikipedia.org/wiki/Mattei\_(apéritif)}}, une mistelle de cépages locaux dans laquelle on fait macérer de l'écorce de quinquina et des plantes en proportions variables."
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

with open('/Users/christophe.thiebaud/_Mugnier/actes/acte_08.tex', 'w', encoding='utf-8') as f:
    f.write(content)
print(f'\nApplied {count} substitutions to acte_08.tex')
