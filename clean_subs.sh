#!/bin/bash
# Находит все подмодули (режим 160000) в индексе и удаляет их

git ls-files --stage | grep ^160000 | while read -r mode hash stage path; do
    echo "Удаление из индекса: $path"
    git rm --cached "$path"
done

echo "Готово. Теперь выполните 'git add .' и проверьте статус."
