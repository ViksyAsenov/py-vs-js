numberToWordMap = {
  3: 'Fizz',
  5: 'Buzz',
  7: 'DrugaDuma'
}

def fizzbuzz(length):
  for i in range(1, length + 1):
    output = ''

    for key, value in numberToWordMap.items():
      if(i % key == 0):
        output += value

    print(output or i)

fizzbuzz(100)