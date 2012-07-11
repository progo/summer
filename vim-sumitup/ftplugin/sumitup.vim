" SumItUp for vim
setlocal syntax=sumitup

if !exists("g:sumitup_parser")
    echom "Set up g:sumitup_parser in your .vimrc"
    let g:sumitup_parser = "./parsin.py"
endif

func NaiveUpdate()
    let curpos = getpos(".")
    exe "0,$!".g:sumitup_parser
    call setpos(".", curpos)
endf

nmap <buffer> <C-c><C-c> :call NaiveUpdate()<CR>
