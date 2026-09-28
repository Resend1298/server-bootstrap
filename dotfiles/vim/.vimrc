" automatically install vim-plug if not already installed
if empty(glob('~/.vim/autoload/plug.vim'))
	silent !curl -fLo ~/.vim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
endif

" automatically install missing plugins
autocmd VimEnter * if len(filter(values(g:plugs), '!isdirectory(v:val.dir)'))
	\| PlugInstall --sync
	\| source $MYVIMRC
\| endif

call plug#begin()
Plug 'arcticicestudio/nord-vim'
call plug#end()

" ignore errors when first time running vim and nord is not installed yet
silent! colorscheme nord
set number
