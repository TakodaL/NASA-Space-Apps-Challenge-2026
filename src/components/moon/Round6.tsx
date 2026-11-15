// Round 6 · Gateway's water recovery system. All numbers and text come from nasa_backend/Data/round6.json.
import { useState } from "react";
import { Check, Droplets } from "lucide-react";
import { play } from "@/lib/moon/audio";
import {
  GATEWAY,
  readAct,
  ROUND6_FINAL,
  round6Points,
  SAMPLE_GUIDE,
  SAMPLE_NOTE,
  sampleCorrect,
  SAMPLES,
  SHARE,
  shareCorrect,
  sharePercents,
  sortCorrect,
  UPGRADE_FACT,
  UPGRADE_PROBLEM,
  UPGRADES,
  WATER_CARDS,
  type GameState,
  type Round6Act,
  type SampleId,
  type UpgradeId,
} from "@/lib/moon/game";
import { TEAMS, TEAM_META, type RoomState, type TeamId } from "@/lib/moon/model";
import { sendAct, setGame } from "@/lib/moon/sync";
import { NextRoundButton, ReadCard, SpeakButton, WaitCard } from "@/components/moon/GameUI";
import { Button, Card, cn, Eyebrow } from "@/components/moon/ui";

const INTRO = `Gateway is a space station NASA designed to orbit the Moon. Up to ${GATEWAY.crew} astronauts could stay there for up to ${GATEWAY.maxStayMonths} months, and the water system must keep working even when the crew is away.`;

const TASK: Record<TeamId, string> = {
  energy: "Water sources",
  water: "Choose one upgrade",
  terrain: "Share the water",
  comms: "Choose the safest sample",
};

const actOf = (state: RoomState, t: TeamId) => readAct<Round6Act>(state.acts[t], "6");

function nextAct(prev: Round6Act | null, correct: boolean, extra: Partial<Round6Act>): Round6Act {
  const tries = (prev?.tries ?? 0) + 1;
  return { ...extra, tries, correct, firstTry: prev?.firstTry || (tries === 1 && correct) };
}

/* ---------------- class screen ---------------- */

