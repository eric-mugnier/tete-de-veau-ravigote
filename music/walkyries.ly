\version "2.24.0"

\score {
  \new Staff \relative c' {
    \clef tenor 
    \time 9/8 
    \partial 8
    g8 |
    c8.-> g16 c8 e4. c |
    e8.-> c16 e8 g4. e |
    g8.-> e16 g8 b4. b, |
    e8.-> b16 e8 gis2.
  }
  \header { }
  \layout { 
    ragged-right = ##f
    indent = 0
    \context {
      \Score
      \omit BarNumber
      \override SpacingSpanner.uniform-stretching = ##t
    }    
  }
  \midi { }
}
