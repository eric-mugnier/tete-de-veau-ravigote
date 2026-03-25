\version "2.24.4"

\header {
%  title = "Piano Concerto in G major"
%  subtitle = "Adagio assai (opening excerpt)"
%  composer = "Maurice Ravel"
}

upper = \relative e' {
  \key e \major
  \time 3/4
  \tempo "Adagio assai" 4 = 76

  \voiceOne
    R2.\p |
    gis4_\markup { \italic "espressivo" }( a2 |
    gis4 fis e |
    b'~ b8 a16 b cis b~ b8~ |
    b2~ b8) b8( |
    b4 cis b |
    gis2~ gis16 fis e fis |
    gis fis~ fis8~~ fis4~ fis8 ) fis~ |
    fis[ gis] b[ gis] fis[ cis] |

  % Opening long melody
}

lower = {
  \key e \major
  \time 3/4
  \clef bass

  \voiceTwo

  e,8\sustainOn[ <gis e'>] <gis e'>[ e,] <gis e'>[ <gis e'>] |
  e,8[ <gis e'>] <gis e'>[ e,] <gis e'>[ <gis e'>] |
  e,8[ <gis e'>] <gis dis'>[ e,] <gis cis'>[ <gis cis'>] |
  gis,[ <b dis'>] <b dis'>[ gis,] <b dis'>[ <b dis'>] |
  gis,[ <b dis'>] <b dis'>[ gis] <b dis'>[ <b dis'>] |
  gis8[ <a e'>] <a e'>[ gis] <a e'>[ <a e'>] |
  fis8[ <a e'>] <a e'>[ fis] <a e'>[ <a dis'>] |
  e8[ <a dis'>] <a dis'>[ e] <a cis'>[ <a cis'>] |
  dis8[ <a cis'>] <a cis'>[ dis] <gis cis'>[ <gis b>] |
}

\score {
  \new PianoStaff  \with {
  instrumentName = "Piano"
} <<
    \new Staff = "RH" <<
      \upper
    >>
    \new Staff = "LH" <<
      \lower
    >>
  >>
  \layout { }
}