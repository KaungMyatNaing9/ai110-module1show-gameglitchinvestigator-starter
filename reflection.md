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
I use Claude code Opus 4.6 and a little bit of copilot on inline code suggestions.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
Claude suggested me on the score system doesnt make sense for the game and I verified it by testing different condition and what i get for the score and I realize most of the time the score is negative even I win which doesnt make sense. So I let Claude fix it. This is what claude suggested:
"Three things that don't make sense: Too High on even attempts gives you +5 points. You guessed wrong and you're rewarded. There's no game logic reason for this — it just creates a quirky exploit where a player could farm points by intentionally guessing high on even turns. Too High and Too Low are treated asymmetrically. Too Low always deducts 5. Too High sometimes adds 5, sometimes deducts 5. A wrong guess is a wrong guess — both directions should behave the same. The +1 offset in the win formula is a double-penalty. In app.py:89, st.session_state.attempts is already incremented before update_score is called. So attempt_number passed in is already 1-indexed. The +1 inside the formula makes it act like attempt 2 when it's actually attempt 1: Guess correctly on your 1st try → 100 - 10*(1+1) = 80 instead of 90"

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
Same with what it suggested on Score system I let Claude fix the score system, yes it fix it but it still doesnt make sense as I still get negative score if I use too many attempts even I win the game. So I need to let Claude refix this by giving exact prompt of what I want the scoring system to be. 
This is what Claude do incorrectly: "Win: max(100 - 10*(attempt-1), 10) — 1st guess = 100pts, 2nd = 90pts, ...Too High → -10 (same as Too Low) Too Low → -10 (symmetric)"
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I test it manually in the game by trying different inputs and see if the game behaves as expected. I also let Claude write some test cases for the functions in logic_utils.py and run those test cases to see if the functions return the expected results. If the game behaves as expected and all the test cases pass, then I consider the bug is fixed.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  I try to see if the secret number change if I go to different difficulty mode. I found that the secret number remain the same even I switch to easy mode which have a range of 20 and the secret remain 29 which is out of range for easy mode. So I realize that the secret number should be reset when I switch to different difficulty mode. After I fix it, I test it again and I found that the secret number change to a number between 1 and 20 when I switch to easy mode which is expected.

- Did AI help you design or understand any tests? How?
Yes, I ask Claude to write some test cases for the functions in logic_utils.py and it help me understand how to test the functions and what kind of test cases I should write. For example, for the function get_range_for_difficulty, Claude suggest me to write test cases for each difficulty level and also for an invalid difficulty level. This help me understand how to test the function and what kind of edge cases I should consider when writing test cases.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Streamlit reruns means that every time you interact with the app, such as clicking a button or changing a slider, the entire script is rerun from top to bottom. This allows Streamlit to update the app in real-time based on user interactions. However, this also means that any variables defined in the script will be reset to their initial values every time the script is rerun. To preserve the state of variables across reruns, Streamlit provides a feature called session state. Session state allows you to store variables that persist across reruns, so you can keep track of user interactions and maintain the state of your app even as it updates in real-time.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
  One habit I would reuse would be prompting different bug fix in different chat so Claude only fix that one specific bug and not change other part of the code. 

- What is one thing you would do differently next time you work with AI on a coding task?
I think I should give more specific or detailed prompt instead of just expecting it have more knowledge than me and trust it to fix the code in its way just like the score system. 

- In one or two sentences, describe how this project changed the way you think about AI generated code.
This project made me realize that AI can be a powerful tool for debugging and testing, but it's important to provide clear and specific instructions to get the desired results.