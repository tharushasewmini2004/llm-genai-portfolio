# Lab 2: AI in Everyday Challenges

**Module:** PUSL 3205 - Large Language Models and Generative AI
**Group 6:** The Plastic Problem
**Product:** BringIt, a campus app that rewards students for bringing their own cup, bottle, container or bag

## Objective
Use an LLM as a product-development partner to design a solution to an everyday student challenge. The deliverables are a product concept, name, key features, target user and a visual prototype.

## The challenge
Students regularly use single-use plastic items such as disposable cups, bottles, food containers and shopping bags. Many want to be more eco-friendly, but convenience often wins. The task is to design a product that makes reducing plastic waste easier and more attractive.

## Our solution: BringIt
BringIt rewards students each time they use their own reusable item at a partner canteen. Students scan a QR code to check in, earn points and streaks, fill a weekly goal and redeem rewards. An LLM-powered Eco Coach gives personalised tips and timely reminders.

![BringIt mock-up](mockup/bringit-mockup.png)

| Item | Summary |
|------|---------|
| Product name | BringIt |
| Target user | University students aged 18 to 25 |
| Key features | QR check-in, weekly goal and streaks, rewards, faculty leaderboard, Eco Coach |
| Prototype | `mockup/bringit-mockup.png` and `mockup/bringit-mockup.html` |

Full details are in [product-concept.md](product-concept.md).

## How the LLM was used
- **Understanding the problem:** broke the challenge into barriers (forgetting, inconvenience, no reward, no refill points, social pressure).
- **Brainstorming:** generated several concepts (borrow-and-return cups, a rewards app, a refill map, a foldable set, reminders, a loyalty pass) and compared them.
- **Defining the product:** combined the strongest ideas into BringIt and drafted the name, target user and features.
- **Building the prototype:** produced the HTML mock-up of the four app screens.
- **Presentation:** drafted the outline for the 2 to 3 minute talk.

The full list of prompts and what we changed is in [prompts-log.md](prompts-log.md).

## What we learned
- A specific, well-explained prompt gives much better results than a vague one.
- The LLM is good at generating options quickly, but the team still has to choose, check and refine the ideas.
- The LLM's output needs checking, for example reward values and how realistic partnerships with canteens are.

## Files
```
lab-02-everyday-challenges/
├── README.md
├── product-concept.md
├── prompts-log.md
└── mockup/
    ├── bringit-mockup.html
    └── bringit-mockup.png
```
