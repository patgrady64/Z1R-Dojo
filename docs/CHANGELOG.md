# Changelog

All notable changes to **Z1 Dojo** will be documented in this file.

This project follows a milestone-based development process rather than feature dumps. Each version represents meaningful progress toward creating a complete training environment for *The Legend of Zelda* (NES) and Zelda 1 Randomizer players.

--
## [0.0.13] - 20260711131149 - Lobby Arena Redirection



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
