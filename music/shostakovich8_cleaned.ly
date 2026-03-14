\version "2.24.3"

\pointAndClickOff

\header {
}

\paper {
}
\layout {
    \context { \Score
    }
}

PartPOneVoiceOne =  \relative d'' {
    \clef "treble" \time 4/4 r1 | % 1
    r2 r4 r8 r16 r32 c | % 2
    g'2.... as32 | %% ( \ 
    as4 bes4.. es,32 [  f32 ]  g8. [  d32  es32 ] |
    f4 ( c8 [ d8 ] es4 ) bes4 
    }

PartPTwoVoiceOne =  \relative c {
    \clef "bass" \time 4/4 
    c4...\ff bes32 c2 ~
    c8.. [ a32 ] c8.. [ as'32 ] \stemUp
    g2 ~ g4... ges32 f2 ~ f4.. es32
    [ d32 ] es2 ~ |
    es4 f2 ges8. [ f32
    es32 ] }


% The score definition
\score {
    <<
        \new Staff
        <<
            \context Staff << 
                \mergeDifferentlyDottedOn\mergeDifferentlyHeadedOn
                \context Voice = "PartPOneVoiceOne" {  \PartPOneVoiceOne }
                >>
            >>
        \new Staff
        <<
            \context Staff << 
                \mergeDifferentlyDottedOn\mergeDifferentlyHeadedOn
                \context Voice = "PartPTwoVoiceOne" {  \PartPTwoVoiceOne }
                >>
            >>
        
        >>
    \layout {}
    % To create MIDI output, uncomment the following line:
    %  \midi {\tempo 4 = 100 }
    }

