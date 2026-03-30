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
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
