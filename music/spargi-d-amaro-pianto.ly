\version "2.24.3"

\header {
}

soprano = \relative c'' {
  \clef treble
  \key ees \major
  \time 3/4

  bes8 r g' r ees r  |
  bes2 a4 |
  c2. |
  bes4 r r |
  g8 r f r g r |
  c2 bes4 |
  c4~ c8  [ \melisma bes] a [g] \melismaEnd |
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
  \layout { }
  \midi { }
}