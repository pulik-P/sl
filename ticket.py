tic = input("Введите номер билета: ")

if len(tic) == 6:
  num_tic1 = int(tic[0]) + int(tic[1]) + int(tic[2])
  num_tic2 = int(tic[3]) + int(tic[4]) + int(tic[5])
  if num_tic1 == num_tic2:
      print("Счастливый билет")
  else:
      print("Несчастливый билет")
else:
    print("должно быть 6 цифр")