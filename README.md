# Artemis Junior

A classroom space mission for kids aged 7–12. It runs in any browser: a class screen plus one device per team. You can also play it on a single device. There are no accounts, no names and no typing, apart from the 4-character class code.

Six rounds; the teacher picks which ones to play (about 53 minutes for all six, including the intro and end):

| Round | Place | The trade-off kids face |
|---|---|---|
| 1 · Choose your Moon base | Moon | Sunlight, ice, landing room and Earth view all point to different sites. The site you pick also decides how much water you have later. |
| 2 · The Martian dust storm | Mars | 8 battery units for life support, food, heat and messages to Earth. Every setting costs something, and the storm lasts 2 or 3 days at random. |
| 3 · Solar storm emergency | Mars | One rover for three explorers, and it only runs if Round 2 left it 1 unit of battery. Then the class builds a radiation shelter from the bags it saved in Rounds 1 and 2. |
| 4 · Pack your space lunch | Moon | Apollo 12 foods: energy against bag space and water. |
| 5 · Solve the mystery | Mars | Teams combine clues to explain rounded pebbles found by Curiosity. |
| 6 · Gateway's water system | Moon orbit | Four team jobs: sort real water sources, choose one upgrade (recycle more or store more), share 2 L like NASA's daily minimums, and pick the safest water sample. |

Choices carry from round to round through two meters, Power and Supplies. Failing never ends the game: an "emergency help" screen explains what went wrong and offers Try again or Continue. At the end, the points from the rounds played add up to one mission score.

## NASA data used, and why

All values are copied into the game (labelled **Saved** in the app). They are listed on the in-app "Where our data comes from" screen.

| Dataset | Used for | Why |
|---|---|---|
| [Artemis III candidate landing regions](https://www.nasa.gov/news-release/nasa-provides-update-on-artemis-iii-moon-landing-regions/) | Round 1 sun and Earth visibility, slope, landing area | These are NASA's real candidate sites, so kids compare the same factors mission planners do. |
| [LRO Diviner temperatures](https://science.nasa.gov/wp-content/uploads/2024/01/lrolitho7temperaturevariation27may2014.pdf) | Round 1 water clue (25 K in a shadowed crater) | Shows why shadowed craters can keep ice. |
| [Opportunity and the 2018 dust storm (JPL)](https://www.jpl.nasa.gov/news/opportunity-hunkers-down-during-dust-storm/) | Round 2 story and reveal | A real power emergency on Mars, with real numbers. |
| Mars–Earth light time | Round 2 message delay (12 min average, about 3–22 min) | Shows why a Mars base can't wait for Earth in an emergency. |
| [DONKI](https://kauai.ccmc.gsfc.nasa.gov/DONKI/) (`2017-09-10T16:09:00-CME-001`, `2017-09-10T16:25:00-SEP-001`) | Round 3 solar storm | The September 10, 2017 event that Curiosity measured on Mars. |
| [Curiosity RAD](https://science.nasa.gov/photojournal/solar-storms-radiation-at-martian-orbit-and-surface/) | Round 3 alert | Radiation at the Mars surface during that storm. |
| [OSDR Environmental Data App](https://visualization.osdr.nasa.gov/eda/) (Rodent Research-1, 2014) | Round 3 reveal: about 0.2 mGy a day on the ISS, 7.96 mGy over 39 days | Real astronaut-environment radiation dose, so the shelter has a real number behind it. |
| [How NASA protects astronauts from radiation](https://science.nasa.gov/science-research/heliophysics/how-nasa-will-protect-astronauts-from-space-radiation-at-the-moon/) | Round 3 shelter rules and reveal | NASA's own shelter-from-supplies plan. |
| [Apollo 12 crew menu](https://science.nasa.gov/wp-content/uploads/2023/09/Apollo_12.pdf) | Round 4 foods | Real foods from a real Moon mission. |
| [Ancient streambed on Mars (2012)](https://science.nasa.gov/resource/remnants-of-ancient-streambed-on-mars/) | Round 5 clues and answer | Real evidence, reasoned through the way scientists did. |
| [CSA: Gateway](https://www.asc-csa.gc.ca/eng/astronomy/moon-exploration/gateway.asp) | Round 6 setting (crew of four, stays of up to three months) | A real station design that has to run its water while uncrewed. NASA paused Gateway in March 2026, and the game says so. |
| [NASA-STD-3001 Vol. 2, Table 6.3-1](https://www.nasa.gov/wp-content/uploads/2025/05/nasa-std-3001-vol-2.pdf) | Round 6 water sharing (2.5 L drinking and meals, 0.4 L hygiene) | NASA's own daily minimums for astronauts. |
| [ECLSS](https://www.nasa.gov/reference/environmental-control-and-life-support-systems-eclss/) and the ISS 98% recovery milestone | Round 6 water sources and upgrade | How the ISS really recycles urine, sweat and breath. |

The Round 1 Moon picture is an illustration. The real NASA region map appears beside it.

This is a student project for the NASA Space Apps Challenge. It is not an official NASA product, and it doesn't use NASA logos.

## Privacy

There are no accounts, names, chat or free-text answers. The server stores only the game state (class code, team choices and scores). That game is deleted after 3 hours without activity.

## How this repository fits together

- **The app (`src/`)** is the live game. It has the screens for the class screen and the team devices, plus its own built-in server: TanStack Start server functions in `src/lib/moon/room.functions.ts` that save each class's game in Postgres (Neon on Vercel). It deploys to Vercel as one project.
- **Round data (`nasa_backend/Data/round1.json` … `round6.json`)** is the single source of truth for every number in the game. The app reads these files directly (`src/lib/moon/game.ts`, `src/lib/moon/model.ts`). To change a number, edit the JSON. Screen wording stays in the components.
- **The Python backend (`nasa_backend/`)** is a reference version of the rules, with its own tests. It reads the same data files. The live app does not call it. It needs a WebSocket host, which Vercel cannot run, so it isn't deployed.
- **Rules tests:** `src/lib/moon/rules.test.ts` checks the app's rules against the shared data (ported from `nasa_backend/Tests`). Run them with `npm test`.

### Run it

```bash
npm install
npm run dev      # http://localhost:8080
npm test
```

## Where things live

- `nasa_backend/Data/*.json`: all round numbers (shared by the app and the Python backend)
- `src/lib/moon/model.ts`: Round 1 rules
- `src/lib/moon/game.ts`: rounds, meters and Rounds 2–5 rules
- `src/components/moon/Round2.tsx` … `Round6.tsx`: screens for each round
- `src/components/moon/Sources.tsx`: the in-app sources list
