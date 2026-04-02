\version "2.12.3"
#(set-global-staff-size 12)
#(set-default-paper-size "a4" )
\paper {
	between-system-padding = 0.5\mm
	top-margin = 12\mm
	bottom-margin = 12\mm
	left-margin = 12\mm
	right-margin = 12\mm
}
\bookpart{
\header { title="Das Rheingold"}
\score {
\relative c, { \clef bass \key ees \major \time 6/8
ees4.(~ees4  bes'8  ees4.~ees4 g8 bes4.~bes4 ees8 g2 ) }
\header {piece= "Le Rhin"}
}

\score {
\new StaffGroup <<
\new Staff \relative c'' { \clef treble \key ees \major \time 6/8
aes16 (ees16 c16 ees16 aes16 c16 ees4.)
aes,16 (ees16 c16 ees16 aes16 c16 ees4.)}
\new Staff \relative c'' { \clef treble \key ees \major \time 6/8
r4 r8 ees,16 (c16 aes16 c16 ees aes16 c4.)
ees,16 (c16 aes16 c16 ees aes16 )} >>
\header { piece = "Les filles du Rhin"}
}

\score {
\relative c' {\clef bass \key ees \major \time 6/8
bes4 a8 r4 ges8 d'4 c8 r4 r8 }
\header { piece = "La servitude"}
}

\score{
\relative c {\clef bass \time 3/4 \partial 4
d8. d16 g4. ( d16) d16-. g8-. b8-. d2. }
\header { piece = "L'or"}
}

\score{
\relative c'' {\clef treble \time 9/8 < c e g>8. <g c e>16 <g d' f>8
< c e g >4. <g c e>4 r8 <b f' a>2. <c e g>4 r8 <b f' a>2. <c e g>4 r8}
\header { piece = "Adoration de l'or" }
}

\score{
\relative c'' {\clef treble \time 9/8
\set Staff.autoBeaming = ##f
e4. cis4.~cis8 a8 gis fis gis a b4}
\header { piece = "La puissance de l'anneau" }
}

\score{
\relative c'' {\clef treble \time 4/4
\set Staff.autoBeaming = ##f
r2 g4 g8 g ees'4. d8 c4 r8 g8 aes2 }
\header { piece = "Renoncement à l'amour" }
}

\score{
\relative c' {\clef bass \time 4/4 <c e>4 (<a c>2 <fis a>4 <d fis>
\times 2/3 {<fis a> <g b>8} <a c>2)}
\header { piece = "L'anneau" }
}

\score{
\relative c' {\clef bass \time 3/4 \key des \major
<aes des f aes>4 (<aes des f>4. <f aes des>8 <ges bes>8.<f aes des>16
<f aes des>8 <ees aes c ees>8 <f aes des f>4) }
\header { piece = "Le Walhalla" }
}

\score{
\relative c' {\clef bass \time 3/4 \key des \major
\set Staff.autoBeaming = ##f
des2 des,8.(f'16) f2 des,8. f16 aes2. }
\header { piece = "Salut au Walhalla" }
}

\score{
\relative c' {\clef bass \time 4/4 \partial 2.
bes4 (a8 g f8. e16 d4 c bes a g f e2)}
\header { piece = "Le traité" }
}

\score{
\relative c' {\clef bass \time 4/4 \key d \minor \partial 2
\set Staff.autoBeaming = ##f
d4 (c8. c16 c4 d,8. d16 d'4 c8. c16 bes4 ees,4) r4
ees (e! f c' bes8 aes8) \time 3/4 g4 d8 }
\header { piece = "La fascination de l'amour" }
}

\score{
\relative c'' {\clef treble \time 4/4 \key g \major 
g4 (a8 ais b e fis g c4 b8.) fis16 (a4 g8.) dis16 (fis4 e8.)
b16 (d4 c8.) g16 (<c, e>1) }
\header { piece = "Freïa - La fuite" }
}

\score{
\relative c {\clef bass \time 4/4 \key d \minor 
\grace {\times 2/3 {g16 [a b]}} c8. c16 c4
\grace {\times 2/3 {g16 [a b]}} c8. c16 c4 }
\header { piece = "Les géants" }
}

\score{
\new StaffGroup <<
\new Staff \relative c {\clef bass \time 4/4 \key aes \major
\set Staff.autoBeaming = ##f
ees8. (g16 bes4 ees d c bes8. bes16 aes4 r8 g8 f4 g8 aes c2~c4 bes4)}
\new Staff \relative c, {\clef bass \time 4/4 \key aes \major
r2 ees8. g16 bes4 ees d c bes4 aes g f g8 aes bes4 r4} >>
\header { piece = "Convention avec les géants" }
}

\score{
\relative c {\clef bass \time 4/4 \key d \major 
\set Staff.autoBeaming = ##f
fis4. e8 d4 a8 r8
\times 2/3 {fis8. a16 d8} \acciaccatura fis8 \times 2/3 {e8 (d) e}
fis8.(a16 a8)r8}
\header { piece = "Les pommes d'or" }
}

\score{
\relative c {\clef bass \time 2/4 \key a \major
\partial 4 r16 cis16 (d g | gis! dis e a ais eis fis b | c g gis cis d a ais
dis \clef treble
| e b ais dis e b ais dis) | <b e> (<c f> <cis fis> <d g>
<dis gis> <e a> <f bes> <fis b> | <g c> <gis cis> <a d> <bes ees>
<b e> <c f> <cis fis> <d! g>) | gis!32 (a gis a gis a gis a)
bes (a bes a bes a bes a) | gis!32 (a gis a gis a gis a)
bes (a bes a bes a bes a) }
\header { piece = "Loge" }
}

\score{
\new StaffGroup <<
\new Staff \relative c' {\clef bass \time 2/4 \key a \major
\set Staff.autoBeaming = ##f
ais8 ais16 cis fis,8 r8 fis8 fis16 fis ais8 ais16 fis ais8. fis16 cis'8
gis16 gis16 ais 8 cis r4}
\new Staff \relative c' {\clef treble \time 2/4 \key a \major
<fis fis' cis'>4. <eis g' d'>8-> (<fis fis' cis'>4.)
<dis a' dis'>8-> (<fis fis' cis'>8-.) r8
<cis eis' cis'>8-. r8 <fis fis' cis'>4. r8 }
>>
\header { piece = "Le charme des flammes" }
}

\score{
\relative c' {\clef tenor \time 3/4
\set Staff.autoBeaming = ##f
f2 e4 d2 c8 bes8 a2. }
\header { piece = "Le regret de l'amour" }
}

