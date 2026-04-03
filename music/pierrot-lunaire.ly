\include "_common.ly"

% ============================================================
% Pierrot Lunaire – Schoenberg
% Rezitation (Sprechstimme), opening bars
% ============================================================
%%% \header {
%%%   title = "Pierrot Lunaire"
%%%   subtitle = "I. Teil."
%%%   subsubtitle = "1. Mondestrunken."
%%%   composer = "Arnold Schoenberg"
%%%   opus = "Op. 21"
%%% }

sprechUp = {
  \override Voice.Stem.stencil = #(lambda (grob)
    (let ((stem (ly:stem::print grob)))
      (if (ly:stencil? stem)
          (ly:stencil-combine-at-edge
            stem Y UP
            (ly:text-interface::print grob) -2.4)
          stem)))
  \override Voice.Stem.text = \markup {
    \hspace #-0.44 \teeny \musicglyph #"noteheads.s2cross" }
}

sprechDown = {
  \override Voice.Stem.stencil = #(lambda (grob)
    (let ((stem (ly:stem::print grob)))
      (if (ly:stencil? stem)
          (ly:stencil-combine-at-edge
            stem Y DOWN
            (ly:text-interface::print grob) -3)
          stem)))
  \override Voice.Stem.text = \markup {
    \hspace #-1.075 \teeny \musicglyph #"noteheads.s2cross" }
}

sprechOff = {
  \revert Voice.Stem.stencil
  \revert Voice.Stem.text
}

vocal = \relative c'' {
  \clef treble
  \key c \major
  \time 2/4
  \tempo \markup { \bold "Bewegt" " (♩ ca 66)" }

  \dynamicUp
  \autoBeamOff
  \stemUp

  %% R2 |
  %% r4 r8 
  \partial 8
  \sprechUp
  a8\p |
  b ais! gis! \tweak shorten-pair #'( 0 . -8 ) \< a! |
  \time 3/4
  c! \! \tweak shorten-pair #'( 3 . 2 ) \> b! gis!\! r r a! \tweak shorten-pair #'( 0 . -9 ) \< |
  \time 2/4
  g! ees! d!8. cis!16 |
  \time 3/4
  f!4. \! des!8 \tweak shorten-pair #'( -2 . 2 ) \> c! a! \! |
  %% \time 2/4
  %% r4
  \bar ""

  \stopStaff
  %% \once \override TextScript.extra-offset = #'(0 . -3)
  %% s2^\markup { \italic "etc." }
}

vocalLyrics = \lyricmode {
  Den Wein, den man mit Au -- gen trinkt, gießt nachts der Mond in Wog -- gen nie -- der
}

\score {
  <<
    \new Staff 
%%%     \with {
%%%       instrumentName = \markup { \italic "Rezitation." }
%%%     }
    {
      \new Voice = "voc" \vocal
    }
    \new Lyrics \lyricsto "voc" \vocalLyrics
  >>
  \commonLayout
  \midi { \tempo 4 = 70 }
}