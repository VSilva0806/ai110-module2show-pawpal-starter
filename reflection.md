# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
My UML design consists of 4 classes: Scheduler, Owner, Pet, and Task. Each class is contained within one another, where task is contained in pet and scheduler, pet is contained in owner, and scheduler manages owner.

- What classes did you include, and what responsibilities did you assign to each?
I chose four classes: Scheduler, Owner, Pet, and Task. Scheduler collects tasks from the owner and organizes it neatly and according to the Owner's relative schedule. Owner class consists of name of the owner and his/her pets owned. Pet class holds date about the pet (age, name, breed, and tasks). Task class contains information about a specific task, its time, and its completion. 

**b. Design changes**

- Did your design change during implementation?
Yes, I made several changes to my design. 
- If yes, describe at least one change and why you made it.
One change I made was removing the task field from scheduler as it already existed in Owner through Pets. I made sure the schedular recieves tasks from the owner class directly. I made this change to reduce redundancy and to ensure tasks do not get out of sync which could cause bugs. 
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
Some constraints my scheduler considers are vital tasks, task durations, conflict windows, frequencies, activities only for specific pets.
- How did you decide which constraints mattered most?
One way I decided constraints mattered most was by urgency and priority. For example, tasks like feeding pets or giving them medication was to be done first given missing those tasks can do crucial harm to the pet. I also decided frequency amttered because it helps the owner maintain consistency and lessens convolution in scheduling.
**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
One tradeoff my scheduler makes is that it only detects scheduling conflicts on a one pet basis. It does not consider various pets the owner owns as it can cause ineffiency and runtime errors.
- Why is that tradeoff reasonable for this scenario?
This tradeoff can be seen as reasonalble because some pet tasks can overlap and be done at the same time. For example, two dogs with a walk or feed task can be done simultaneously. Many tasks among multiple pets do not require one-at-a-time owner attention. Additionally, checking pet conflicts across all pets is inefficient and would make the algorithm slow and complicated. 

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I mainly used AI to help me design my UML diagram based on the classes and methods I needed for the app to function. I also used to to generate and debug code, as well as help with testing and verification.
- What kinds of prompts or questions were most helpful?
Prompts that were most helpful were prompts where I specified errors in the UI and code. For example, when the app did not perform in alerting the user of scheduling conflict, I let the AI know specifically that there was an issue regarding that and it immediately corrected it. I verified through testing. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
One time where I did not accept an AI suggestion was when it suggested that it makes numerous inheritance classes for the standard pet class. I did not want to overcomplicate the app and wanted to keep things simple, and wanted to give the user more freedom in inputting their pets. 
- How did you evaluate or verify what the AI suggested?
For every suggestion the AI made, I made sure it tested the suggestions and if they worked and enhanced the app, I followed through with them. If not, I simply asked the AI to revert the code back to before it made that suggestiong and started a new chat session to keep it focused so that it produced quality results.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
I tested scheduling, conflicted scheduling, having multiple pets, priority scheduling, and frequencies to make the experience optimal. 
- Why were these tests important?
These tests were important because they determined how the app was going to run and it also ensures there aren't any bugs and errors that could be caused by user input. Additionally, certain feautres like frequencies and priority scheduling could ensure users have an optimal and straightforward experience using the app.

**b. Confidence**

- How confident are you that your scheduler works correctly?
After multiple tests, I was fairly confident the scheduler worked correctly. 
- What edge cases would you test next if you had more time?
Some edge cases I would test if I had more time are time zone manipulation or daylight savings time change.
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I was very satisfied with the overall User Interface and the scheduler working well and passing thorough tests. I was also satisfied with the AI being able to construct json files where the app could recollect previous data in previous sections.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I would redesign the UI background so that it has the aesthetic of pets and not simply just a blank background with text boxes. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
One thing I learned is that it is an immensely helpful tool and can save so much time and energy from doing all the coding youreself. However, there are precautions that must be considered like keeping the AI focused and directed, and not blindly accepting what it outputs. The AI also can not verify and validate everything so that is left to the programmer.

## 6. Prompt Comparison
I asked ChatGPT and Claude both to complete the scheduling logic so I could compare the two. I found Claude's code to be fitting because it was short, simple and easy to read.