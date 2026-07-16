# Changelog

All notable changes to **Z1 Dojo** will be documented in this file.

This project follows a milestone-based development process rather than feature dumps. Each version represents meaningful progress toward creating a complete training environment for *The Legend of Zelda* (NES) and Zelda 1 Randomizer players.

--
## [0.0.22] - 20260716132052 - Dynamic Enemy Graphics Foundation



## [0.0.21] - 20260714085724 - Full-Arena Spawn Pool

### Added

* Added randomized enemy spawn positions for the Z1 Dojo combat room.
* Added a full-arena pool containing 84 interior spawn candidates.
* Added support for placing all eight configured enemies on every room entry.
* Added randomized starting positions and randomized traversal through the spawn pool.
* Added unique-position validation so two enemies cannot begin on the same cell.
* Added arena-aware collision validation using the selected room’s actual collision data.
* Added a strict initial placement pass using Zelda’s normal terrain and Link-distance checks.
* Added a fallback placement pass that retains terrain safety while using a smaller safety zone around Link.
* Added a spawn-failure state for detecting configurations that cannot be placed safely.
* Added stable runtime variables for the full-arena placement system:

  * `$06F4` — current candidate index
  * `$06F5` — traversal step
  * `$06F6` — attempts remaining
  * `$06F7` — current enemy object slot
  * `$06F8` — candidate X coordinate
  * `$06F9` — candidate Y coordinate
  * `$06FA` — spawn-failure state

### Changed

* Replaced Zelda’s original nine-position Dojo placement system with an 84-cell interior spawn pool.
* Enemy positions are now regenerated whenever the player enters the combat room.
* The same enemy configuration now produces different combat arrangements between attempts.
* Spawn candidates are validated against the currently selected arena instead of relying only on a small fixed list.
* Enemy placement no longer silently reduces `RoomObjCount` when the first available positions are unsuitable.
* All configured enemies must receive valid positions.
* Regular enemy encounters now retain their complete configured count of up to eight enemies.
* Normal non-Dojo Zelda rooms continue using the original direction-based spawn-position tables.

### Fixed

* Fixed combat encounters occasionally spawning only three, six, or another incomplete number of configured enemies.
* Fixed the limited nine-cell system failing to find enough valid positions in restrictive arena geometries.
* Fixed the possibility of two enemies receiving the same starting coordinate.
* Fixed enemy placement becoming predictable after repeated room entries.
* Fixed deleted references to Zelda’s original `SpawnPosListAddrsLo` and `SpawnPosListAddrsHi` tables.
* Removed leftover code from the abandoned nine-cell traversal implementation.
* Fixed undefined symbols caused by missing full-arena constants, tables, and runtime variables.

### Technical

* Added `DojoFullArenaSpawnCells`, containing 84 packed row-and-column candidates.
* Added `DojoFullArenaSpawnSteps`, containing traversal increments that visit every candidate before repeating.
* Added a randomized strict traversal pass.
* Added a deterministic fallback traversal pass.
* Added helper routines for:

  * initializing randomized traversal;
  * initializing fallback traversal;
  * converting packed cells into object coordinates;
  * checking position uniqueness;
  * accepting a valid candidate;
  * advancing through the pool;
  * testing terrain safety;
  * testing relaxed Link distance.
* Preserved Zelda’s existing `IsSafeToSpawn` behavior during the strict placement pass.
* Preserved collision validation during fallback placement.
* Kept `RoomObjCount` unchanged throughout placement.
* Added `DOJO_SPAWN_FAILURE` at `$06FA`:

  * `$00` means every configured enemy was placed successfully.
  * `$01` means the selected encounter could not be completely placed.
* Verified `$06FA` remains `$00` with eight active enemies across all curated arenas.

### Verified Arenas

Eight-enemy randomized placement was tested successfully in:

* Blank
* 4 Short
* 4 Tall
* Maze
* Grid
* Chevy
* NSU
* Single 6

### Current Test Encounter

* Slot 1: Stalfos
* Slot 2: Blue Keese
* Slot 3: Stalfos
* Slot 4: Blue Keese
* Slot 5: Stalfos
* Slot 6: Blue Keese
* Slot 7: Stalfos
* Slot 8: Blue Keese

All eight enemies spawn in unique, randomized, arena-safe positions on every room entry.

### Design Rules Confirmed

* Regular combat mode supports up to eight enemies.
* Regular enemies must use randomized safe starting positions.
* Encounters must not become predictable through fixed placement.
* Boss mode will be developed separately after the regular combat zone is complete.
* Boss encounters will allow exactly one dungeon boss with no regular enemies.
* Dodongo encounters may allow up to three Dodongos as a special exception.


## [0.0.20] - 20260712035228 - First Combat Drill

Added
Added configurable combat encounters for the fixed Z1 Dojo combat room at $63.
Added support for up to eight regular enemy slots.
Added mixed enemy groups instead of requiring every enemy to use the same type.
Added DOJO_ENEMY_NONE entries for unused configuration slots.
Added automatic enemy counting.
Added automatic slot compaction so NONE entries may appear anywhere in the configuration table.
Added support for empty combat drills with zero active enemies.
Added automatic encounter reset whenever the player leaves and re-enters the combat room.
Added enemy constants for:
Stalfos
Blue Keese
Gibdo
Added the first working mixed combat drill using two Stalfos and two Blue Keese.
Changed
Replaced the original repeated-enemy override with an eight-slot enemy configuration table.
Z1 Dojo now populates Zelda’s individual object-type slots directly.
Enemy count is derived from the configured non-empty slots instead of being maintained manually.
Active enemies are compacted into consecutive object slots before the original spawn-position logic runs.
Enemy placement continues to use Zelda’s normal game-controlled spawn system.
The combat room’s enemy configuration remains independent from:
Arena geometry
Door configuration
Player loadout
Moved temporary Z1 Dojo runtime state from game-owned RAM at $0516–$0520 to stable RAM at $06F0–$06F3.
Fixed
Fixed enemies appearing inside the HUD because the calculated enemy count was tested using stale processor flags after STY.
Fixed the selected arena resetting to Blank when entering the combat room.
Fixed arena state being overwritten during room transitions.
Fixed Select+Up and Select+Down also cycling the B-button item.
Fixed encounters failing or behaving incorrectly after leaving and re-entering the combat room.
Fixed empty configuration slots producing broken or invisible objects.
Technical
Added DojoCombatEnemySlots, an eight-byte encounter configuration table.
Added automatic scanning of all eight configuration entries.
Added compaction of active enemies into ObjType+1 through ObjType+8.
Added automatic calculation of RoomObjCount.
Preserved Zelda’s original object-template and safe-spawn-position logic.
Added carry-based signaling from ApplyDojoCombatEnemyConfig:
Carry clear uses the original room configuration.
Carry set uses the Z1 Dojo custom encounter.
Assigned stable runtime state addresses:
$06F0 — selected arena
$06F1 — Select-control state
$06F2 — previous arena
$06F3 — banner timer
Current Test Encounter
Slot 1: Stalfos
Slot 2: None
Slot 3: Blue Keese
Slot 4: None
Slot 5: Stalfos
Slot 6: Blue Keese
Slot 7: None
Slot 8: None

The resulting encounter contains two Stalfos and two Blue Keese.

## [0.0.19] - 20260711182054 - Runtime Arena Selection

