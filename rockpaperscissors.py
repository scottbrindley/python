#!/bin/python3

#from random import randint
import random

choice = input("Choose Rock, Paper, Scissors")
#choice = "Rock"
print("You chose", choice)

err = ["Rock", "Paper", "Scissors"]
if choice not in err:
  print("ERROR: Please choose one of the values")
  raise SystemExit('error in code want to exit')

botOptions = ["Rock", "Paper", "Scissors"]
botChoice = random.choice(botOptions)
print("Bot chose", botChoice)

if choice==botChoice:
  print("You draw")
elif choice == "Rock" and botChoice == "Scissors":
  print("You win")
elif choice == "Scissors" and botChoice == "Paper":
  print("You win")
elif choice == "Paper" and botChoice == "Rock":
  print("You win")
else:
  print("You lose")

