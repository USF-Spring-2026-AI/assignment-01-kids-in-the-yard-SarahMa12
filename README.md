# AI Assignment 01 - Kids in the Yard

See assignment details on Canvas.

# Comparison

## Which tool(s) did you use?

I used Gemini

## If you used an LLM, what was your prompt to the LLM?

I had to chat with it a couple times before the code ran with no errors. I first copy and pasted the whole implementation portion from the PDF, as well as how the csv files were storing the data and that it didn’t need to implement the graduate parts. I think it got confused on mapping the last names to the probabilities in the other CSV so there were errors when I tried to run the first piece of generated code. It also started blaming me that my csv files were wrong, but after 2-3 chats with it and pasting in the error on my terminal, it worked. 

## What differences are there between your implementation and the LLM?

Everything was in one file from the LLM. It is used with open() as f for reading files and I used pandas. The way it generated a person took way less code. The LLM used a couple functions I didn’t know about like zip(). It also implemented more fall backs, error checking, and clean ups when I didn’t really. 

## What changes would you make to your implementation in general based on suggestions from the LLM?

Although my code runs correctly, I would improve it by adding more error checking and safeguards. It would allow more reusability in different situations without crashing when I can throw an error. I would include proper validation, handling incorrect input, and extra clean ups on input. The LLM also used a queue and I would possibly make this change because a queue is more clear and structured to manage the processing order especially when making a tree and traversing it. It would definitely make it easier to follow and more efficient.

## What changes would you refuse to make?

For me making reusable helper functions in PersonFactory to get life expectancies, first names, last names makes understanding the code much easier for me. I was also able to reuse it when creating the create spouse and create child functions. Though the LLM did this in a much easier way with less code it was a little less intuitive with first glance so I would keep the way I did it. It also made the menu and querying logic in one whole function but the way I did it in different functions was much more clear and organized. 