Added
Added runtime-selectable combat arena geometry.
Added a curated list of eight player-facing arenas:
Blank
4 Short
4 Tall
Maze
Grid
Chevy
NSU
Single 6
Added validation for the runtime arena selection.
Added automatic fallback to 4 Short when the selected arena value is invalid.
Added temporary lobby controls for testing arena selection:
Hold Select and press Down to select the next arena.
Hold Select and press Up to select the previous arena.
Press Select by itself to cycle through available B-button items.
Added support for the starting boomerang loadout so B-item cycling can be tested.
Added a two-line lobby notification banner when the arena changes.
Added dynamic previous-arena and new-arena names to the banner.
Added an approximately 1.5-second banner timer.
Added automatic restoration of the original lobby graphics after the banner disappears.
Added immediate banner cleanup when leaving the lobby.
Changed
Arena geometry is now selected at runtime instead of being limited to a compile-time constant.
The selected geometry continues to use the fixed combat-room slot at room $63.
Arena geometry remains independent from combat-room door configuration.
Arena selection wraps from the final arena back to Blank and from Blank back to the final arena.
Arena changes no longer play a confirmation sound.
Temporary Select-based controls consume directional input so Link does not move while changing arenas.
Added a direction-release lock intended to reduce repeated arena changes from a single directional press.
Technical
Added DOJO_SELECTED_PLAYABLE_ARENA at $0516.
Added DOJO_SELECT_MODIFIER_STATE at $0517.
Added DOJO_PREVIOUS_PLAYABLE_ARENA at $0518.
Added DOJO_ARENA_BANNER_TIMER at $0520.
Added a playable-arena-to-geometry mapping table.
Added fixed-width eight-tile arena-name records for notification rendering.
Added dynamic PPU transfer-buffer generation for the two-line lobby banner.
Added row-by-row restoration using the game’s existing room-row rendering system.
Preserved the existing geometry safety metadata and fallback behavior.
Kept Chevy selectable while retaining its future ladder-requirement metadata.
Kept Turnstyle excluded from the player-facing arena list because it depends on special push-block room behavior.
Notes
The Select-based arena controls and notification banner are temporary development tools.
Occasional imperfect arena stepping may still occur with rapid controller input. This is acceptable for the temporary testing interface and will be replaced by the permanent Z1 Dojo setup menu.
Enemy configuration and spawning are not included in this release.

## [0.0.18] - 20260711173155 - Curated Playable Arena List

Added
Added a curated player-facing combat-arena list.
Added separate player-facing arena selection indexes.
Added DojoPlayableArenaGeometries, which maps approved arena choices to entries in the complete internal geometry catalog.
Added a fallback player-facing arena for invalid curated selections.
Added the following initial playable arenas:
Blank
4 Short
4 Tall
Maze
Grid
Chevy
NSU
Single 6
Changed
Player-facing arena selection no longer directly references raw Zelda geometry IDs.
The complete technical geometry catalog remains available internally for research and documentation.
Noncombat and special-purpose geometries are excluded from the normal playable-arena list.
Plain geometry is presented to the player as the canonical Blank arena.
Black geometry is not exposed because it is functionally redundant with Blank for normal combat practice.
ApplyDojoCombatGeometry now resolves selections through the curated playable-arena table.
Invalid player-facing selections now fall back safely to 4 Short.
The internal metadata safety check remains active after the curated lookup.
Excluded Geometries

The curated list intentionally excludes geometries that are unsuitable for general combat practice, including:

Turnstyle
Level 1 entrance/lobby
Zelda’s room
Ganon’s room
Triforce room
fireball-shooter rooms
other boss, traversal, or special-purpose layouts

These geometries remain documented in the complete internal catalog and may be used by specialized training modes later.

Selection Architecture

The arena-selection path is now:

Player-facing arena index
        ↓
DojoPlayableArenaGeometries
        ↓
Internal geometry catalog index
        ↓
DojoGeometryIds
        ↓
Raw Zelda underworld geometry
        ↓
Fixed combat slot $63

This keeps the player-facing list independent from Zelda’s raw room-layout numbering.

Confirmed Behavior

The following selections were tested successfully:

4 Short
Maze
Blank

For each selection:

the physical combat room remained $63,
the selected geometry appeared correctly,
only the south combat-room doorway remained open,
returning to lobby $73 worked,
lobby colors remained correct,
and repeated visits retained the same selection.

Invalid curated selection $08 correctly fell back to 4 Short.

Milestone

Version 0.0.18 establishes the initial player-safe arena-selection layer that the future Z1 Dojo setup menu will control.

## [0.0.17] - 20260711171901 - Arena Metadata and Safety Fallback

Added
Added one metadata byte for every named arena geometry.
Added metadata flags for:
currently selectable arenas
boss-shaped arenas
built-in fireball shooters
special-purpose rooms
geometries requiring special doorway behavior
Added a configurable fallback arena through DOJO_FALLBACK_GEOMETRY.
Added catalog-range validation before loading a selected arena.
Added metadata-based safety validation before applying arena geometry.
Changed
ApplyDojoCombatGeometry now validates the selected catalog index before reading the geometry table.
Out-of-range geometry selections now fall back safely to 4 Short.
Arena entries without the selectable flag now fall back safely to 4 Short.
Turnstyle remains cataloged but is temporarily blocked from normal selection because its doorway requirements have not yet been implemented.
Metadata Flags

Each arena receives a metadata byte using the following flags:

Bit	Purpose
0	Selectable with the current combat-room system
1	Boss-shaped arena
2	Contains built-in fireball shooters
3	Special-purpose room
4	Requires special doorway or room behavior

Flags can be combined so one arena can belong to multiple categories.

Safety Fallback

The current fallback is:

DOJO_FALLBACK_GEOMETRY := DOJO_GEOMETRY_4_SHORT

The loading path is now:

Configured selection
        ↓
Check catalog range
        ↓
Read arena metadata
        ↓
Check SELECTABLE flag
        ↓
Load selected arena or fall back to 4 Short
Confirmed Behavior

The following tests were completed successfully:

4 Short loaded normally.
Maze loaded normally.
Turnstyle fell back to 4 Short.
Invalid catalog index $2A fell back to 4 Short.
The lobby-to-combat-room loop remained functional.
The combat room remained physical room $63.
Lobby colors remained correct.
No invalid room graphics or crashes occurred during fallback testing.
Milestone

Version 0.0.17 introduces the safety and metadata layer required before arena choices are exposed through a player-facing menu.

## [0.0.16] - 20260711153027 - Named Arena Catalog

Added
Added a permanent named combat-arena geometry catalog.
Cataloged all verified Zelda 1 underworld geometries from $00 through $29.
Added named geometry constants for standard rooms, boss rooms, moat rooms, stair rooms, special rooms, and hazard rooms.
Added direct lookup of verified raw geometry IDs through DojoGeometryIds.
Added DOJO_GEOMETRY_COUNT with 42 valid catalog entries.
Changed
Replaced the temporary three-entry source-room catalog with a complete direct geometry-ID catalog.
Removed the temporary geometry scanner and its $06FF RAM probe.
Removed scanner initialization and automatic geometry advancement.
Geometry selection now remains stable between repeated lobby-to-combat-room visits.
The combat room continues to use physical room $63, regardless of the selected geometry.
Verified Geometry Range

Valid underworld geometry data was confirmed from:

$00 through $29

Values $2A and above produced corrupted graphics or crashes and are not treated as valid underworld geometry.

