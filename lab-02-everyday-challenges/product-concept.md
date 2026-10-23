# BringIt: Product Concept

**Tagline:** Bring your own. Get rewarded.

## The problem
Students use disposable cups, bottles, food containers and shopping bags every day. Most of them want to be more eco-friendly, but convenience wins. The barrier is not awareness. It is friction: they forget the reusable item, nothing rewards them for remembering, and nobody around them is doing it.

## The product
**BringIt** is a mobile app for university campuses. Students check in at partner canteens and shops each time they bring their own cup, bottle, container or bag. Every check-in earns points, builds a daily streak and adds to a weekly goal. Points are redeemed for discounts and free items at the same canteens.

The idea: make the plastic-free choice the easy and rewarding one, instead of asking students to rely on willpower.

## Target user
University students aged 18 to 25 who care about the environment but have busy days, move between lectures, labs and the canteen, and often forget or skip reusable items.

**Example persona (Nimali, 2nd-year student):** wants to cut plastic, but forgets her cup on morning lecture days and sees no benefit in remembering. A small reward and a friendly reminder would change her habit.

## Key features
1. **Check-in by QR code.** Scan the code at a partner canteen when you bring your own cup, bottle, container or bag. Each check-in earns points.
2. **Weekly cup and streaks.** A cup on the home screen fills up as you complete plastic-free days, which makes progress visible and keeps students coming back.
3. **Rewards.** Redeem points for a free coffee, a lunch discount or other perks from partner canteens.
4. **Faculty leaderboard.** Faculties compete monthly, which adds friendly social pressure.
5. **Eco Coach (LLM-powered).** A chat assistant that gives personalised tips, writes a weekly impact summary, and sends reminders based on a student's habits and timetable, such as "pack your cup before your 9:00 lecture".
6. **Today checklist.** A simple list of bottle, cup, container and bag, so students see what they still need to bring.

## How the LLM adds value
- Turns raw check-in data into friendly, personal advice.
- Suggests easy swaps for single-use items based on what the student actually buys.
- Writes short, motivating weekly summaries.
- Helps the team during development (see `prompts-log.md`).

## What makes it different
Many eco apps only teach or track. BringIt connects the habit to an immediate, local reward at the places students already visit every day.

## Possible challenges
- Canteens must agree to join and fund the discounts.
- Check-ins could be faked, so the canteen staff may need to confirm them.
- The Eco Coach needs clear limits so its advice stays accurate and relevant.

## Prototype
See `mockup/bringit-mockup.png` (and the interactive `mockup/bringit-mockup.html`). The mock-up shows four screens: Home, Check in, Rewards and Eco Coach. All names, points and rankings are sample data.
