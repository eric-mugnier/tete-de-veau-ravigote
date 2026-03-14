\version "2.24.0"

\paper {
  left-margin = 0
  right-margin = 0
}

\header {
  tagline = ##f
}

\score {
  \new Staff {
    \clef treble
    \key c \minor
    \time 4/4
    \tempo "Adagio" 4 = 52

    \relative c'' {
      % Thème initial des cordes (violoncelles/altos), transposé en clé de sol
      c2~ c8 bes aes g |
      f2~ f8 ees d c |
      bes2~ bes8 c d ees |
      f4 g aes2~ |
      aes8 g f ees d4 c~ |
      c1 |
    }
  }

  \layout {
    indent = 0
  }
  \midi { }
}