Special Geometry Notes
$20 is Turnstyle geometry.
Turnstyle appears to require appropriate doorway or room-behavior configuration and is not yet considered a normal menu-ready arena.
$23 is the two-fireball-shooter room, distinct from the block-only two-fireball geometry at $0A.
Boss and special rooms remain cataloged, but may later require metadata or restrictions before being exposed in the arena-selection menu.
Confirmed Behavior

The permanent catalog was tested with multiple named geometries, including:

4 Short
Maze
Single 6
Level 1 entrance geometry

For each tested geometry:

the physical room remained $63,
the map moved only one room north and south,
the combat room retained its independent south-only doorway layout,
returning to the lobby worked,
lobby colors remained correct,
and the selected geometry remained stable between visits.
Milestone

Version 0.0.16 establishes the permanent named arena catalog that future setup menus will use.

## [0.0.15] - 20260711150729 - Fixed Combat Slot with Selectable Geometry

Added
Added a fixed physical combat-room slot at Level 1 room $63.
Added independent combat-arena geometry selection.
Added geometry selection IDs for three initial test layouts:
Level 1 entrance room $73
Level 1 north room $63
Level 1 two-north room $53
Added DojoGeometrySourceRooms, which maps geometry selection IDs to source room IDs.
Added ApplyDojoCombatGeometry, which copies a selected room’s unique underworld layout ID into the fixed combat slot.
Changed
Combat arena selection no longer changes the physical destination room.
The lobby now connects normally to the adjacent combat slot:
Lobby $73 north to combat slot $63
Combat slot $63 south to lobby $73
Removed the need to jump two dungeon rows when loading a selected arena.
Preserved the combat slot’s map position, door configuration, enemies, and upper room-attribute bits while replacing only its interior geometry.
Combat geometry is now applied before the independent combat-door configuration and before the destination room is drawn.
Geometry Attribute Handling

The lower six bits of LevelBlockAttrsD identify the unique underworld room layout.

ApplyDojoCombatGeometry:

Reads the selected source room from DojoGeometrySourceRooms.
Extracts the source room’s lower-six-bit geometry ID.
Preserves the combat slot’s upper two attribute bits.
Writes the combined value into the fixed combat slot.

Conceptually:

Selected geometry ID
        ↓
Source room lookup table
        ↓
Source room layout bits 0–5
        +
Combat slot bits 6–7
        ↓
Combat slot $63
Confirmed Geometry Selections

All three initial geometry selections were successfully tested.

Entrance Geometry
DOJO_STARTING_GEOMETRY := DOJO_GEOMETRY_L1_ENTRANCE
Physical room remained $63.
Interior geometry was borrowed from room $73.
Map position and lobby return remained correct.
Original Combat-Slot Geometry
DOJO_STARTING_GEOMETRY := DOJO_GEOMETRY_L1_NORTH
Physical room remained $63.
Room $63 used its original geometry.
Independent combat doors remained active.
Two-North Geometry
DOJO_STARTING_GEOMETRY := DOJO_GEOMETRY_L1_TWO_NORTH
Physical room remained $63.
Interior geometry was borrowed from room $53.
The map still moved only one room north and south.
Confirmed Separation

Changing the selected geometry did not change:

the physical combat room ID,
the dungeon map location,
the safe doorway configuration,
the combat slot’s original enemy assignment,
the lobby’s appearance,
or the lobby-to-combat return loop.
Milestone

Version 0.0.15 establishes the fixed-combat-slot architecture.

Z1 Dojo can now place different arena interiors into one safe, adjacent combat location without moving Link to unrelated dungeon coordinates.

## [0.0.14] - 20260711135608 - Separate Lobby and Combat-Room Configuration

Added
Added separate doorway configurations for the safe lobby and the selected combat room.
Added a reusable door-attribute packing routine that accepts four temporary door-type values.
Added dedicated routines for:
applying the fixed lobby door layout
applying the selected combat-room door layout
Added combat-room configuration during the lobby-to-arena scrolling transition.
Added normal Zelda room-layout handling for all transitions that do not originate from the Dojo lobby.
Changed
Replaced the single global door configuration with independent lobby and combat-room settings.
Updated initial dungeon loading so only the safe lobby receives the lobby doorway layout.
Updated upward room scrolling so the redirected destination receives the selected combat-room doorway layout before Zelda draws it.
Preserved normal room-transition behavior outside the Dojo lobby.
Converted the original local @CheckDark label into a normal label so it remains accessible after the new global transition labels.
Preserved normal shutter, bombable-wall, and walk-through-wall behavior inside the redirected combat arena.
Lobby Configuration

The lobby uses a fixed safe layout:

Side	Type
North	Open
East	Wall
South	Wall
West	Wall

This keeps the player inside the lobby while leaving the north entrance available for beginning a combat attempt.

Combat-Room Test Configuration

The redirected combat room was configured with four different doorway behaviors:

Side	Type
North	Shutter
East	Bombable wall
South	Open
West	Walk-through wall

This deliberately mixed layout was used to confirm that the destination room received the combat configuration rather than its original ROM-defined door layout.

Confirmed Behavior

All configured combat-room doorway behaviors were successfully tested.

North Shutter
Began closed.
Opened after every enemy in the combat room was defeated.
Used Zelda’s normal shutter-opening behavior.
East Bombable Wall
Appeared as an ordinary wall, as expected in Zelda 1.
Opened when bombed.
Consumed one bomb.
Used Zelda’s normal bomb-hole behavior.
South Open Doorway
Rendered as an open passage.
Allowed Link to enter the redirected combat room normally.
West Walk-Through Wall
Appeared as an ordinary wall.
Allowed Link to pass after pushing against it for approximately two seconds.
Used Zelda’s normal Second Quest walk-through-wall behavior.
Door-Configuration Architecture

The lobby and combat room now provide their door types to one shared packing routine.

Conceptually:

Lobby door values
        ↓
ApplyDojoLobbyDoorConfig
        ↓
ApplyDojoDoorConfigFromTemps

and:

Combat door values
        ↓
ApplyDojoCombatDoorConfig
        ↓
ApplyDojoDoorConfigFromTemps

The shared routine packs:

south and north into LevelBlockAttrsA
east and west into LevelBlockAttrsB

while preserving each room’s original palette bits.

Transition-Time Application

During an upward room transition, Zelda temporarily installs NextRoomId as RoomId so it can lay out the destination.

Z1 Dojo now checks whether:

the source room is the Dojo lobby,
the current level is the Dojo lobby level,
and the transition is the northward lobby exit.

When those conditions match:

Temporarily install selected combat RoomId
        ↓
Apply combat-room doorway configuration
        ↓
Lay out the selected combat room
        ↓
Restore the lobby RoomId until scrolling finishes

All other upward transitions use Zelda’s normal destination-layout path.

Development Issue Resolved

The combat-room configuration routine initially existed but was never called from the upward-scroll path.

A temporary RAM marker at $06FF confirmed whether the routine executed. After the call was inserted correctly, the selected doorway layout appeared and all behaviors worked.

The diagnostic marker was removed after testing.

Milestone

Version 0.0.14 establishes independent lobby and combat-room configuration.

Z1 Dojo can now:

maintain a fixed safe lobby,
redirect the lobby to a selected combat arena,
apply a separate doorway layout to that arena,
preserve the selected door behaviors,
and leave unrelated Zelda room transitions unchanged.

This is the first version where the lobby and combat arena operate as two distinct parts of one configurable training flow.

## [0.0.13] - 20260711131149 - Lobby Arena Redirection