\score{
\relative c' {\clef treble \time 9/8 \key des \major f8. f16 f8 f8 des8
ees8 f8. f16 f8}
\header { piece = "La forge" }
}

\score{
\relative c' {\clef treble \time 2/4 \key des \major 
<aes ces ees>2~(<aes ces! ees>4 <fes aeses ces fes>)
<aes ces ees>2~(<aes ces! ees>4 <fes aeses ces fes>) }
\header { piece = "Le pouvoir du casque" }
}

\score{
\relative c {\clef bass \time 2/4 \key bes \major 
<f a>2 (<b, dis> <a' c> <dis, fis> <c' ees> <fis, a> 
<ees' g> <c ees>4 <a c>) }
\header { piece = "La réflexion" }
}

\score{
\relative c {\clef bass \time 3/4 \key des \major 
<< {<bes des>2~<bes des>4 <bes des>2~<bes des>4~<bes des>4} \\
{e,2\f\> (fis4)\p e2\f\> (fis4\p g)}>> }
\header { piece = "La puissance d'Alberich" }
}

\score{
\new StaffGroup <<
\new Staff \relative c' { \clef treble \key a \major \time 3/4 
\times 2/3 {fis4.:8}
\times 2/3 {fis4.:8}
\times 2/3 {fis4.:8}
\times 2/3 {fis4.:8}
\times 2/3 {fis4.:8}
\times 2/3 {fis4.:8}
\times 2/3 {fis4.:8}
\times 2/3 {fis4.:8}
\times 2/3 {fis4.:8}
\times 2/3 {fis4.:8}
\times 2/3 {fis4.:8}
\times 2/3 {fis4.:8} }
\new Staff \relative c, { \clef bass \key a \major \time 3/4
fis2 gis4 a2. gis2 a4 b2. } >>
\header { piece = "L'amoncellement du trésor" }
}

\score{
\relative c''' { \clef treble \key a \major \time 3/4 
a16 (d, cis b' a d, cis b' a d, b' cis, a'4)}
\header { piece = "Cri de triomphe du Nibelung" }
}

\score{
\relative c, { \clef bass \key a \major \time 4/4 
dis4\p\< ( e dis\!\> fis8.\!) r16
eis4\p\< ( fis eis\!\> gis8.\!) r16 }
\header { piece = "Le dragon" }
}

\score{
\relative c {\clef bass \key d \major \time 12/8
\partial 8 
\times 4/5 {fis,32 (g a b c} cis!8->) 
<e g>4~ <e g>8 <e g>8 <e g>8 ~<e g>8 <cis e g>4~<cis e g>8 r8 r8}
\header { piece = "Travail de destruction des Nibelungs" }
}

\score{
\relative c {\clef bass \key d \major \time 4/4
\set Staff.autoBeaming = ##f
\partial 4 fis8 fis a2 a4 a8. a16 c2. r8 c8
e2 e,4 e8 c8 g'2}
\header { piece = "Malédiction de l'anneau" }
}

\score{
\relative c {\clef bass \key e \major \time 4/4 
<e, cis'>4. <gis dis'>8 <cis e>4. <dis fis>8 <e gis>4. <gis cis>8 <cis e>2
}
\header { piece = "Les nornes" }
}

\score{
\relative c'' {\clef treble \key e \major \time 4/4 
<a d fis a>4.( <e' gis>8 <d fis>4. <a e'>8 <fis d'>4. <e a>8  <d fis>4. <cis e>8
<a bis eis>2) }
\header { piece = "Le déclin des dieux" }
}

\score{
\relative c {\clef bass \key bes \major \time 4/4
\set Staff.autoBeaming = ##f
\partial 16 f16 bes2. r8. f16 d'8 f,16 bes2 }
\header { piece = "Incantation du tonnerre" }
}

\score{
\relative c {\clef bass \key des \major 
\time 3/4 
ges4 (bes4. des8 ges8. bes16 des4 bes ges des bes8 ces des4 bes ges8 aes )
}
\header { piece = "L'arc en ciel" }
}

\score{
\relative c'' {\clef treble \time 4/4 
\partial 8 g8 c2 c,4.. e16 g4. c8 e2 }
\header { piece = "L'épée" }
}
}

\bookpart{
\header {title = "Die Walküre"}
\score {
\relative c, { \clef bass \key f \major \time 3/2
\times 4/5 { d16 [ e f g a] } bes4 a g-. f-. e-. d-. e-. f-. g-. a-. f-.}
\header {piece= "La tempête"}
}

\score {
\relative c { \clef bass \key f \major \time 3/2
d1~( d4 c bes) a ( g4. f8) f4 (e bes'1) }
\header {piece= "Lassitude de Siegmund"}
}

\score {
\new StaffGroup <<
\new Staff \relative c' { \clef treble \key f \major \time 3/4
r2. | r8 <g bes>8 (<bes e> <e g> <g bes>8. <f a>16 <e g>4)
}
\new Staff \relative c { \clef bass \key f \major \time 3/4
g4. f8 (e) d(~d8. cis16 cis4) cis8 (bes'4) }
>>
\header {piece= "La compassion"}
}

\score {
\relative c'' { \clef tenor \key f \major \time 3/4
bes2.(~bes4 a4. ees8 g2.)~(g4 f4. c8 ees4. e8 f8. ces16 ees4 d8) ees8 (e8.
b16 d4 c8) cis (d8. g,16 bes4. a8 bes8. d16 d2.) }
\header {piece= "L'amour"}
}

\score {
\relative c { \clef bass \key f \major \time 3/4 c2( b8. c16 a'2
f4 d2.)}
\header {piece= "La race des Wælsungs"}
}

\score {
\relative c' { \clef treble \key ees \major \time 4/4 ees4-. ees-. r8.
ees32-. ees-. \times 2/3 {ees8-. c-. aes'-.} f8.-. f16 f4-.}
\header {piece= "Hunding"}
}

\score {
\relative c { \clef bass \key ees \major \time 3/4 c2 d8. d16
ees8. d16 ees4.\( d8 g4~\times 2/3 {g8 [fis g]} bes8. g16 g2(aes4)\)
\clef treble des'2 (g,8 aes c2~c8. c16 ees2 d!4 c-.) r r b-. r
}
\header {piece= "L'héroïsme des Wælsungs"}
}

\score {
\new StaffGroup <<
\new Staff \relative c'' { \set Staff.autoBeaming = ##f
\clef treble \key bes \major \time 9/8 bes4 (f8 f4 bes8 d c d ees4 d8
c4.~c8) r8 c (c4 g8 bes4 a8 bes8 a bes c4.~c4) r8 }
\new Staff \relative c' {
\clef treble \key bes \major \time 9/8 f8 (d) f(d) f(d) f(d)f(ees) f(ees)
f (c)f(c)f(c) ees(c) ees(bes) ees(a,) bes(d) bes(c) f(c)f(c)f}
>>
\header {piece= "Hymne au printemps"}
}

\score {
\relative c' {
\clef treble \time 3/4 r8. b16 gis'-> a8 r8
}
\header {piece= "La volupté"}
}

\score {
\new StaffGroup <<
\new Staff \relative c' {\clef tenor \time 9/8 \partial 4.
r4 g8 | c8.-> g16 c8 e4. c | e8.-> c16 e8 g4. e | g,8.-> e16 g8 b4. b,
e8.-> b16 e8 gis2. }
\new Staff \relative c'' {\clef treble \time 9/8 \partial 4.
e8. c16 g8 
\repeat unfold 2 { e''8. c16 fis,8 a8. g16 c,8 e8. c16 g8 | }
e''8. b16 fis8 a8. g16 b,8 b'8. fis16 dis8 |
gis'8. e16 b8 e8. b16 gis8 b8. gis16 e8 
}
\new RhythmicStaff { \time 9/8 \partial 4.
\set Staff.timeSignatureFraction = #'(3 . 4)
\scaleDurations #'(3 . 2) {
\repeat unfold 7 { c8. [c32 c32] }
c8 r8 c8 r8 r4 c2.\trill
}
}
>>
\header {piece= "La chevauchée"}
}

\score{
\relative c''' {\clef treble \time 9/8 \key d \major
\set Staff.autoBeaming = ##f
g8 (dis8.) g,16 b4.~b4 r8
g'8 (dis8.) g,16 b4.~b8 r8 b16 b16
e!2.~e8 r8 e16 e16
g2.~g8 r8 r8
}
\header { piece = "Cri d'appel des Walkyries" }
}

\score{
\relative c {\clef bass \time 4/4
r2 \grace { \times 2/3 { e16 ([f g]}}
f2) (e4. d8 c4. e16 d c2 b4. c8)
}
\header { piece = "Le courroux de Wotan" }
}

\score{
\relative c, {\clef bass \time 4/4
e8.( [fis16 g8. a16] b8.[ e16 g8. fis16] | e8. g,16)
}
\header { piece = "Détresse des dieux" }
}

\score{
\relative c {\clef bass \time 4/4 \key aes \major
\times 4/6 { a8 ([bes c des ees e]}
\times 4/6 { f [ges ees c b bes]) }
}
\header { piece = "La poursuite" }
}
\score{
\relative c' {\clef bass \time 4/4
\key a \major
<< {a2.(gis4 b1)~b4} \\
{<dis,, e d' eis>1 <cis gis' cis e>1~<cis gis' cis e>4}>>
r4 r2 r1
<< {b''2.(ais4 cis1)~cis4} \\
{<e,, fisis e' fisis>1 <dis ais' dis fisis>1~<dis ais' dis fisis>4}>>
r4 r2 r1
}
\header { piece = "Le sort" }
}

\score{
\relative c' {\clef treble \time 4/4
\key a \major
cis2 (fis4. gis8 a2. gis4 b2. ais4) cis1\fermata
}
\header { piece = "La mort" }
}

\score{
\relative c'' {\clef treble \time 6/8
\key g \major \partial 4.
\set Staff.autoBeaming = ##f
g4 g8 c4.~c4 c8 ees4. d4 c8 aes'2.
c,4. bes4 aes8 ees'4.~ees4 ees8 f4.~f8 c8 d8 ees2.
}
\header { piece = "Siegfried gardien de l'épée" }
}

\score{
\relative c'' {\clef treble \time 6/8
\key g \major \partial 4.
d4. g4.(g8 fis g a4. g4) fis8 g2. a,4 }
\header { piece = "La rédemption par l'amour" }
}

\score{
\relative c {\clef bass \time 3/4
\key g \major e2 (fis4 a4. g8 fis8. e16 d'2 c4)  }
\header { piece = "Soumission de Brünnhilde" }
}

\score{
\new StaffGroup <<
\new Staff \relative c'' {\clef treble \key e \major \time 3/4 
\set Staff.autoBeaming = ##f
e2.~e2.~e8 fis,8 fis4 fis4 cis'2 b8 a8 gis4
}
\new Staff \relative c'' {\clef treble \key e \major \time 3/4 
e4.(dis8 cis8. b16 a'2 gis4) fis4.(e8 dis8. cis16 cis'2 b8 a8 gis4))
}
>>
\header { piece = "L'annonce d'une nouvelle vie" }
}

\score{
\new StaffGroup <<
\new Staff \relative c'' {\clef treble \key d \major \time 4/4 
c2 (b bes2. a4 gis) r4 r2 r1 r1}
\new Staff \relative c'' {\clef treble \key d \major \time 4/4
r1 r1 gis2 (g ges2. f4 e8) r8 r4 r2
}
>>
\header { piece = "Le sommeil éternel" }
}

\score{
\relative c' {\clef treble \key e \major \time 4/4 
\partial 2 e8 (cis' b gis16. fis32 e8) }
\header { piece = "Le sommeil de Brünnhilde" }
}

\score{
\relative c {\clef bass \key g \major \time 4/4 
\set Staff.autoBeaming = ##f
\partial 4 fis4 b4. bis8 cis2 cis4. b16 ais b4. b16 b16
c4. b8 b4 a8. r16 b4. fis8 gis2
 }
\header { piece = "Chant d'adieu de Wotan" }
}
}

\bookpart {
\header {title = "Siegfried"}
\score{
\relative c'' {\clef treble \key g \major \time 6/8 
g8\staccatissimo d'8.\marcato b16\staccatissimo
g8\staccatissimo a\staccatissimo b\staccatissimo 
c\staccatissimo b\staccatissimo a\staccatissimo 
d\staccatissimo c\staccatissimo b\staccatissimo 
e\staccatissimo d\staccatissimo c\staccatissimo 
fis\staccatissimo e\staccatissimo d\staccatissimo 
}
\header { piece = "Appel du fils des bois" }
}

\score{
\relative c'' {\clef treble \key bes \major \time 2/4 
\grace{\times 2/3 {d8 ([e fis]}} g8) [d ees bes] c [g a d,]
}
\header { piece = "L'amour de la vie" }
}

\score{
\relative c' {\clef tenor \key f \major \time 6/8 
g4.(~g4 gis8 a4.~a4 b8 c4 cis8 e4 d8 c4. b4.))
}
\header { piece = "L'amour filial" }
}

\score{
\relative c'' {\clef tenor \key bes \major \time 6/8
g4 f8 ees d4 f ees8 d c4
}
\header { piece = "Le désir de voyager" }
}

\score{
\new StaffGroup <<
\new Staff \relative c' { \clef treble \time 4/4
<b fis' b>2-. (<a d! a'>-. <bes f'! bes>-. <gis b e gis>-.)
}
\new Staff \relative c, { \clef bass \time 4/4
<dis fis dis'>2-. (<fis a fis'>-. <d! f! d'!>-. <e b'! e>-.)
}
>>
\header { piece = "Wotan errant" }
}

