import sys
import time
import random
actived = str(input("Would you like to start the Number-Guessing game? ")).lower()
if actived in ["yes", "yeah", "yea", "absolutely", "sure", "definitely", "accord", "concur", "consensus", "unison"]:
  computer_choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
61, 62, 63, 64, 65, 66, 67, 68, 69, 70,
71, 72, 73, 74, 75, 76, 77, 78, 79, 80,
81, 82, 83, 84, 85, 86, 87, 88, 89, 90,
91, 92, 93, 94, 95, 96, 97, 98, 99, 100]
  computer_number = random.choice(computer_choices)
  while True:
    user_guess = input("Guess the number: ")
    if not user_guess in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
"11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
"21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
"31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
"41", "42", "43", "44", "45", "46", "47", "48", "49", "50",
"51", "52", "53", "54", "55", "56", "57", "58", "59", "60",
"61", "62", "63", "64", "65", "66", "67", "68", "69", "70",
"71", "72", "73", "74", "75", "76", "77", "78", "79", "80",
"81", "82", "83", "84", "85", "86", "87", "88", "89", "90",
"91", "92", "93", "94", "95", "96", "97", "98", "99", "100"]:
      print("Please put in a valid number.")
    else:
      user_guess = int(user_guess)
      if user_guess == computer_number:
        print("You guessed it!")
        print(f"The Computer chose the number: {computer_number}")
        computer_number = random.choice(computer_choices)
      elif user_guess > computer_number:
        print("Lower!")
      elif user_guess < computer_number:
        print("Higher!")
      else:
        print("Please put in a number.")
else:
  print("Closing the program..")
  time.sleep(3)
  exit("Successfully exited the program.")