Added
Added lobby-to-combat-arena room redirection.
Added a third confirmed development arena:
Level 1 room $53
Added named constants for the Dojo lobby level and room.
Added named constants for the currently selected test combat arena.
Added Z1 Dojo branding to the dungeon status bar.
Changed
Changed the lobby’s south side from an open exit to a solid wall.
Prevented players from leaving the dungeon through the lobby’s southern boundary.
Intercepted the lobby’s northward room transition.
Replaced Zelda’s normally adjacent destination with the selected combat-room destination.
Replaced the dungeon status-bar text LEVEL-1 with Z1-DOJO.
Removed the original behavior that replaced the final status-bar character with the current dungeon number.
Lobby Door Configuration

The lobby now uses:

Side	Door type
North	Open
East	Wall
South	Wall
West	Wall

Link can still initially enter the lobby through the south side because direct room initialization bypasses normal doorway traversal.

After Link gains control, the south side behaves as a solid wall and prevents the player from attempting to leave the dungeon.

Normal Zelda Destination

The lobby is Level 1 room $73.

Under Zelda’s normal dungeon-grid calculation, moving north produces:

$73 - $10 = $63

Before this milestone, the lobby’s north doorway always led to room $63.

Redirected Destination

The test combat arena was changed to Level 1 room $53.

When Link leaves the lobby through the north doorway, Z1 Dojo now checks:

Is the current level the Dojo lobby level?
Is the current room the Dojo lobby room?
Is Link moving north?

When all conditions are true, Z1 Dojo replaces NextRoomId with the selected combat-room ID.

The confirmed flow is:

Lobby room $73
      ↓ north exit
Redirected combat room $53

Reaching $53 instead of the naturally adjacent $63 confirms that the transition is genuinely redirected.

Transition Variables
Address	Variable	Purpose
$00E7	Transition direction	Direction used to calculate the next room
$00EB	RoomId	Current room
$00EC	NextRoomId	Destination room

For a northward lobby exit:

Transition direction = $08
RoomId before scroll = $73
NextRoomId during scroll = $53
RoomId after scroll = $53
Status-Bar Branding

The original dungeon heading:

LEVEL-1

was replaced with:

Z1-DOJO

Both strings contain seven characters, so the new heading fits the original transfer-buffer length.

The original code replaced the final character with the current dungeon number. That write was removed so the final O remains intact.

Current Limitations

The redirect currently changes only the destination room.

The selected combat arena still uses its original ROM-defined:

door layout,
room geometry,
enemies,
room triggers,
and other attributes.

The custom door configuration is currently applied during initial room loading and therefore configures the lobby rather than the redirected combat room.

Future work will distinguish lobby configuration from combat-arena configuration and apply the selected setup after the lobby transition.

Milestone

Version 0.0.13 establishes arbitrary lobby-to-arena redirection.

Z1 Dojo can now:

begin in a safe lobby,
prevent the player from exiting south,
detect the lobby’s north exit,
redirect that exit to a selected nonadjacent room,
preserve normal Zelda room scrolling,
and display Z1 Dojo branding in the dungeon interface.

This is the first step toward allowing the permanent lobby to lead to any player-selected combat arena.

## [0.0.12] - 20260711055124 - Safe Combat Lobby Foundation

Added
Added the first safe combat-lobby flow.
Added named development references for:
the lobby arena
the test combat arena
Configured Level 1 room $73 as the initial development lobby.
Configured Level 1 room $63 as the adjacent test combat room.
Added a preparation phase before combat begins.
Changed
Updated the active starting arena so Z1 Dojo begins in the lobby instead of directly inside a combat room.
Configured the lobby with:
an open north doorway
an open south doorway
solid east and west walls
Preserved south-side dungeon entry so Link walks naturally into the lobby.
Kept enemies out of the initial preparation room.
Allowed Zelda’s normal room-transition and enemy-spawning systems to begin combat only after Link enters the room to the north.
Confirmed Lobby Flow

The following sequence was successfully tested:

Start Z1 Dojo
      ↓
Enter Level 1 room $73 from the south
      ↓
Prepare safely in the lobby
      ↓
Walk through the north doorway
      ↓
Enter Level 1 room $63
      ↓
Room $63 enemies spawn normally
Confirmed Room Values
Purpose	Level	Room
Safe lobby	$01	$73
Test combat room	$01	$63

When Z1 Dojo starts:

CurLevel = $01
RoomId   = $73

After Link passes through the north doorway and the room transition completes:

CurLevel = $01
RoomId   = $63
Lobby Door Configuration
Side	Door type
North	Open
East	Wall
South	Open
West	Wall

The north exit leads naturally to room $63 because that room is physically located north of room $73 in Level 1’s dungeon map.

Combat Timing

Enemies are not active while Link is in the lobby.

The combat-room enemies are created only after Link:

chooses to enter through the north doorway,
completes the room transition,
and arrives in room $63.

This establishes the intended Z1 Dojo rhythm:

Configure
   ↓
Prepare
   ↓
Enter when ready
   ↓
Fight
Current Limitations

The lobby currently relies on Zelda’s original dungeon adjacency.

The north doorway of room $73 naturally leads to room $63. It cannot yet redirect to an arbitrary selected arena.

The following are planned for later milestones:

redirecting the lobby exit to the selected arena
applying the selected arena geometry after leaving the lobby
applying the selected entry side
applying configured door types to the combat room rather than the lobby
spawning a player-selected enemy roster
returning to the lobby after reset or victory
opening the lobby’s north door through a deliberate start sequence
Milestone

Version 0.0.12 establishes the safe combat-lobby foundation.

Z1 Dojo now provides a safe preparation room and allows the player to decide when combat begins by entering the room to the north.

This is the first complete gameplay flow that resembles the intended finished combat-training experience.

## [0.0.11] - 20260711052649 - Unknown Door-Type Research

Added
Researched the remaining dungeon door-type values $02, $03, and $06.
Confirmed that door values $02 and $03 both behave as Second Quest walk-through walls.
Confirmed that door value $06 behaves like the standard locked key door.
Added clearer internal names for the duplicate original door encodings.
Walk-Through Wall Behavior

Door values $02 and $03 were tested independently.

Both values produced the same observed behavior:

Property	Result
Appearance	Ordinary dungeon wall
Passage method	Push against the wall
Time before passage	Approximately two seconds
Key required	No
Bomb required	No
Door animation	None
Room transition	Normal transition into adjacent room

These are the walk-through walls primarily associated with Second Quest dungeon layouts.

The wall does not visually open. Link pushes through it and enters the adjacent room.

Adjacent-Room Door Appearance

After passing through a north walk-through wall, a visible doorway appeared on the south side of the destination room.

This does not mean the walk-through wall transformed into a normal door.

Z1 Dojo currently overrides the doorway attributes only for the initially loaded arena. The adjacent room continues using its original ROM-defined doorway configuration.

Duplicate Walk-Through Values

Both original values are retained internally:

DOJO_DOOR_TYPE_WALK_THROUGH_WALL   := $02
DOJO_DOOR_TYPE_WALK_THROUGH_WALL_2 := $03

No behavioral difference was observed during testing.

Z1 Dojo will use $02 as its canonical walk-through-wall value and expose only one walk-through-wall option in the eventual setup menu.

Alternate Key-Door Value

Door value $06 was tested using normal dungeon keys.

Its behavior matched door value $05:

Property	Result
Appearance	Locked key door
Opens with a normal key	Confirmed
Keys consumed	One
Opening animation	Normal
Opened-door bit updated	Confirmed
Remained open after returning	Confirmed

