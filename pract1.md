# Практика 1
## Задание 1
```
localhost:~# cd /etc

localhost:/etc# cut -d: -f1 passwd | sort
```
## Задание 2
```
localhost:/etc# awk '{print $2, $1}' protocols | sort -nr | head -n 5

localhost:/etc# cd ~
```
## Задание 3
```
localhost:~# nano banner

# рисуем рамку по длине текста
text="$1"
length=${#text}
line=$(printf '%*s' "$length" ''| tr ' ' '-')
echo "+-${line}-+"
echo "| ${text} |"
echo "+-${line}-+"

localhost:~# chmod +x banner
localhost:~# ./banner "Hello from RTU MIREA!"
```
## Задание 4
```
localhost:~# nano find_ids

# ищем все идентификаторы и убираем повторы
filename="$1"
grep -oE '[a-zA-Z_][a-zA-Z0-9_]*' "$filename" | sort -u | xargs

localhost:~# chmod +x find_ids
localhost:~# ./find_ids hello.c
```
## Задание 5
```
localhost:~# nano reg

# выдаём права и копируем команду в /usr/local/bin
name="$1"
chmod +x "$name"
cp "$name" /usr/local/bin/

localhost:~# chmod +x reg
localhost:~# ./reg banner
localhost:~# banner "Работает!"
```
## Задание 6
```
localhost:~# nano check_comments

# перебираем все файлы нужных расширений
for file in *.c *.js *.py; do
    # пропускаем, если файла нет
    [ -f "$file" ] || continue

    # берём первую строку
    first=$(head -n 1 "$file")

    # проверяем, начинается ли строка с комментария
    case "$first" in
        //*|/\**|\#*) echo "$file: комментарий есть" ;;
        *) echo "$file: комментария нет" ;;
    esac
done

localhost:~# chmod +x check_comments
localhost:~# ./check_comments
```
## Задание 7
```
localhost:~# nano find_dupes

# считаем md5 каждого файла и ищем совпадающие хэши
dir="${1:-.}"
find "$dir" -type f -exec md5sum {} + | sort | uniq -w32 -D

localhost:~# chmod +x find_dupes
localhost:~# ./find_dupes .
```
## Задание 8
```
localhost:~# nano make_tar

# находим файлы с расширением и упаковываем в tar
dir="$1"
ext="$2"
archive="archive_${ext}.tar"
find "$dir" -maxdepth 1 -name "*.$ext" -print0 | tar --null -cvf "$archive" --files-from=-
echo "Создан архив $archive"

localhost:~# chmod +x make_tar
localhost:~# ./make_tar . c
```
## Задание 9
```
localhost:~# nano space_to_tab

# меняем 4 пробела на таб
in="$1"
out="$2"
sed 's/    /\t/g' "$in" > "$out"
echo "Готово: $out"

localhost:~# chmod +x space_to_tab
localhost:~# ./space_to_tab hello.c hello_tab.c
```
## Задание 10
```
localhost:~# nano find_empty

# ищем пустые .txt файлы в каталоге
dir="${1:-.}"
find "$dir" -maxdepth 1 -type f -empty -name "*.txt"

localhost:~# chmod +x find_empty
localhost:~# ./find_empty .
```
