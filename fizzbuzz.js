const numberToWordMap = {
  3: "Fizz",
  5: "Buzz",
  7: "DrugaDuma",
};

function fizzbuzz(length) {
  for (let i = 1; i <= length; i++) {
    let output = "";

    for (const [key, value] of Object.entries(numberToWordMap)) {
      if (i % key === 0) {
        output += value;
      }
    }

    console.log(output || i);
  }
}

fizzbuzz(100);