Both original values are retained internally:

DOJO_DOOR_TYPE_KEY   := $05
DOJO_DOOR_TYPE_KEY_2 := $06

Z1 Dojo will use $05 as its canonical locked-door value and expose only one locked-door option in the eventual setup menu.

User-Facing Door Types

Based on all completed door research, the eventual combat setup menu needs these distinct choices:

Open
Solid wall
Walk-through wall
Bombable wall
Locked door
Shutter door

An already-open bomb hole is represented by combining:

door type: Bombable
starts open: Yes

The duplicate original encodings $03 and $06 do not require separate user-facing menu options.

Milestone

Version 0.0.11 completes the initial identification of Zelda’s eight dungeon door-type values.

Z1 Dojo now understands which original values represent distinct player-facing behaviors and which values appear to be duplicate encodings.

## [0.0.10] - 20260711045632 - Bombable Walls

Added
Added functional bombable-wall support to configurable dungeon arenas.
Added support for beginning with a bombable passage already open.
Added independent starting-open configuration for:
north doorway
east doorway
south doorway
west doorway
Added named opened-door bit constants for all four room sides.
Added configured bomb and maximum-bomb application after the selected save inventory is loaded.
Changed
Applied configured bomb counts after Zelda copies the selected save file’s inventory into active RAM.
Extended the configurable door system so visible door type and initial opened state are controlled separately.
Reused Zelda’s original bomb-wall opening, animation, bomb consumption, and persistence systems.
Preserved opened passages when leaving and returning to the room during the same session.
Bombable-Wall Behavior

A closed north bombable wall was tested using Zelda’s normal bomb behavior.

Unlike later Zelda games, bombable walls in the original Legend of Zelda have no special visible markings. A closed bombable wall appears like an ordinary dungeon wall.

Confirmed results:

Test	Result
Wall appeared as an ordinary wall	Confirmed
Bomb could open the passage	Confirmed
Bomb count decreased from 8 to 7	Confirmed
Bomb-hole animation played	Confirmed
Opened-door state changed from $00 to $08	Confirmed
Passage remained open after leaving and returning	Confirmed
Opened-Door State

Opened dungeon doors and bomb holes use the CurOpenedDoors bit field:

CurOpenedDoors = $00EE

The four side bits are represented as:

Side	Bit
East	$01
West	$02
South	$04
North	$08

A north bomb hole therefore changes:

$00 → $08

All four bits together produce:

$01 | $02 | $04 | $08 = $0F
Starting With an Open Bomb Hole

Door type and initial opened state are now separate properties.

A closed bombable wall uses:

DOJO_NORTH_DOOR_TYPE       := DOJO_DOOR_TYPE_BOMBABLE
DOJO_NORTH_DOOR_START_OPEN := 0

This requires the player to use a bomb.

An already-open bomb passage uses:

DOJO_NORTH_DOOR_TYPE       := DOJO_DOOR_TYPE_BOMBABLE
DOJO_NORTH_DOOR_START_OPEN := 1

This causes the passage to be open immediately when the room loads:

no bomb is consumed,
no explosion is required,
and no opening animation is played.
Four-Side Test

All four sides were configured as bombable and set to begin open:

DOJO_NORTH_DOOR_TYPE := DOJO_DOOR_TYPE_BOMBABLE
DOJO_EAST_DOOR_TYPE  := DOJO_DOOR_TYPE_BOMBABLE
DOJO_SOUTH_DOOR_TYPE := DOJO_DOOR_TYPE_BOMBABLE
DOJO_WEST_DOOR_TYPE  := DOJO_DOOR_TYPE_BOMBABLE

DOJO_NORTH_DOOR_START_OPEN := 1
DOJO_EAST_DOOR_START_OPEN  := 1
DOJO_SOUTH_DOOR_START_OPEN := 1
DOJO_WEST_DOOR_START_OPEN  := 1

Results:

north bomb hole began open,
east bomb hole began open,
south bomb hole began open,
west bomb hole began open,
and all four passages were usable without consuming bombs.
Technical Flow
Apply configured door types
        ↓
Apply configured starting-open bits
        ↓
Lay out room graphics and collision
        ↓
Closed bombable wall:
    wait for normal bomb interaction
        ↓
Open bomb hole:
    use existing CurOpenedDoors state
Current Implementation

Starting-open values are currently compile-time configuration constants.

The future Z1 Dojo menu will store the four selected door types and four starting-open values in the active combat setup.

Saved and shared combat setups will preserve both properties independently.

Milestone

Version 0.0.10 establishes configurable bombable walls and bomb holes.

Z1 Dojo can now create arenas containing:

closed bombable walls,
pre-opened bomb passages,
independent bomb-hole states on all four sides,
normal bomb consumption,
normal opening animation,
and persistent opened passages.

This supports bomb-hole entry practice, bomb-wall combat strategies, and arena configurations that begin with selected passages already accessible.

## [0.0.9] - 20260711040757 - Door Behavior Verification

Added
Connected configured key doors to Zelda’s original key-consumption and opened-door systems.
Connected configured shutter doors to Zelda’s original room-clear trigger system.
Added automatic all-enemies-defeated trigger configuration when one or more custom shutter doors are present.
Added configured starting-key application after the selected save file’s inventory is copied into active RAM.
Added support for multiple configured shutters opening together after combat is completed.
Changed
Moved the configured starting-key assignment to the correct point in the save-loading sequence.
Updated custom room attribute F so rooms with configured shutters use Zelda’s normal all-enemies-defeated secret trigger.
Updated the cached LevelBlockAttrsByteF value after Z1 Dojo modifies the active room’s trigger attributes.
Preserved Zelda’s original door-opening animations and room-clear behavior rather than creating a separate custom shutter system.
Key-Door Behavior

A configured north key door was tested with one starting key.

Results:

Test	Result
Key door displayed correctly	Confirmed
Door opened normally	Confirmed
Key count decreased from 1 to 0	Confirmed
Door remained open after leaving and returning	Confirmed
Opened-door state changed	$00 to $08

The north opened-door flag is therefore:

North opened-door bit = $08

The opened-door state is stored in:

CurOpenedDoors = $00EE
Starting-Key Load Order

The first starting-key implementation was applied before Zelda copied the selected save file’s inventory into active RAM.

That later copy overwrote the configured key count with the value stored in the save file.

The key assignment is now performed after the inventory-copy loop:

LDA #DOJO_STARTING_KEYS
STA InvKeys

Testing with:

DOJO_STARTING_KEYS := 5

correctly produced five starting keys.

This location will later become part of the central player-selected loadout application routine.

Shutter-Door Trigger

Changing a door’s visible type to shutter was not sufficient to make it open after combat.

Zelda also checks the room’s secret-trigger value stored in the low three bits of LevelBlockAttrsF.

Z1 Dojo now sets those bits to:

$01 = all enemies defeated

whenever at least one configured shutter is present.

The upper five bits of LevelBlockAttrsF are preserved.

The modified attribute is also copied into:

LevelBlockAttrsByteF

because Zelda caches that byte before normal gameplay begins.

Confirmed Shutter Tests

Each doorway was independently configured as a shutter and tested.

Side	Opened after all enemies were defeated
North	Confirmed
East	Confirmed
South	Confirmed
West	Confirmed

A room with all four sides configured as shutters was also tested.

After the final enemy was defeated:

