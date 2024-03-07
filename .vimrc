set clipboard=unnamed
set nowrap
set number
set mouse=a
syntax on
set term=kitty

call plug#begin()
Plug 'neoclide/coc.nvim', {'branch': 'release'}
"Plug 'vim-airline/vim-airline'
"Plug 'vim-airline/vim-airline-themes'
Plug 'lambdalisue/nerdfont.vim'
"Plug 'ryanoasis/vim-devicons'
call plug#end()

"let g:airline_powerline_fonts = 1
"let g:airline_theme='bubblegum'

nmap <space>e <Cmd>CocCommand explorer<CR>

highlight LineNr ctermfg=red
highlight Keyword ctermfg=blue
highlight Operator ctermfg=green
highlight Conditional ctermfg=green
highlight Statement ctermfg=green
