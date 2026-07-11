# Right-Edge Screen Scroll Drill

## Status

Initial development drill introduced in Z1 Dojo v0.0.5.

## Purpose

Provide immediate access to the confirmed X-coordinate setup used for
right-edge screen-scroll practice on the overworld.

## Configuration

| Property | Value |
|---|---:|
| Starting world | Overworld |
| Starting room | `$77` |
| Expected destination room | `$78` |
| Starting X | `$E9` / 233 |
| Starting Y | `$90` |
| Starting direction | Right / `$01` |

## Room Transition

The drill starts on overworld room `$77`.

Moving to the screen on the right changes the current room to `$78`.

## Confirmed Setup

The required horizontal setup coordinate is:

```text
X = 233 decimal
X = $E9 hexadecimal