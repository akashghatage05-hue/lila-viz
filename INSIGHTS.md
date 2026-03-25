# INSIGHTS — LILA BLACK Player Journey Analysis

---

## Insight 1: AmbroseValley Dominates Play Time — But May Be Crowding Out Other Maps

### What caught my eye
AmbroseValley accounts for 566 matches out of 796 total (71%). GrandRift has 
only 59 matches (7.4%) and Lockdown 171 (21.5%). This is not a small gap — 
AmbroseValley gets nearly 10x more matches than GrandRift.

### The evidence
| Map | Matches | % of Total | Human Position Events |
|-----|---------|------------|----------------------|
| AmbroseValley | 566 | 71% | 36,189 |
| Lockdown | 171 | 21.5% | 11,418 |
| GrandRift | 59 | 7.4% | 3,740 |

When you look at the visualization with "All dates" selected and switch between 
maps, AmbroseValley is densely covered with player paths while GrandRift looks 
sparse — entire sections of the map have almost no player traffic at all.

### Why a level designer should care
GrandRift's low play rate could mean one of two things: players are actively 
avoiding it (bad sign — suggests the map has design problems), or it's simply 
not being surfaced enough in matchmaking rotation. Either way, the level design 
team needs to investigate. If players are avoiding it, heatmaps on GrandRift 
will reveal which zones specifically feel dead or unengaging.

### Actionable items
- **Metric to track:** Map selection rate per session — are players dodging 
  GrandRift when given a choice?
- **Action 1:** Run a heatmap analysis specifically on GrandRift to identify 
  dead zones where no player ever travels
- **Action 2:** Compare loot density across maps — GrandRift's 880 loot events 
  vs AmbroseValley's 9,955 suggests loot may be too sparse to reward exploration
- **Action 3:** Consider whether GrandRift's layout naturally funnels players 
  into fewer paths, reducing replayability

---

## Insight 2: Players Are Looters First, Fighters Second — PvP Is Nearly Absent

### What caught my eye
There are only 3 human-vs-human kills across the entire 5-day dataset. 
Meanwhile there are 2,415 bot kills and 12,885 loot events. Players are 
spending their time looting and fighting bots — not each other.

### The evidence
| Event Type | Count | % of Combat Events |
|------------|-------|--------------------|
| Loot | 12,885 | — |
| BotKill (human kills bot) | 2,415 | 99.9% |
| Kill (human kills human) | 3 | 0.1% |
| KilledByStorm | 39 | — |

The loot-to-PvP ratio is staggering: for every 1 human kill, there are 
4,295 loot pickups. Even accounting for this being an extraction shooter 
where looting is core, near-zero PvP suggests players either aren't 
encountering each other or are actively avoiding fights.

The average match has only 1.0 human player — meaning most matches are 
essentially solo runs against bots. This directly explains the PvP drought.

### Why a level designer should care
If the game is designed around tense PvP extraction moments but matches 
rarely have more than one human, the core tension loop is broken. Players 
are getting a PvE experience by default. Map design decisions — like 
chokepoints, extraction zone placement, and loot concentration — that were 
built to create PvP pressure are currently untested in real conditions.

### Actionable items
- **Metric to track:** Average human players per match over time — is this 
  a player count problem or a map design problem?
- **Action 1:** Concentrate high-value loot near extraction zones to force 
  human players into the same areas — increasing encounter probability 
  without changing matchmaking
- **Action 2:** Review chokepoint design — if humans can complete a full 
  run without crossing another player's likely path, the map layout may 
  need forced convergence zones
- **Action 3:** Use the traffic heatmap to identify if human paths on 
  AmbroseValley ever naturally intersect — if they don't, the map may be 
  too wide for current player counts

---

## Insight 3: The Storm Is Not a Meaningful Threat — Especially on AmbroseValley

### What caught my eye
Only 39 players died to the storm across 796 matches over 5 days. That's 
a 4.9% storm death rate per match. On AmbroseValley specifically, the 
loot-to-storm-death ratio is 585 — meaning players pick up 585 items for 
every one storm death. The storm is barely registering as a threat.

### The evidence
| Map | Storm Deaths | Matches | Deaths/Match | Loot:Storm Ratio |
|-----|-------------|---------|--------------|-----------------|
| AmbroseValley | 17 | 566 | 0.03 | 585:1 |
| Lockdown | 17 | 171 | 0.10 | 120:1 |
| GrandRift | 5 | 59 | 0.08 | 176:1 |

Lockdown has the highest storm death rate (0.10 per match) — 3x higher 
than AmbroseValley. This makes sense for a smaller, close-quarters map 
where the storm closes faster relative to map size.

### Why a level designer should care
The storm is the primary pacing mechanic in extraction shooters — it's 
supposed to compress the play space, force decisions, and create urgency. 
If players are dying to it less than once every 30 matches on AmbroseValley, 
it's not fulfilling that role. Players may be extracting too easily, 
looting without time pressure, or the storm moves too slowly relative to 
map size.

### Actionable items
- **Metric to track:** Average time-to-extraction per match — are players 
  extracting early and comfortably, or cutting it close?
- **Action 1:** Use the storm death heatmap to see *where* on the map 
  players are dying to the storm — if all deaths cluster near one edge, 
  the storm origin point may be too predictable
- **Action 2:** Consider tightening the storm timing on AmbroseValley 
  specifically — it's the largest and most played map, yet has the lowest 
  storm pressure per match
- **Action 3:** Compare Lockdown's storm parameters to AmbroseValley — 
  Lockdown's 3x higher storm death rate suggests its pacing creates more 
  tension, which could inform a AmbroseValley redesign
```

---

Save it, then push:
```
git add INSIGHTS.md
git commit -m "Add insights doc"
git push
