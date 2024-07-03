def fizzbuzz(length):
  for i in range(1, length + 1):
    output = ''

    if(i % 3 == 0):
      output += 'Fizz'

    if(i % 5 == 0):
      output += 'Buzz'

    print(output if output else i)

fizzbuzz(100)