" Syntax highlighting for SumItUp

syn match Identifier /\v\@\w+/
syn region Statement start="<" end=">" contains=Identifier
syn match Comment /\v^\s*;.*$/

" match the last number on the line so the user knows what's included in
" accumulation.
syn match Number /\v<[0-9.]+(\D*$)@=/

" match the result the same way? hmm...