export function Round6Main({ state, game }: { state: RoomState; game: GameState }) {
  const acts = Object.fromEntries(TEAMS.map((t) => [t, actOf(state, t)])) as Record<TeamId, Round6Act | null>;
  if (game.stage === "tasks")
    return (
      <div className="grid items-start gap-4 lg:grid-cols-[minmax(0,1.2fr)_minmax(18rem,0.8fr)]">
        <Card className="rise">
          <Eyebrow>Round 6 · Gateway's water system</Eyebrow>
          <div className="mt-1 flex items-start gap-3">
            <h2 className="flex-1 font-display text-3xl font-semibold">Gateway needs a water system</h2>
            <SpeakButton text={INTRO} />
          </div>
          <p className="mt-2 text-lg leading-relaxed text-muted">{INTRO}</p>
          <p className="mt-3 rounded-lg bg-bg/50 px-3 py-2 text-sm text-faint">{GATEWAY.status}</p>
          <p className="mt-4 text-sm text-muted">Each team has a different water job on its device.</p>
        </Card>
        <Card className="rise-2">
          <p className="font-display text-base font-semibold">Water recycling mission</p>
          <ul className="mt-2 grid gap-2 text-sm">
            {TEAMS.map((t) => {
              const a = acts[t];
              return (
                <li key={t} className="flex items-center justify-between gap-2 rounded-lg bg-bg/50 px-3 py-2">
                  <span>
                    <b>{TEAM_META[t].label}</b> · {TASK[t]}
                  </span>
                  <span className={a?.correct ? "text-good" : "text-faint"}>
                    {!a ? "Working…" : a.correct ? "Done" : `Try ${a.tries}: not yet`}
                  </span>
                </li>
              );
            })}
          </ul>
          <p className="mt-3 text-xs text-faint">No device for a team? Use the station buttons above to do its job here.</p>
          <Button
            className="mt-4"
            disabled={!Object.values(acts).some(Boolean)}
            onClick={() => {
              play("lock");
              setGame({ ...game, stage: "results", scores: { ...game.scores, "6": round6Points(acts) } });
            }}
          >
            Show the results
          </Button>
        </Card>
      </div>
    );

  const upgrade = acts.water?.choice as UpgradeId | undefined;
  const pct = sharePercents();
  return (
    <div className="grid gap-4">
      <div className="grid items-start gap-4 lg:grid-cols-2">
        <Card className="rise">
          <Eyebrow>Water sources · used by NASA today?</Eyebrow>
          <div className="mt-3 grid gap-3 sm:grid-cols-2">
            <div>
              <p className="font-display text-sm font-semibold text-good">Used by NASA today</p>
              <ul className="mt-2 grid gap-1.5 text-sm">
                {WATER_CARDS.filter((c) => c.usedToday).map((c) => (
                  <li key={c.id} className="rounded-lg bg-good/10 px-3 py-2">
                    <b>{c.label}</b>
                    <span className="block text-xs text-muted">{c.fact}</span>
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <p className="font-display text-sm font-semibold text-warn">Not used by NASA today</p>
              <ul className="mt-2 grid gap-1.5 text-sm">
                {WATER_CARDS.filter((c) => !c.usedToday).map((c) => (
                  <li key={c.id} className="rounded-lg bg-warn/10 px-3 py-2">
                    <b>{c.label}</b>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </Card>
        <Card className="rise-2">
          <Eyebrow>The upgrade</Eyebrow>
          {upgrade ? (
            <ReadCard title={`The class chose ${upgrade}: ${UPGRADES[upgrade].title}`} text={UPGRADES[upgrade].result} tone="accent" />
          ) : (
            <p className="mt-2 text-sm text-muted">No upgrade was chosen.</p>
          )}
          <p className="mt-3 text-sm leading-relaxed text-muted">{UPGRADE_FACT}</p>
          <div className="mt-4">
            <Eyebrow>Sharing the water</Eyebrow>
            <p className="mt-2 text-sm leading-relaxed">
              NASA's daily minimum for one astronaut: <b>{SHARE.dailyMinimumLitres.drinkingAndMeals} L</b> for drinking and meals and{" "}
              <b>{SHARE.dailyMinimumLitres.hygiene} L</b> for personal hygiene. That's about {pct.drinking}% and {pct.hygiene}%. In the game's 2 L:{" "}
              <b>{SHARE.correctUnits.drinkingAndMeals} units</b> and <b>{SHARE.correctUnits.hygiene} units</b>.
            </p>
            <p className="mt-1 text-xs text-faint">Source: {SHARE.source}.</p>
          </div>
          <div className="mt-4">
            <Eyebrow>The safest sample</Eyebrow>
            <p className="mt-2 text-sm">
              Sample A: {SAMPLES.A.result} {SAMPLE_NOTE}
            </p>
          </div>
        </Card>
      </div>
      <Card className="rise-3">
        <div className="flex items-start gap-3">
          <div className="flex-1">
            <p className="font-display text-xl font-semibold">{ROUND6_FINAL.message}</p>
            <p className="mt-2 text-base leading-relaxed text-muted">{ROUND6_FINAL.discussion}</p>
          </div>
          <SpeakButton text={`${ROUND6_FINAL.message} ${ROUND6_FINAL.discussion}`} />
        </div>
        <p className="mt-3 text-sm">
          Round 6 points: <b>{game.scores["6"] ?? 0} / 3</b> (one for each task done right on the first try).
        </p>
        <div className="mt-4">
          <NextRoundButton game={game} />
        </div>
      </Card>
    </div>
  );
}

/* ---------------- team devices ---------------- */

export function Round6Team({ state, game, team }: { state: RoomState; game: GameState; team: TeamId }) {
  const prev = actOf(state, team);
  if (game.stage !== "tasks") return <WaitCard text="The class screen is showing the results." />;
  return (
    <Card className="rise mx-auto w-full max-w-xl">
      <Eyebrow>
        {TEAM_META[team].label} · {TASK[team]}
      </Eyebrow>
      <div className="mt-3">
        {team === "energy" && <SortTask team={team} prev={prev} />}
        {team === "water" && <UpgradeTask team={team} prev={prev} />}
        {team === "terrain" && <ShareTask team={team} prev={prev} />}
        {team === "comms" && <SampleTask team={team} prev={prev} />}
      </div>
    </Card>
  );
}

function Feedback({ prev, ok, notOk }: { prev: Round6Act | null; ok: string; notOk: string }) {
  if (!prev) return null;
  return (
    <p className={cn("mt-3 rounded-lg px-3 py-2 text-sm", prev.correct ? "bg-good/15 text-good" : "bg-warn/15 text-warn")}>
      {prev.correct ? ok : notOk}
    </p>
  );
}

function SortTask({ team, prev }: { team: TeamId; prev: Round6Act | null }) {
  const [sorted, setSorted] = useState<Record<string, boolean>>(prev?.sorted ?? {});
  const all = WATER_CARDS.every((c) => sorted[c.id] !== undefined);
  return (
    <div>
      <ReadCard
        title="Which water sources does NASA use today, and which not?"
        text="Put each card in a group: Used by NASA today, or Not used by NASA today. Then press Submit."
      />
      <ul className="mt-3 grid gap-2">
        {WATER_CARDS.map((c) => (
          <li key={c.id} className="rounded-2xl bg-bg/50 px-3 py-2">
            <p className="font-display text-sm font-semibold">{c.label}</p>
            <div className="mt-2 grid grid-cols-2 gap-2">
              {[true, false].map((used) => (
                <button
                  key={String(used)}
                  type="button"
                  aria-pressed={sorted[c.id] === used}
                  onClick={() => {
                    play("tap");
                    setSorted({ ...sorted, [c.id]: used });
                  }}
                  className={cn(
                    "min-h-11 rounded-lg px-2 text-xs font-semibold transition-transform active:scale-[0.97]",
                    sorted[c.id] === used ? (used ? "bg-good text-bg" : "bg-warn text-bg") : "bg-surface-2 text-muted",
                  )}
                >
                  {used ? "Used by NASA today" : "Not used today"}
                </button>
              ))}
            </div>
          </li>
        ))}
      </ul>
      <Button
        className="mt-4 w-full"
        disabled={!all}
        onClick={() => {
          const ok = sortCorrect(sorted);
          play(ok ? "lock" : "nope");
          sendAct(team, "6", nextAct(prev, ok, { sorted }));
        }}
      >
        Submit
      </Button>
      <Feedback prev={prev} ok="All the cards are in the right group!" notOk="Some cards are in the wrong group. Talk it over and try again." />
    </div>
  );
}

function UpgradeTask({ team, prev }: { team: TeamId; prev: Round6Act | null }) {
  const [pick, setPick] = useState<UpgradeId | null>((prev?.choice as UpgradeId) ?? null);
  const sent = prev?.choice as UpgradeId | undefined;
  return (
    <div>
      <ReadCard title="You have room for one upgrade. What should the station add?" text={UPGRADE_PROBLEM} />
      <div className="mt-3 grid gap-2">
        {(Object.keys(UPGRADES) as UpgradeId[]).map((id) => (
          <button
            key={id}
            type="button"
            aria-pressed={pick === id}
            onClick={() => {
              play("tap");
              setPick(id);
            }}
            className={cn("rounded-2xl px-4 py-3 text-left transition-transform active:scale-[0.98]", pick === id ? "bg-accent/15 ring-2 ring-accent" : "bg-bg/50")}
          >
            <span className="font-display text-base font-semibold">
              {id} · {UPGRADES[id].title}
            </span>
            <span className="mt-1 block text-sm text-muted">{UPGRADES[id].card}</span>
          </button>
        ))}
      </div>
      <Button
        className="mt-4 w-full"
        disabled={!pick}
        onClick={() => {
          if (!pick) return;
          play("send");
          sendAct(team, "6", { tries: (prev?.tries ?? 0) + 1, correct: true, firstTry: false, choice: pick });
        }}
      >
        Submit
      </Button>
      {sent && (
        <div className="mt-3">
          <ReadCard title={`You chose ${sent}: ${UPGRADES[sent].title}`} text={UPGRADES[sent].result} tone="accent" />
        </div>
      )}
    </div>
  );
}

function ShareTask({ team, prev }: { team: TeamId; prev: Round6Act | null }) {
  const total = SHARE.totalUnits;
  const [drink, setDrink] = useState<number>(prev?.drinking ?? Math.round(total / 2));
  const hyg = total - drink;
  const litres = (u: number) => (u * SHARE.litresPerUnit).toFixed(1);
  const pct = sharePercents();
  return (
    <div>
      <ReadCard
        title="Share the water"
        text={`You have ${litres(total)} litres of water (${total} units of ${SHARE.litresPerUnit} L). Share the units between Drinking and meals and Personal hygiene. Then press Submit to compare your plan with NASA's daily minimums for one astronaut. Your ${litres(total)} L is less than one astronaut needs in a day, so this task is about how to split the water, not how much there is.`}
      />
      <div className="mt-3 grid grid-cols-10 gap-1.5" role="img" aria-label={`${drink} units for drinking and meals, ${hyg} units for hygiene`}>
        {Array.from({ length: total }, (_, i) => (
          <Droplets key={i} className={cn("size-6", i < drink ? "text-accent" : "text-warn")} aria-hidden />
        ))}
      </div>
      <div className="mt-3 grid grid-cols-2 gap-3">
        <Stepper label="Drinking and meals" value={drink} litres={litres(drink)} onMinus={() => setDrink(Math.max(0, drink - 1))} onPlus={() => setDrink(Math.min(total, drink + 1))} tone="text-accent" />
        <Stepper label="Personal hygiene" value={hyg} litres={litres(hyg)} onMinus={() => setDrink(Math.min(total, drink + 1))} onPlus={() => setDrink(Math.max(0, drink - 1))} tone="text-warn" />
      </div>
      <Button
        className="mt-4 w-full"
        onClick={() => {
          const ok = shareCorrect(drink);
          play(ok ? "lock" : "nope");
          sendAct(team, "6", nextAct(prev, ok, { drinking: drink }));
        }}
      >
        Submit
      </Button>
      <Feedback
        prev={prev}
        ok="You matched NASA's proportions! Drinking and meals need most of the water."
        notOk="Compare your split with NASA's proportions and try again."
      />
      {prev && (
        <p className="mt-2 text-xs leading-relaxed text-muted">
          NASA's daily minimums for one astronaut: drinking and meals {SHARE.dailyMinimumLitres.drinkingAndMeals} L (about {pct.drinking}%), personal
          hygiene {SHARE.dailyMinimumLitres.hygiene} L (about {pct.hygiene}%).
        </p>
      )}
    </div>
  );
}

function Stepper({ label, value, litres, onMinus, onPlus, tone }: { label: string; value: number; litres: string; onMinus: () => void; onPlus: () => void; tone: string }) {
  return (
    <div className="rounded-2xl bg-bg/50 p-3 text-center">
      <p className="text-sm">{label}</p>
      <p className={cn("font-display text-3xl font-semibold tabular-nums", tone)}>{value}</p>
      <p className="text-xs text-muted">{litres} L</p>
      <div className="mt-2 flex justify-center gap-2">
        <button type="button" aria-label={`Less for ${label}`} onClick={() => { play("tap"); onMinus(); }} className="size-11 rounded-full bg-surface-2 font-display text-xl">
          −
        </button>
        <button type="button" aria-label={`More for ${label}`} onClick={() => { play("tap"); onPlus(); }} className="size-11 rounded-full bg-surface-2 font-display text-xl">
          +
        </button>
      </div>
    </div>
  );
}

function SampleTask({ team, prev }: { team: TeamId; prev: Round6Act | null }) {
  const [pick, setPick] = useState<SampleId | null>((prev?.choice as SampleId) ?? null);
  return (
    <div>
      <ReadCard title="Choose the safest water sample to send to the crew" text={SAMPLE_GUIDE.join(" ")} />
      <div className="mt-3 grid gap-2">
        {(Object.keys(SAMPLES) as SampleId[]).map((id) => {
          const s = SAMPLES[id];
          return (
            <button
              key={id}
              type="button"
              aria-pressed={pick === id}
              onClick={() => {
                play("tap");
                setPick(id);
              }}
              className={cn("rounded-2xl px-4 py-3 text-left transition-transform active:scale-[0.98]", pick === id ? "bg-accent/15 ring-2 ring-accent" : "bg-bg/50")}
            >
              <span className="font-display text-base font-semibold">Sample {id}</span>
              <span className="mt-2 flex flex-wrap items-center gap-1" aria-label={`Water, ${s.minerals} useful ${s.minerals === 1 ? "mineral" : "minerals"}, ${s.unknown} unknown ${s.unknown === 1 ? "particle" : "particles"}`}>
                <Droplets className="size-5 text-accent" aria-hidden />
                {Array.from({ length: s.minerals }, (_, i) => (
                  <span key={`m${i}`} className="size-3.5 rounded-full bg-good" aria-hidden />
                ))}
                {Array.from({ length: s.unknown }, (_, i) => (
                  <span key={`u${i}`} className="size-3.5 rotate-45 bg-warn" aria-hidden />
                ))}
              </span>
              <span className="mt-1 block text-xs text-muted">
                {s.minerals} useful {s.minerals === 1 ? "mineral" : "minerals"} · {s.unknown} unknown {s.unknown === 1 ? "particle" : "particles"}
              </span>
            </button>
          );
        })}
      </div>
      <p className="mt-2 flex items-center gap-3 text-xs text-faint">
        <span className="inline-flex items-center gap-1"><span className="size-3 rounded-full bg-good" /> useful minerals</span>
        <span className="inline-flex items-center gap-1"><span className="size-3 rotate-45 bg-warn" /> unknown particles</span>
      </p>
      <Button
        className="mt-4 w-full"
        disabled={!pick}
        onClick={() => {
          if (!pick) return;
          const ok = sampleCorrect(pick);
          play(ok ? "lock" : "nope");
          sendAct(team, "6", nextAct(prev, ok, { choice: pick }));
        }}
      >
        Submit
      </Button>
      {prev?.choice && (
        <p className={cn("mt-3 flex items-start gap-2 rounded-lg px-3 py-2 text-sm", prev.correct ? "bg-good/15 text-good" : "bg-warn/15 text-warn")}>
          {prev.correct && <Check className="mt-0.5 size-4 shrink-0" aria-hidden />}
          Sample {prev.choice}: {SAMPLES[prev.choice as SampleId].result} {prev.correct ? "" : "Try again."}
        </p>
      )}
    </div>
  );
}
