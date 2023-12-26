# Lines configured by zsh-newuser-install
HISTFILE=~/.histfile
HISTSIZE=1000
SAVEHIST=1000
setopt extendedglob nomatch notify
unsetopt autocd beep
bindkey -v
# End of lines configured by zsh-newuser-install
# The following lines were added by compinstall
zstyle :compinstall filename '/home/jannis/.zshrc'

autoload -Uz compinit
compinit
# End of lines added by compinstall

# Autoload zsh's `add-zsh-hook` and `vcs_info` functions
# (-U autoload w/o substition, -z use zsh style)
autoload -Uz add-zsh-hook vcs_info

# Set prompt substitution so we can use the vcs_info_message variable
setopt prompt_subst

# Run the `vcs_info` hook to grab git info before displaying the prompt
add-zsh-hook precmd vcs_info

# Style the vcs_info message
zstyle ':vcs_info:*' enable git
zstyle ':vcs_info:git*' formats '%b%u%c'
# Format when the repo is in an action (merge, rebase, etc)
zstyle ':vcs_info:git*' actionformats '%F{14}⏱ %*%f'
zstyle ':vcs_info:git*' unstagedstr '*'
zstyle ':vcs_info:git*' stagedstr '+'
# This enables %u and %c (unstaged/staged changes) to work,
# but can be slow on large repos
zstyle ':vcs_info:*:*' check-for-changes true

autoload -U colors && colors
autoload -U promptinit && promptinit

function testfunc() {
  branch=$(git symbolic-ref HEAD 2> /dev/null | awk 'BEGIN{FS="/"} {print $NF}')
  if [[ $branch == "" ]];
  then
    echo '%k%F{red}\Ue0b4%f'
  else
    echo '%k%K{green}%F{red}\Ue0b4%f '$branch' %k%F{green}\Ue0b4%f'
  fi
}
#Ue0b0
PS1=$'%F{blue}\Ue0b6%f%K{blue} %(?..) %k%F{blue}%K{red}\Ue0b4%k%f%K{red} %~ $(testfunc) '
RPS1=''
#RPS1='%F{8}⏱ %*%f'
#PROMPT=
