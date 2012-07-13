" Syntax highlighting for SumItUp

syn match Identifier /\v\@\w+/
syn region Statement start="<" end=">" contains=Identifier

syn match Comment /\v^\s*;.*$/

" Match the last number
syn match Number /\v<[0-9.]+(\D*$)@=/

" ... except when NoACC is on. And keep <>s highlit.
syn match Normal /\v(^\s*--.*$|^.*--\s*$)/ contains=Statement,Identifier
