\version "2.24.4"


\header {
}

upper = \relative c'' {
  \clef treble
  \key c \major
  \time 2/4
  \partial 8
  g16( e) |
  \autoBeamOff
  c8 c
  c16[ d ]
  e f |
  g8 g g e |
  a a a8. g16 |
  a8. g16 a b c d |
  e4. c16 g |
  c4. g16 e |
  g4. d16 e |
  c2
}


parole = \lyricmode {
  I wish I was in the land of cot -- ton,
  Old times they are not for -- got -- ten;
  Look a -- way! Look a -- way! Look a -- way! Dix -- ie Land.
}

\score {
  <<
    \new Voice = "melody" { \upper }
    \new Lyrics \lyricsto "melody" { \parole }
  >>
  \layout { 
    indent = 0
    \context {
      \Score
      \omit BarNumber
    }    
  }
  \midi { }
}