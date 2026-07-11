# Combat Lobby Research

## Purpose

The Z1 Dojo combat lobby provides a safe preparation area between setup selection and active combat.

The player is not placed directly into a room containing active enemies.

## Initial Test Layout

| Purpose     | Level |  Room |
| ----------- | ----: | ----: |
| Lobby       | `$01` | `$73` |
| Combat room | `$01` | `$63` |

Room `$63` is directly north of room `$73`.

## Confirmed Flow

1. Z1 Dojo loads room `$73`.
2. Link enters the lobby from the south.
3. No combat enemies are active in the lobby.
4. The player chooses when to walk through the north doorway.
5. Zelda performs its normal room transition.
6. Room `$63` becomes the active room.
7. Room `$63` enemies spawn normally.

## Lobby Door Layout

| Side  | Type |
| ----- | ---- |
| North | Open |
| East  | Wall |
| South | Open |
| West  | Wall |

## Design Result

The lobby successfully separates preparation from combat.

This allows the player to:

* confirm equipment,
* inspect health and consumables,
* position their hands,
* and deliberately begin the attempt.

## Current Limitation

The first lobby implementation uses normal dungeon adjacency.

The lobby north exit currently reaches room `$63` because that is the room naturally located north of `$73`.

A later system must intercept the lobby transition and replace the normal destination with the player-selected combat arena.

## Arbitrary Arena Redirection

Z1 Dojo v0.0.13 intercepts the lobby’s northward room transition.

### Normal Room Calculation

Zelda calculates the next dungeon room by adding a direction-based offset to the current room.

For a northward transition:

```text
RoomId + $F0
```

Because the arithmetic uses an eight-bit room ID, this is equivalent to subtracting `$10`.

The normal destination from lobby room `$73` is therefore `$63`.

### Z1 Dojo Override

After Zelda calculates `NextRoomId`, Z1 Dojo checks:

* current level,
* current room,
* transition direction.

When the current location is the Dojo lobby and the direction is north, `NextRoomId` is replaced with the selected combat-room ID.

### Confirmed Test

| Property               |         Value |
| ---------------------- | ------------: |
| Lobby level            |         `$01` |
| Lobby room             |         `$73` |
| Direction              | North / `$08` |
| Normal destination     |         `$63` |
| Redirected destination |         `$53` |

Room `$53` loaded successfully using Zelda’s normal scrolling process.

### Lobby Containment

The lobby’s south doorway is configured as a wall.

Direct initial loading can still place Link through that side, but the player cannot use it as an exit after gaining control.

## Separate Lobby and Combat-Room Configuration

Z1 Dojo v0.0.14 separates the fixed lobby layout from the selected combat-room layout.

### Lobby

The lobby receives its doorway configuration during initial dungeon loading.

### Combat Room

The selected combat room receives its doorway configuration while Zelda lays out the redirected destination during the upward room scroll.

### Confirmed Test Layout

| Side  | Lobby | Combat room       |
| ----- | ----- | ----------------- |
| North | Open  | Shutter           |
| East  | Wall  | Bombable          |
| South | Wall  | Open              |
| West  | Wall  | Walk-through wall |

The combat room successfully displayed and executed all four configured behaviors.

### Shared Door Packer

Both configurations use the same reusable packing routine.

Temporary bytes contain:

| Temporary | Door  |
| --------: | ----- |
|     `$01` | North |
|     `$02` | East  |
|     `$03` | South |
|     `$04` | West  |

The routine writes the values into the selected room’s door-attribute fields while preserving its palette information.

### Upward-Scroll Integration

For upward scrolling, Zelda temporarily assigns `NextRoomId` to `RoomId` before calling `LayOutRoom`.

Z1 Dojo uses this moment to apply the selected combat-room attributes.

The source lobby room is restored after the destination is drawn, and Zelda completes its normal scrolling transition.