all four shutters opened,
Zelda’s normal opening behavior was used,
and no custom animation or replacement door logic was required.
Technical Flow
Apply configured door types
        ↓
Detect whether any configured side is a shutter
        ↓
Set room trigger to “all enemies defeated”
        ↓
Update cached room-trigger attributes
        ↓
Spawn and fight enemies
        ↓
Final enemy is defeated
        ↓
Zelda’s original shutter logic opens all shutters
Special Cases

Zelda’s room has special behavior tied to Ganon’s defeat. That exception should remain intact and will be researched separately when the Ganon training system is developed.

Current Limitations

The following door behaviors remain for future milestones:

bombable walls
already-open bomb holes
false walls
alternate key-door behavior
alternate false-wall behavior
explicit door-hiding starts
Khananakey setup and reset behavior
restoration of door state when restarting a combat setup
Milestone

Version 0.0.9 establishes functional key and shutter door behavior.

Configured doors now participate in Zelda’s real gameplay systems rather than only changing their appearance.

Z1 Dojo can now create combat arenas with:

working locked doors,
normal key consumption,
persistent opened-key-door state,
working shutters on any side,
multiple simultaneous shutters,
and normal enemy-clear opening behavior.

## [0.0.8] - 20260711034757 - Configurable Door States

Added
Added the first configurable dungeon-door system.
Added named constants for Zelda’s eight three-bit door-type values:
open
wall
false wall
alternate false wall
bombable wall
key door
alternate key door
shutter door
Added independent door-type configuration for:
north
east
south
west
Added ApplyDojoDoorConfig, which applies the selected door types to the active dungeon room before its graphics and collision are laid out.
Changed
Updated initial dungeon-room setup so Z1 Dojo can override the original room’s four doorway attributes.
Preserved each room’s original low palette bits while replacing only the six bits that describe its door types.
Kept door configuration independent from:
arena geometry
entry side
enemies
player loadout
Door Attribute Layout

Dungeon door types are stored in two room-attribute bytes.

LevelBlockAttrsA
Bits	Purpose
0–1	Room palette information
2–4	South door type
5–7	North door type
LevelBlockAttrsB
Bits	Purpose
0–1	Room palette information
2–4	East door type
5–7	West door type

Z1 Dojo preserves bits 0–1 and replaces the selected door fields.

Door-Type Values
Value	Named type
$00	Open
$01	Wall
$02	False wall
$03	Alternate false wall
$04	Bombable
$05	Key
$06	Alternate key
$07	Shutter

The exact gameplay differences between the two false-wall values and the two key-door values still require further research.

Confirmed Test 1

The selected arena was configured with:

DOJO_NORTH_DOOR_TYPE := DOJO_DOOR_TYPE_OPEN
DOJO_EAST_DOOR_TYPE  := DOJO_DOOR_TYPE_WALL
DOJO_SOUTH_DOOR_TYPE := DOJO_DOOR_TYPE_OPEN
DOJO_WEST_DOOR_TYPE  := DOJO_DOOR_TYPE_WALL

Results:

Side	Expected	Result
North	Open	Confirmed
East	Wall	Confirmed
South	Open	Confirmed
West	Wall	Confirmed
Confirmed Test 2

The north side was changed to:

DOJO_NORTH_DOOR_TYPE := DOJO_DOOR_TYPE_KEY

Result:

The north doorway displayed as a locked key door.
The other three sides retained their configured types.
Changing one side did not incorrectly alter another side.
Technical Notes

The door configuration is applied before LayOutRoom runs:

Select dungeon and room
        ↓
Apply configured door attributes
        ↓
Lay out room graphics and collision
        ↓
Position Link and begin gameplay

This ensures the room is initially drawn using the configured doorway layout rather than its original ROM-defined doors.

Current Limitations

This milestone confirms door-type encoding and independent four-side selection.

The following behavior is not yet fully tested:

opening and consuming a key door
shutter opening and closing
bombable-wall destruction
beginning with an already opened bomb hole
false-wall traversal
preserving or resetting opened-door state
victory-triggered shutter behavior
door-hiding starts
Khananakey behavior

Those systems may depend on additional opened-door flags and room-transition state beyond the visible door-type attributes.

Milestone

Version 0.0.8 establishes the configurable door-type foundation.

Z1 Dojo can now combine:

a selected arena
an independently selected entry side
independently selected north, east, south, and west door types

This provides the room-configuration foundation needed for door hiding, locked-door strategies, bomb-hole entry, shutter behavior, and other combat-specific practice conditions.

## [0.0.7] - 20260711032329 - Configurable Dungeon Entry

Added
Added independently configurable dungeon entry directions.
Added named entry-side constants:
ENTRY_FROM_NORTH
ENTRY_FROM_EAST
ENTRY_FROM_SOUTH
ENTRY_FROM_WEST
Added separate coordinate definitions for:
vertical doorway alignment
horizontal doorway alignment
north-edge entry
south-edge entry
Added entry-direction handling that automatically positions Link at the appropriate room edge.
Added support for entering the same arena from any of its four sides.
Changed
Replaced the single fixed dungeon-entry position with direction-aware placement.
Separated arena selection from entry-side selection.
Removed the requirement to manually configure X and Y coordinates for each entry-side test.
Updated direct dungeon loading to reproduce the edge placement normally established by Zelda’s room-scrolling system.
Entry Direction Values

ObjDir describes the direction Link moves into the room. The physical entry side is the opposite side.

Entry side	Link movement	ObjDir
West	Right	$01
East	Left	$02
North	Down	$04
South	Up	$08
Entry Coordinates

Horizontal and vertical entries require different coordinate handling.

North Entry
Link is horizontally centered.
Link begins near the top edge.
Link moves downward into the room.
X = $78
Y = $3D
Direction = $04
South Entry
Link is horizontally centered.
Link begins near the bottom edge.
Link moves upward into the room.
X = $78
Y = $DD
Direction = $08
West Entry
Link uses the configured horizontal doorway lane.
Zelda’s room-entry routine places him at the left edge.
Link moves right into the room.
Y = $8D
Direction = $01
East Entry
Link uses the configured horizontal doorway lane.
Zelda’s room-entry routine places him at the right edge.
Link moves left into the room.
Y = $8D
Direction = $02
Technical Discovery

Direct dungeon-room loading skips the normal scrolling sequence that ordinarily places Link at the appropriate vertical edge.

For horizontal entries, Zelda’s existing room-entry routine automatically replaces Link’s X coordinate with the appropriate left or right edge value.

For vertical entries, the routine does not replace Link’s Y coordinate. Z1 Dojo therefore supplies the edge coordinate directly:

North entry: $3D
South entry: $DD

The dungeon’s normal internal movement boundaries remain:

Boundary	Value
Left	$21
Right	$D0
Top	$5E
Bottom	$BD

The entry coordinates intentionally begin outside those internal boundaries so Link can walk through the doorway and into the playable room area.

Door Independence

All four entry directions worked even when the selected room did not contain a visible doorway on the chosen side.

This confirms that initial entry placement and visible door geometry are separate systems.

Future Z1 Dojo combat setups can therefore configure these properties independently:

arena geometry
entry side
north door type
east door type
south door type
west door type
Confirmed Tests

The same selected arena was successfully loaded using all four entry directions:

North
East
South
West

Each direction placed Link at the corresponding room edge and moved him inward correctly.

Milestone

Version 0.0.7 establishes configurable dungeon entry.

Z1 Dojo can now combine:

