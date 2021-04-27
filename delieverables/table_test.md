\begin{table}[]
\begin{tabular}{|l|l|l|l|l|l|l|l|}
\hline
idiom & frequency & \multicolumn{5}{l|}{collocations}          & use cases \\ \hline
      &           & model & verb          & noun & adj  & adv  &           \\ \hline
from\_a\_to\_z &
  1 &
  tf &
  (scan, 2) &
  None &
  None &
  None &
  \begin{tabular}[c]{@{}l@{}}He knew his subject from A to Z.\\ This book tells the story of her life from A to Z.\\ The book is titled "Home Repairs From A to Z.\end{tabular} \\ \hline
      &           & tfidf & (scan, 1.0)   & None & None & None &           \\ \hline
      &           & pmi   & (scan, 15.65) & None & None & None &           \\ \hline
      &           & tf    &               &      &      &      &           \\ \hline
      &           & tfidf &               &      &      &      &           \\ \hline
      &           & pmi   &               &      &      &      &           \\ \hline
\end{tabular}
\end{table}