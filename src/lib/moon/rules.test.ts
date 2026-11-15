// Rules tests for Rounds 1–5 (ported from nasa_backend/Tests so the live app is checked the same way).
// Run: npm test  (or: node --experimental-strip-types --test src/lib/moon/rules.test.ts)
import { test } from "node:test";
import assert from "node:assert/strict";
import * as G from "./game.ts";

test("round 1: site sets the water bags", () => {
  assert.deepEqual(G.WATER_BY_SITE.A, { thick: 1, wide: 2 });
  assert.deepEqual(G.WATER_BY_SITE.C, { thick: 1, wide: 1 });
  assert.deepEqual(G.WATER_BY_SITE.B, { thick: 0, wide: 1 });
});

test("round 2: energy, battery limit and survival", () => {
  assert.equal(G.START_POWER, 8);
  assert.equal(G.planTotal({ life: 2, food: 2, heat: 1, comms: 1 }), 6);
  let g = { ...G.newGame([2]) };
  g.r2 = { ...g.r2, stormDays: 2 };
  g = G.runDay(g, { life: 1, food: 1, heat: 1, comms: 2 });
  assert.equal(g.power, 3);
  assert.equal(g.r2.forecast, "long");
  assert.equal(g.r2.survived, 1);
  g = G.runDay({ ...g, stage: "plan", r2: { ...g.r2, day: 2 } }, { life: 1, food: 0, heat: 1, comms: 0 });
  assert.equal(g.scores["2"], 3);
  assert.equal(g.foodBag, false, "Food OFF eats the packed food bag");
  const fail = G.runDay({ ...G.newGame([2]) }, { life: 0, food: 1, heat: 1, comms: 0 });
  assert.equal(fail.scores["2"], 0);
  assert.equal(fail.r2.failedOn, 1);
});

test("round 2: try again restores the meters", () => {
  const fail = G.runDay({ ...G.newGame([2]) }, { life: 0, food: 2, heat: 2, comms: 2 });
  const again = G.retryRound(fail);
  assert.equal(again.power, 8);
  assert.equal(again.stage, "plan");
});

test("round 3: rescue needs rover battery", () => {
  let g = G.nextRound({ ...G.newGame([2, 3]), power: 1 });
  const far = (Object.entries(g.r3.times) as [string, [number, number]][]).find(([, p]) => p[0] === 11)![0];
  const ok = G.runRescue({ ...g, r3: { ...g.r3, rover: far as never } });
  assert.equal(ok.scores["3a"], 3);
  assert.equal(ok.power, 0);
  g = { ...g, power: 0 };
  const flat = G.runRescue({ ...g, r3: { ...g.r3, rover: far as never } });
  assert.equal(flat.scores["3a"], 2);
});

test("round 3: shelter points and best possible", () => {
  assert.equal(G.shelterPoints([{ obj: "thick", spot: "A" }, { obj: "wide", spot: "BC" }, { obj: "wide", spot: "BC" }]), 6);
  assert.equal(G.shelterPoints([{ obj: "empty", spot: "A" }, { obj: "clothing", spot: "AB" }, { obj: "wide", spot: "BC" }]), 4);
  assert.equal(G.bestShelter({ thick: 1, wide: 2, food: 1, clothing: 1, empty: 1 }), 6);
  assert.equal(G.bestShelter({ thick: 0, wide: 1, food: 0, clothing: 1, empty: 1 }), 4);
});

test("round 4: lunch limits", () => {
  const ids = (labels: string[]) => labels.map((l) => G.FOODS.find((f) => f.label.startsWith(l))!.id);
  assert.equal(G.lunchPoints(ids(["Chicken", "Spaghetti", "Beef", "Turkey", "Chocolate"])).points, 3);
  assert.equal(G.lunchPoints(ids(["Chicken", "Spaghetti", "Beef", "Chocolate"])).points, 1);
  assert.equal(G.lunchPoints(G.FOODS.map((f) => f.id)).points, 0);
});

test("round 5: hypothesis scoring", () => {
  assert.equal(G.mysteryPoints(G.CORRECT_CAUSE, ["shape", "size"]), 3);
  assert.equal(G.mysteryPoints("wind", ["size", "mars_cold"]), 1);
  assert.equal(G.mysteryPoints(G.CORRECT_CAUSE, ["stones_red", "mars_cold"]), 1);
  assert.equal(Object.keys(G.MYSTERY_CLUES).length, 4);
});

test("end of mission: score and stars", () => {
  const g = { ...G.newGame([1, 2, 3, 4, 5]), scores: { "1": 3, "2": 3, "3a": 3, "3b": 5, "4": 3, "5": 2 } };
  assert.deepEqual(G.missionTotals(g), { points: 19, max: 21, stars: 3 });
  const skip = G.newGame([3]);
  assert.equal(skip.power, 2, "skipped Round 2 leaves 2 battery units");
  assert.deepEqual(skip.water, G.WATER_BY_SITE.C, "skipped Round 1 uses site C");
});

test("round 6: Gateway water tasks", () => {
  const right = Object.fromEntries(G.WATER_CARDS.map((c) => [c.id, c.usedToday]));
  assert.equal(G.sortCorrect(right), true);
  assert.equal(G.sortCorrect({ ...right, comet: true }), false);
  assert.equal(G.WATER_CARDS.filter((c) => c.usedToday).length, 5);
  assert.equal(G.shareCorrect(17), true);
  assert.equal(G.shareCorrect(15), false);
  assert.deepEqual(G.sharePercents(), { drinking: 86, hygiene: 14 });
  assert.equal(G.sampleCorrect("A"), true);
  assert.equal(G.sampleCorrect("C"), false);
  const first = { tries: 1, correct: true, firstTry: true };
  const later = { tries: 2, correct: true, firstTry: false };
  assert.equal(G.round6Points({ energy: first, water: first, terrain: later, comms: first }), 2, "upgrade is a trade-off, not scored");
  assert.equal(G.SCORE_MAX["6"], 3);
  const g = { ...G.newGame([...G.ALL_ROUNDS]), scores: { "1": 3, "2": 3, "3a": 3, "3b": 6, "4": 3, "5": 3, "6": 3 } };
  assert.deepEqual(G.missionTotals(g), { points: 24, max: 24, stars: 3 });
});
