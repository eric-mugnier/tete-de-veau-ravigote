\include "_common.ly"

\score {
  \new Staff {
    \clef treble
    \key c \major
    \time 2/4

    \relative c' {

      % Measure 1
      c2

      % Measure 2
      d8 f e d |

      % Measure 3
      g4 g |

      % Measure 4
      g8 a e f |

      % Measure 5
      d4 d |

      % Measure 6
      d8 f e d |

      % Measure 7
      c8 c' b a |

      % Measure 8
      g8 f e d |

      % Measure 9
      c4
  \stopStaff
  \once \override TextScript.extra-offset = #'(0 . -3)
  s2^\markup { \italic "etc." }

      
|
    }
  }
  \commonLayout
  \midi { }
}