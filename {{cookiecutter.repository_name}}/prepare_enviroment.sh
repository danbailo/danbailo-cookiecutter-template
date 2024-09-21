#!/bin/bash

define_shell_rc() {
    if [ -e "$HOME/.zshrc" ]; then
        SHELL_RC_PATH="$HOME/.zshrc"
    else                         
        SHELL_RC_PATH="$HOME/.bashrc"
    fi
}

bkp_shell_rc() {
    cp "$SHELL_RC_PATH" "$SHELL_RC_PATH.bkp"
    printf "Created a backup of $SHELL_RC_PATH\n"
}

uv_settings() {
    printf "\n# UV Settings\n"
    printf "alias python='.venv/bin/python'\n"
    printf "if [ -f .venv/bin/activate ]; then\n"
    printf "    source .venv/bin/activate\n"
    printf "fi\n\n"  # Added newline after the closing if statement
}

define_shell_rc

bkp_shell_rc

if ! grep -q "UV Settings" "$SHELL_RC_PATH"; then
    uv_settings >> "$SHELL_RC_PATH"
    printf "Environment prepared!\n"
else
    printf "Environment already configured!\n"
fi