a selected arena ID
a selected dungeon level and room
an independently selected entry side
correct direction-aware starting coordinates

This provides the entry system needed for the future combat lobby, door-hiding practice, bomb-hole starts, locked-door strategies, and configurable doorway conditions.

## [0.0.6] - 20260711030623 - Arena Definition System

Added
Added the first Z1 Dojo arena-definition system.
Added named arena IDs:
DOJO_ARENA_L1_ENTRANCE
DOJO_ARENA_L1_NORTH
Added DOJO_ARENA_COUNT to record the current number of defined arenas.
Added DOJO_STARTING_ARENA as the active development-arena selection.
Added parallel arena lookup tables for:
dungeon level
dungeon room
Added two confirmed development arenas:
Arena ID	Level	Room
Level 1 Entrance	$01	$73
Level 1 North Room	$01	$63
Changed
Replaced direct starting-level and starting-room constants with an arena-ID lookup.
Updated the gameplay-launch routine so it reads the selected arena’s level and room from the arena tables.
Preserved the save-slot index while the arena lookup temporarily uses the X register.
Removed the temporary forced starting key used to discover the room north of the Level 1 entrance.
Restored the configured starting key count to zero.
Technical Notes

The active arena is selected using:

DOJO_STARTING_ARENA := DOJO_ARENA_L1_NORTH

The selected arena ID is used as the index into matching tables:

DojoArenaLevels:
    .BYTE WORLD_LEVEL_1
    .BYTE WORLD_LEVEL_1

DojoArenaRooms:
    .BYTE $73
    .BYTE $63

Each position across the tables represents one arena record.

For example, arena $01 reads:

level $01 from DojoArenaLevels
room $63 from DojoArenaRooms

The menu-launch routine then stores those values in:

CurLevel
CaveSourceRoomId

The controlled dungeon-loading system introduced in v0.0.5 handles the rest of the transition.

Confirmed Tests

Both defined arena IDs were tested successfully.

Level 1 Entrance
DOJO_STARTING_ARENA := DOJO_ARENA_L1_ENTRANCE

Result:

Property	Value
CurLevel	$01
RoomId	$73
Level 1 North Room
DOJO_STARTING_ARENA := DOJO_ARENA_L1_NORTH

Result:

Property	Value
CurLevel	$01
RoomId	$63

Changing only DOJO_STARTING_ARENA reliably switched between the two rooms.

Current Limitations

The first arena records contain only:

dungeon level
room ID

Future arena definitions will add independently configurable information such as:

named room geometry
safe entry position
entry direction
north, east, south, and west door types
palette or visual variant
lobby and combat-room roles

Enemy selection and player loadout will remain separate from arena selection.

Milestone

Version 0.0.6 establishes the arena abstraction layer.

Z1 Dojo no longer needs to hardcode a starting level and room for each test. It can now select an arena by ID and resolve that arena into the correct dungeon location.

This is the foundation for the eventual visual arena-selection menu and saved, shareable combat configurations.

## [0.0.5] - 20260711021138 -  Controlled Dungeon Loading

Added
Added controlled dungeon selection through DOJO_STARTING_LEVEL.
Added support for starting in a dungeon rather than always beginning on the overworld.
Added WORLD_LEVEL_1 as a named level constant.
Added ROOM_USE_LEVEL_DEFAULT to allow a dungeon to use its original entrance room.
Added separate initial-spawn behavior for overworld and dungeon starts.
Documented Level 1’s entrance room ID as $73.
Changed
Updated initial room selection so CaveSourceRoomId can be used for both overworld and dungeon starts.
Removed the original restriction that forced every dungeon start to use LevelInfo_StartRoomId.
Preserved $FF as the value meaning “use the selected level’s normal starting room.”
Updated dungeon initialization so Link uses Zelda’s original safe dungeon entrance position.
Prevented the overworld screen-wrap coordinates from being applied to dungeon starts.
Configured dungeon starts to enter through the south doorway while Link moves upward.
Confirmed Level 1 Start
Property	Value
Level	$01
Entrance room	$73
Entry side	South/bottom
Movement direction	Up / $08
Starting X	Approximately $78
Starting Y	LevelInfo_StartY
Direction and Entry Relationship

ObjDir represents the direction Link is moving into the room:

ObjDir	Movement	Entry side
$01	Right	West
$02	Left	East
$04	Down	North
$08	Up	South

The first dungeon test inherited the configured overworld direction of $01, causing Link to enter Level 1 from the west doorway.

Dungeon and overworld spawn behavior are now handled separately. Dungeon starts set ObjDir to $08, placing Link at the south entrance and moving him upward into the room.

Technical Notes

The original room-selection routine behaved differently for the two worlds:

Overworld starts could use CaveSourceRoomId.
Dungeon starts always used LevelInfo_StartRoomId.

Z1 Dojo now checks CaveSourceRoomId regardless of the selected world:

$FF uses LevelInfo_StartRoomId.
Any valid room ID can be used as a requested starting room.

Arbitrary non-entrance dungeon-room loading has been implemented at the room-selection level but has not yet been fully tested. The confirmed test for this version uses Level 1’s normal entrance room, $73.

Milestone

Version 0.0.5 establishes the controlled dungeon-loading foundation.

Z1 Dojo can now:

select the overworld or a dungeon,
load Level 1 directly,
use the dungeon’s normal entrance room,
keep dungeon and overworld spawn behavior separate,
and enter the dungeon correctly through the south doorway.

This provides the foundation for the future combat lobby and selectable dungeon arenas.

### Arbitrary Dungeon Room Test

Direct loading of a non-entrance dungeon room was successfully confirmed.

| Property           |      Value |
| ------------------ | ---------: |
| Level              |      `$01` |
| Selected room      |      `$63` |
| Entry side         |      South |
| Movement direction | Up / `$08` |

Room `$63`, located north of Level 1’s normal entrance room `$73`, loaded directly without first passing through the entrance room.

The selected room’s graphics, collision, enemies, and door configuration initialized normally.

The south entrance was locked, but Link’s initial room-entry sequence still placed him through that doorway. Direct room initialization therefore bypasses normal locked-door traversal checks and does not require or consume a key.

This behavior is appropriate for direct practice-room loading. Future lobby-to-combat-room transitions will use separate logic so configured door states can affect entry and practice strategy.


## [0.0.4] - 20260710183056 -  Configurable Player Spawn Position

Added
Added configurable player spawn-position settings to Z1DojoConfig.inc.
Added named direction constants:
DIR_RIGHT
DIR_LEFT
DIR_DOWN
DIR_UP
Added configurable values for:
Link’s starting X coordinate
Link’s starting Y coordinate
Link’s initial facing direction
Added Z1 Dojo configuration support to program bank 5.
Expanded room-loading documentation with player-position initialization details.
Documented the approximate overworld movement boundaries used by the Zelda engine.
Changed
Replaced the original hardcoded starting X coordinate with DOJO_STARTING_X.
Replaced the original level-defined starting Y coordinate with DOJO_STARTING_Y.
Replaced the original upward-facing direction with DOJO_STARTING_DIR.
Configured the current development build to begin with:
X coordinate $40
Y coordinate $90
Link facing right
Updated the initial room-loading routine so Z1 Dojo controls Link’s position immediately after laying out the starting room.
Confirmed Direction Values
Direction	Value
Right	$01
Left	$02
Down	$04
Up	$08
Original Spawn Behavior

Before this milestone, Zelda initialized Link using:

LDA #$08
STA ObjDir

