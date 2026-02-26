# Reasoning trajectory labeling.

This is the github repository for the in-class activity of UCSD's AI-Agent's class.

There are two parts for this activity:

1.) Take a reasoning trajectory from the Zork folder and read through it. Then, create a second .txt file and note down any weird reasoning behaviors. You should copy the relevant section from the original trajectory in quotes and then describe what the issue is below. For example:

---

"Wait, but how do they get a carrot? The available commands include 'take' and 'examine' other objects. Maybe they need to check if there's a carrot somewhere else in the kitchen. Let me check the observation again. The user is in the kitchen with a fridge, oven, table, counter, stove. The counter has the raw potatoes, banana, knife. The fridge might have ingredients. So perhaps they need to open the fridge to look for a carrot. The command 'open fridge' would be necessary here. Once they open the fridge, maybe they can find the carrot and take it. Then they can slice it with the knife and proceed with the recipe. So the next action should be to open the fridge. Let me make sure there's no other way. The user can't get a carrot from the current items. So the correct next step is to open the fridge."

Excessive token use. The model arrives at the right action after sentence 5 but continues to ramble for 6 sentences after that.

---

(This is an example from textworld but same idea.)

2.) Open the AIME folders and browse through reasoning_trace_A and reasoning_trace_B. The folders have reasoning traces from a model attempting a number of American Invitational Mathematics Examination problems. For each folder, one reasoning trace is correct and one reasoning trace is incorrect. Your task is to determine which file has the CORRECT trace. Note, these reasoning traces in their entirety are extremely long, so we have truncated the ones included.
