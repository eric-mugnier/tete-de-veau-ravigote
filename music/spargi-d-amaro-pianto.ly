\include "_common.ly"

\header {
}

soprano = \relative c'' {
  \clef treble
  \key ees \major
  \time 3/4

  bes8-. r8 \acciaccatura { bes^( } g'8-.) r ees-. r  
  bes2 a4 
  c2.-> 
  bes4 r r 
  \acciaccatura { aes8} g8 r fis r g r 
  c2-> bes4 
  c4~ c8  [ \melisma bes] \acciaccatura { bes} aes [g] \melismaEnd 
  f2
}

parole = \lyricmode {
  Spar -- gi d'a -- ma -- ro pian -- to
  Il mio ter -- re -- stre ve -- lo
}

\score {
  <<
    \new Voice = "lucia" { \soprano }
    \new Lyrics \lyricsto "lucia" { \parole }
  >>
  \commonLayout
  \midi { }
}