LDA #$78
STA ObjX

LDA LevelInfo_StartY
STA ObjY

This caused Link to:

Face upward
Begin horizontally near the middle of the room
Use a Y coordinate defined by the current level data

Z1 Dojo now replaces those values with:

LDA #DOJO_STARTING_DIR
STA ObjDir

LDA #DOJO_STARTING_X
STA ObjX

LDA #DOJO_STARTING_Y
STA ObjY
Technical Notes

Link is object slot zero, so the base addresses of the object-position arrays also represent Link’s coordinates:

Symbol	RAM	Purpose
ObjX	$0070	Link’s X coordinate
ObjY	$0084	Link’s Y coordinate
ObjDir	$0098	Link’s facing direction

FCEUX may display coordinate bytes as signed decimal values.

For example:

$95 is unsigned decimal 149
The same byte displayed as signed decimal is -107

The observed $0084 value of -107 therefore represents $95. The difference from the configured $90 is likely caused by movement or adjustment during the initial room-entry animation before the RAM value was observed.

The approximate normal overworld movement boundaries are:

Boundary	Coordinate
Left	$11
Right	$E0
Top	$4E
Bottom	$CD
Milestone

Version 0.0.4 establishes configurable player spawning.

Z1 Dojo can now control:

Starting health
Starting equipment
Starting world
Starting room
Starting X coordinate
Starting Y coordinate
Starting facing direction

This provides the positioning system required to place Link directly beside room edges, blocks, water formations, enemies, and other drill-specific starting locations.

### Calibration Results

The configurable spawn system was tested on overworld room `$77`.

The following drill coordinates were confirmed:

| Property | Configured value | Final observed value |
|---|---:|---:|
| Starting X | `$EA` | `$E9` |
| Starting Y | `$8D` | `$8D` |
| Direction | `$01` | Right |
| Room | `$77` | `$77` |

The engine adjusts Link’s configured X coordinate one pixel to the left
during startup. Configuring `$EA` therefore produces the desired final
coordinate of `$E9`.

Y coordinate `$8D` was confirmed as a clear horizontal lane on room `$77`.

These values form the first documented screen-wrap practice preset, but
they do not represent a separate engine feature. They are an application
of the configurable spawn-position system introduced in this version.

## [0.0.3] - 20260710180607 -  Controlled Room Loading

Added
Added configurable starting-location settings to Z1DojoConfig.inc.
Added named configuration values for:
Starting world
Starting overworld room
Added the ability to begin gameplay on a selected overworld screen instead of always using the original starting screen.
Created initial room-loading research documentation.
Documented important room and position variables:
CurLevel
RoomId
NextRoomId
CaveSourceRoomId
ObjX
ObjY
ObjDir
Documented the overworld room-grid format.
Confirmed that overworld rooms are arranged in a 16-column grid.
Documented the normal starting screen and nearby room IDs.
Changed
Updated save-file selection so Z1 Dojo applies the configured starting world and room whenever a file is loaded.
Replaced the original fixed overworld starting location with a configurable room override.
Configured the current development build to begin on overworld room $78, one screen to the right of the original starting room.
Confirmed Room IDs
Location	Decimal	Hex
Original starting screen	119	$77
One screen right	120	$78
One screen up	103	$67
Technical Notes

The overworld uses a 16-column room grid:

Right: RoomId + $01
Left: RoomId - $01
Up: RoomId - $10
Down: RoomId + $10

When a save slot is selected, Z1 Dojo stores the configured room in CaveSourceRoomId.

During room initialization, the original game checks whether CaveSourceRoomId contains a valid room ID. When it does, that value is copied into RoomId instead of using the normal LevelInfo_StartRoomId.

After the override is applied, CaveSourceRoomId is reset to $FF, preserving the original game’s normal room-transition behavior.

The default initial player position was also identified:

Link faces upward.
Link starts at X coordinate $78.
Link’s Y coordinate comes from LevelInfo_StartY.

Configurable starting coordinates have not yet been implemented and are planned for the next development milestone.

Milestone

Version 0.0.3 establishes controlled overworld room loading.

Z1 Dojo can now control:

Starting health
Starting equipment
Starting world
Starting overworld room

This is the first location-control system in the project and provides the foundation for future overworld screen-scroll drills and direct access to specialized practice areas.

## [0.0.2] - 20260710172606 - Inventory System

Added
Created Z1DojoConfig.inc as the central configuration file for Z1 Dojo settings.
Added named constants for sword grades:
No Sword
Wooden Sword
White Sword
Magical Sword
Added named constants for ring grades:
No Ring / Green Tunic
Blue Ring
Red Ring
Added reusable constants for owned and unowned inventory items.
Added an InvSword alias for the sword value stored at the beginning of the inventory block.
Added configurable starting values for:
Heart containers
Current health
Sword
Ring
Bomb count
Maximum bomb capacity
Ladder ownership
Began documenting the Zelda inventory and save-data system.
Documented the 40-byte inventory block beginning at RAM address $0657.
Documented confirmed inventory offsets for:
Sword
Bombs
Arrows
Bow
Candle
Bait
Potion
Raft
Book
Ring
Ladder
Magical Key
Power Bracelet
Letter
Compasses
Maps
Rupees
Keys
Hearts
Triforce pieces
Boomerangs
Magical Shield
Maximum bombs
Documented the packed format used by HeartValues.
Documented the Zelda item-class system:
Unique and boolean items
Numeric item amounts
Upgrade grades
Special item values
Changed
Replaced the temporary hardcoded starting-health modification with named Z1 Dojo configuration constants.
Updated new-file initialization to apply the configured Z1 Dojo starting loadout.
Updated active-profile initialization to apply the same configured loadout.
New save files now begin with:
8 full heart containers
White Sword
Blue Ring
8 bombs
Maximum bomb capacity of 8
Ladder
Confirmed that configured equipment appears correctly in gameplay and on the inventory screen.
Technical Notes

The sword is stored at offset $00 of the inventory block and uses graded values:

$00 — No Sword
$01 — Wooden Sword
$02 — White Sword
$03 — Magical Sword

The ring is stored at offset $0B and uses graded values:

$00 — No Ring / Green Tunic
$01 — Blue Ring
$02 — Red Ring

The ladder is stored at offset $0C and uses a boolean ownership value:

$00 — Not owned
$01 — Owned

This milestone establishes the first reusable Z1 Dojo subsystem. Future practice rooms and training modes will be able to use configurable equipment instead of relying on one-off ROM edits.

## [0.0.1] - 20260710172419 - Foundation

### Added

* Established the Z1 Dojo project.
* Successfully built the original Zelda 1 source from the disassembly project.
* Verified a byte-identical build against the original PRG0 ROM.
* Configured the development environment using:

  * Git
  * Git Bash
  * cc65
  * ca65
  * ld65
  * FCEUX
* Established the project's Git workflow and development roadmap.
* Began documenting the Zelda engine for future development.

### Changed

* Modified new game initialization to start Link with **8 full heart containers** instead of the default 3.
* Successfully rebuilt and verified the modified ROM.
* Confirmed the complete edit → build → test workflow.

### Notes

This release represents the successful creation of the project's development foundation. While the only gameplay change is the starting heart count, the more significant milestone is proving that the entire toolchain is functioning correctly and that the project is ready for larger engine modifications.

Future releases will focus on configurable loadouts, practice environments, combat arenas, movement drills, and the long-term goal of creating the definitive Zelda 1 training platform.