\score{
\relative c, {\clef bass \key des \major \time 3/4
r8. ees16 [aes8. bes16 c8. des16] |
ees8. [f16 ges8. aes16 bes8. c16] | des4
}
\header { piece = "La puissance divine" }
}

\score{
\relative c' {\clef C \key aes \major \time 4/4
\times 2/3 {ees8 (d des~}\times 2/3 {des c bes} \times 2/3 { aes g fis}
\times 2/3 {f d e} f)
}
\header { piece = "Mime Rampant" }
}

\score{
\relative c' {\clef treble \key d \major \time 3/4
a8[ \times 2/3 {a16 a a]} a4. d8-. |
a8-. [d-. a-. d-. a-. d-.]
bes[(d bes d bes d ] bes [d bes d bes] ) d-.
}
\header { piece = "La fonte de l'acier" }
}

\score{
\new StaffGroup <<
\new Staff \relative c { \clef bass \time 3/4
r16 c8 [r16 c16] c8 r8 fis,8 r8 c'8 r8
}
\new Staff \relative c {\clef bass \key aes \major \time 3/4
\partial 16
ges64 ([aes bes b] c8) r8 r4 ges8 r8 c8 r8 }
>>
\header { piece = "Fafner" }
}

\score{
\relative c' { \clef bass \key aes \major \time 4/4
c8 b4\marcato bes\marcato a8\marcato [aes\marcato g\marcato] |
<d fis>2. }
\header { piece = "La vengeance" }
}

