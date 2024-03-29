ALPHABET = "abcdefghijklmnopqrstuvwxyz"

word = "and"
insert_list = []
delete_list = []
replace_list = []
transpose_list = []
for i in range(len(word)):
    delete_list.append(word[:i] + word[i+1:])
    for j in range(i+1, len(word)):
        transpose_list.append(word[:i] + word[j] + word[i+1:j] + word[i] + word[j+1:])
    for letter in ALPHABET:
        insert_list.append(word[:i] + letter + word[i:])
        replace_list.append(word[:i] + letter + word[i+1:])
        

print(insert_list)
print(delete_list)
print(replace_list)
print(transpose_list)