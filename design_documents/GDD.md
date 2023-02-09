# Game Design Document

The basis for the game is simple. It is a location based "cookie-clicker" based in the University of Exeter to incentivise recycling and the healthy habit of going outside.

---

## General Breakdown

The bounds of the playing area will be the University of Exeter's Streatham Campus. At the core of the game, you will be split into 3 teams (Red, Green, Blue) [Cooler names OTW].  

Each team will compete for territory that will increase their resource generation. That resource can then be used to upgrade their territories monster or used for buffs or debuffs.

How a team may acquire territory is by taking over a territory's monster. To take over a territories monster, you have to feed the trash to the Trashmuncher (trademark pending). In the physical location of the Trashmuncher there will be a recycling bin and upon recycling your trash, your team will be rewarded favor for that specific Trashmuncher.([Verification process in tech breakdown](./TDD.md))

Each Trashmuncher will have a public scoreboard of how much trash it has consumed by each team. The team with the most points (most trash recycled) will be the Trashmuncher's favourite. If the Trashmuncher belongs to your team, you will gain resources from it but in return it will consume the points you have gained from feeding it trash. The Trashmuncher will always "serve" the team that has the most points.

---

## Exploit Prevention

To preface, high effort exploits that are hardly reproducable will not be the main focus of this section. Instead this will focus on the simple player exploits we might face and how we will overcome them.

- Verification of users actually recycling: We will use a seemless multifactor authentication system that uses QR scanning, Video proof (elaborated on below) and GPS tracking. GDPR has been considered and the full breakdown on how the technology will work is [[here](./TDD.md)]

- Prevent users from "spam feeding" monsters: Implement a cooldown to how often a user can feed a monster. The drawbacks are limited due to the assumption that a user should be recycling all the trash they currently have in one go.

- TBD

---

## Known Design Problems
- Uses for resources (Potential buffs and debuffs? Personal mini-munchers?)
- TBD