" SumItUp for vim
setlocal syntax=sumitup

if !exists("g:sumitup_parser")
    echom "Set up g:sumitup_parser in your .vimrc"
    let g:sumitup_parser = "./parsin.py"
endif

" Call the script workhorse and replace the whole buffer with new info.
" Yes, inefficient.
func SIUNaiveUpdate()
    let curpos = getpos(".")
    exe "0,$!".g:sumitup_parser
    call setpos(".", curpos)
endf

" Toggle commenting for the line
func SIUToggleComment()
    let line = getline('.')
    if line =~ '\v^\s*;'
        call setline('.', substitute(line, '^\s*;', '',''))
    else
        " comment
        exec "normal! gI;"
    endif
    call SIUNaiveUpdate()
endf

" Toggle ACC disable for the line
func SIUToggleACC()
    " prefer EOL
    let line = getline('.')

    " Check the beginning. Clear the end as well.
    if line =~ '\v^\s*--'
        call setline('.', substitute(line, '^\s*--', '', ''))
        call setline('.', substitute(getline('.'), '--\s*$', '', ''))
        call SIUNaiveUpdate()
        return
    endif

    " Check the ending
    if line =~ '\v^.+--\s*$'
        " contains --
        call setline('.', substitute(line, '--\s*$', '', ''))
    else
        " doesn't contain --
        call setline('.', substitute(line, '\s*$', ' --', ''))
    endif
    call SIUNaiveUpdate()
endf

nmap <buffer> <LocalLeader>e :call SIUNaiveUpdate()<CR>
nmap <buffer> <LocalLeader>c :call SIUToggleComment()<CR>
nmap <buffer> <LocalLeader>a :call SIUToggleACC()<CR>
