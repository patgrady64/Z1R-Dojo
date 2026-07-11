## Controlled Dungeon Loading

Z1 Dojo v0.0.5 added support for beginning directly inside a selected dungeon.

### Level 1 Test

| Property        |      Value |
| --------------- | ---------: |
| `CurLevel`      |      `$01` |
| `RoomId`        |      `$73` |
| Entry direction | Up / `$08` |
| Entry side      |      South |

Level 1’s normal entrance room is `$73`.

### Initial Entry Problem

The first dungeon test inherited the overworld practice direction:

```text
ObjDir = $01
```

Because `$01` means Link is moving right, the room-entry routine interpreted this as an entrance from the west doorway.

Dungeon starts now use:

```text
ObjDir = $08
```

This means Link moves upward and enters from the south doorway.

### Entry Direction Table

| Movement direction | Value | Room entry side |
| ------------------ | ----: | --------------- |
| Right              | `$01` | West            |
| Left               | `$02` | East            |
| Down               | `$04` | North           |
| Up                 | `$08` | South           |

### Room Override Behavior

The original game only allowed `CaveSourceRoomId` to select an initial overworld room. Dungeon starts always used `LevelInfo_StartRoomId`.

Z1 Dojo now uses the following behavior:

* `CaveSourceRoomId = $FF`: use `LevelInfo_StartRoomId`
* `CaveSourceRoomId = valid room ID`: use the supplied room ID

Direct loading of a non-entrance dungeon room still needs to be tested.

## Configurable Dungeon Entry

Z1 Dojo v0.0.7 separated dungeon entry direction from arena selection.

The same arena can be entered from any of its four sides.

### Direction Mapping

| Entry side | Movement direction | Value |
| ---------- | ------------------ | ----: |
| West       | Right              | `$01` |
| East       | Left               | `$02` |
| North      | Down               | `$04` |
| South      | Up                 | `$08` |

### Direct-Load Coordinate Handling

Horizontal entries are partially positioned by Zelda’s normal room-entry routine:

* west entry sets Link near the left edge,
* east entry sets Link near the right edge.

The direct-load path must supply the Y lane used for those entries.

Vertical entries require Z1 Dojo to supply the complete starting position because the normal scrolling sequence is skipped:

| Entry side |     X |     Y |
| ---------- | ----: | ----: |
| North      | `$78` | `$3D` |
| South      | `$78` | `$DD` |

The confirmed horizontal doorway lane is:

```text
Y = $8D
```

### Entry and Door Geometry

Initial entry placement does not require the selected room to contain a visible door on that side.

A room without a west doorway can still be initialized using a west entry.

This confirms that the following systems can be controlled separately:

1. Room geometry
2. Entry direction
3. Visible door type
4. Door behavior
