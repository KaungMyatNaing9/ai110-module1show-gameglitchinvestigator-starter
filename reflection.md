# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
The game look simple and it seems to work like what it should be but after detail checkings, I found that there were many bugs in the game. Based on my understandings, user type in a number ranging from 1 to 100, and the game will give you hint whether the typed number is lower or upper the target number. There is no validation for whether the number was out of range or not, and the hints were backwards. In the first try I typed 1 as my first input and it said lower and I type 0 and it still said lower then i typed negative and it still said lower and I realized the two bugs in first try.
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
    1. The hints were backwards. The lower and upper are reversed.
    2. There is no validation for whether the input number was out of range or not. The game should only accept numbers between 1 and 100, but it accepts any number, including negative numbers, zero and numbers greater than 100.
    3. After the game is over, either win or lose, we cannot start a new game without refreshing the page. The game should allow users to start a new game after the current game ends.
    4. The Attempts Left is off by one, it means it should ends when the attempts left is 0, but it ends when the attempts left is 1. It should be fixed to end when the attempts left is 0.
    5. The difficulty level is not working, so based on my understanding by looking at left sidebar, for easy mode, the range should be 1 to 20 and attempts should be 6, for normal mode, the range should be 1 to 100 and attempts should be 8, for hard mode, the range should be 1 to 50 and attempt should be 5. I am not sure if this should be the difficulty of each level but it kind of doesnt make senese.
    6. In no hint mode, after the user type a number it should at least say its correct or not, it is not necessay but good to have. 
    7. When user input a number the input box right side say press enter to apply, but it is not working, the user have to click the submit button to apply the input. It should be fixed to allow users to press enter to submit the input.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
