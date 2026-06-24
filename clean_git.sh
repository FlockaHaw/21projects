#!/bin/bash
# Удаляем все .git-каталоги внутри текущей папки, кроме корневого.
# Работает рекурсивно (удалит и вложенные .git в materials/src и т.п.).

find . -type d -name ".git" ! -path "." ! -path "./.git" -exec rm -rf {} +
