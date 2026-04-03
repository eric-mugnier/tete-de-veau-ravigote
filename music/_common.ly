\version "2.24.4"

#(set-global-staff-size 12)

\paper {
  ragged-right = ##f
  ragged-last = ##f
}

commonLayout = \layout {
  indent = 0
  \context {
    \Score
    \omit BarNumber
  }
}