\score{
\relative c'' { \clef treble \key e \major \time 3/4
\partial 4 b8-.[e16-. gis-.] fis2.-.\marcato }
\header { piece = "L'oiseau" }
}

\score{
\new StaffGroup <<
\new Staff \relative c''' { \clef treble \key bes \major \time 4/4
c2\marcato ees,2(~ees4 c8)des\staccatissimo ees4\marcato f\marcato g4.\marcato
aes8 bes2~bes4 r4 r2}
\new Staff \relative c { \clef bass \key bes \major \time 4/4
aes2. \times 4/6 {g16 (aes bes c des ees)}
f2 c4\marcato aes\marcato ees1~ees4 r4 r2}
>>
\header { piece = "L'héritage du monde" }
}

\score{
\relative c''' { \clef treble \time 3/4
<c e>4\marcato(<d f>\marcato <e g>\marcato)~<e g>
<d f>2\trill~<d f>\trill
<cis e>8. (<d f>16)
<f a>4.(<d f>8 <b d>8. <a c>16)
<a c>8 (<d, f> <g b> <f a> <cis e> <d f>)
<f a>4.(<cis e>8 <d f>8. <dis fis>16 <a' c>2)
}
\header { piece = "Salut au monde" }
}

\score{
\relative c'' { \clef treble \time 3/4
\set Staff.autoBeaming = ##f
\partial 4 d4 g8. b,8 fis'4. e8 \times 2/3 {d8 [c] b} a2
}
\header { piece = "Salut à l'amour" }
}

\score{
\relative c'' { \clef treble \time 3/4
e8. a32 (g) g8. f32(g) \afterGrace {f4\trill} {e16 [(f)]} |
e8. a32 (g) g8. f32(g) \afterGrace {f4\trill} {e16 [(f)]} }
\header { piece = "Enthousiasme de l'amour" }
}

\score{
\relative c'' { \clef treble \key e \major \time 4/4
b2(~b8 e, \times 2/3 { fis a b) } b2. b,4(
b'2~b8 e, \times 2/3 { fis a b } cis4 b2 e4 fis,2.)
}
\header { piece = "La paix" }
}

\score{
\relative c'' { \clef treble \key g \major \time 4/4
b1 b2( c4) ees aes4. (ees8) c4 aes |
ees'2 (des4.) c8 bes4 }
\header { piece = "Siegfried trésor du monde" }
}
\score{
\new StaffGroup <<
\set StaffGroup.autoBeaming = ##f
\new Staff \relative c''' { \clef treble \time 2/2 g1~g~g4 a,4 a2 r1}
\new Staff \relative c''' { \clef treble \time 2/2
r1 r1 b4 e, r4 d | c d8 [e] f [e] f g}
>>
\header { piece = "La décision d'aimer" }
}

}

\bookpart {
\header {title = "Götterdämmerung"}

\score{ \relative c' { \clef treble \key bes \major \time 4/4
ees4. (d32 ees f ees c'4. g8 bes4 c,2~c8 ees g2.)~g8 r8}
\header { piece = "Brünnhilde" }
}

\score{
\new StaffGroup <<
\new Staff \relative c''' { \clef treble \key ees \major \time 4/4
\set Staff.autoBeaming = ##f
g2(~g8 [f]) d bes g4(ees'2)~ees8 a,8 bes4 r4 r2 r1 r1 }
\new Staff \relative c' { \clef treble \key ees \major \time 4/4
\slurUp d2.(f4 g2. \afterGrace {a4\trill} {g16 [a]()} \times 2/3 {bes8) (cis) d-.}
g4.(f8 \times 2/3 {d8 [bes ) a-.] } g4(ees'2 c8 a) bes4 r4 r2
}
>>
\header { piece = "L'amour héroïque" }
}

\score{
\new Staff \relative c' { \time 3/4 \clef treble \key d \major
\grace{\times 2/3 { e16 [(fis g)]}} a4-. fis2 |
\grace{\times 2/3 { fis16 [(gis a)]}} b4-. cis,2 }
\header { piece = "Hagen" }
}

\score {
\new RhythmicStaff { \time 3/4 
c8. [c16-. c8. c16-. c8. c16-.] }
\header {piece= "Gibichungen"}
}

\score{
\new Staff \relative c'' { \time 3/4 \clef treble \key ees \major
r8 ees8 (fis,4. g8 aes8.[f!16] c'4~c16[d g f])
}
\header { piece = "Amitié perfide de Hagen" }
}

\score {
\new Staff \relative c' { \clef bass \key d \major \time 3/4
\set Staff.autoBeaming = ##f
g8 c, r4 \times 2/3 {cis8 e g} c, r8 r4 r
}
\header {piece= "Trahison par la magie"}
}

\score {
\new Staff \relative c''' { \clef treble \key g \major \time 3/4
\set Staff.autoBeaming = ##f
d4( g,4. a8 b4 e,4. fis8 g8. [a16] a2\trill \grace{gis16 [a]} d2. )
}
\header {piece= "Bienvenue de Gutrune"}
}

\score {
\new Staff \relative c' { \clef bass \key bes \major \time 4/4
d2. d4 b2 gis4. e8 dis1
}
\header {piece= "Justice de l'expiation"}
}

\score {
\new Staff \relative c'' { \clef treble \key bes \major \time 4/4
\partial 8
ges8~ges2 \(ges8[f bes, \acciaccatura des8 ces] aes\) r
}
\header {piece= "Le meurtre"}
}

\score {
\new Staff \relative c' { \clef bass \key g \major \time 3/4
<e g>4 <a, c>4. <b d>8 <c e>8. [<e g>16] <e g>2~<e g>4
}
\header {piece= "Appel au mariage"}
}

}

