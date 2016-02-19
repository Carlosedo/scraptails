from tempfile import mkstemp
from shutil import move
from os import remove, close


file_path = 'scraptails/items.json'
pattern1 = 'Absolut Vodka'
subst1 = 'Vodka'

pattern2 = '"name": ["Absolut '
subst2 = '"name": ["'


#Create temp file
fh, abs_path = mkstemp()

with open(abs_path, 'w') as new_file:
    with open(file_path) as old_file:
        for line in old_file:
            new_file.write(line.replace(pattern1, subst1).replace(pattern2, subst2))

close(fh)

#Remove original file
remove(file_path)

#Move new file
move(abs_path, file_path)
