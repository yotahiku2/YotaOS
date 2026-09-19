# YotaOS interactive Bash prompt
# Applied only to interactive Bash sessions.

[ -n "${BASH_VERSION:-}" ] || return
case $- in
    *i*) ;;
    *) return ;;
esac

# Don't override a prompt the user explicitly requests.
[ "${YOTAOS_DISABLE_PROMPT:-0}" = "1" ] && return

_yotaos_git_branch()
{
    command -v git >/dev/null 2>&1 || return

    local branch
    branch=$(git symbolic-ref --quiet --short HEAD 2>/dev/null) ||
        branch=$(git rev-parse --short HEAD 2>/dev/null) ||
        return

    printf '%s' "$branch"
}

_yotaos_set_prompt()
{
    local exit_code=$?
    local branch
    branch=$(_yotaos_git_branch)

    # ANSI colors wrapped in \[...\] so Bash calculates prompt width correctly.
    local reset='\[\e[0m\]'
    local dim='\[\e[38;5;244m\]'
    local green='\[\e[38;5;48m\]'
    local cyan='\[\e[38;5;81m\]'
    local white='\[\e[38;5;252m\]'
    local red='\[\e[38;5;203m\]'

    local status_color="$green"
    if (( exit_code != 0 )); then
        status_color="$red"
    fi

    PS1="${dim}╭─${green}[YotaOS]${dim}─${cyan}[\u"

    if [[ -n "$branch" ]]; then
        PS1+="${white}@${green}${branch}${cyan}"
    fi

    PS1+="${cyan}]${dim}─${white}[\w]${reset}\n"
    PS1+="${dim}╰─${status_color}❯${reset} "
}

PROMPT_COMMAND="_yotaos_set_prompt${PROMPT_COMMAND:+;$PROMPT_COMMAND}"
