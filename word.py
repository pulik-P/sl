word = input("Введите слово: ")
num_letters = len(word)

if num_letters % 2 == 1:
    mid_index = num_letters // 2
    result = word[mid_index]
else:
    mid_index1 = num_letters // 2 - 1
    mid_index2 = num_letters // 2
    result = word[mid_index1] + word[mid_index2]
print(result)