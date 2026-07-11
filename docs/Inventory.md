# Inventory System

The active player inventory is stored in a 40-byte block beginning at
RAM address `$0657`.

```asm
Items := $657


HeartValues

Location:
$066F

Purpose:
Stores current hearts and maximum heart containers.

Format:
High nibble = Current full hearts (0-based)
Low nibble = Heart containers (0-based)

Example:

$22 = 3/3 hearts

$77 = 8/8 hearts

Used by:
New File
Save System
HUD
Damage
Healing


|   Offset |        RAM | Variable            | Likely purpose             |
| -------: | ---------: | ------------------- | -------------------------- |
|    `$00` |     `$657` | `Items`             | Sword                      |
|    `$01` |     `$658` | `InvBombs`          | Current bombs              |
|    `$02` |     `$659` | `InvArrow`          | Arrow upgrade              |
|    `$03` |     `$65A` | `Bow`               | Bow ownership              |
|    `$04` |     `$65B` | `InvCandle`         | Candle upgrade             |
|    `$05` |     `$65C` | Unnamed             | Probably Recorder          |
|    `$06` |     `$65D` | `InvFood`           | Bait                       |
|    `$07` |     `$65E` | `Potion`            | Potion level               |
|    `$08` |     `$65F` | Unnamed             | Unknown                    |
|    `$09` |     `$660` | `InvRaft`           | Raft                       |
|    `$0A` |     `$661` | `InvBook`           | Book                       |
|    `$0B` |     `$662` | `InvRing`           | Ring upgrade               |
|    `$0C` |     `$663` | `InvLadder`         | Ladder                     |
|    `$0D` |     `$664` | `InvMagicKey`       | Magical Key                |
|    `$0E` |     `$665` | `InvBracelet`       | Power Bracelet             |
|    `$0F` |     `$666` | `InvLetter`         | Letter                     |
|    `$10` |     `$667` | `InvCompass`        | Compass flags, Levels 1–8  |
|    `$11` |     `$668` | `InvMap`            | Map flags, Levels 1–8      |
|    `$12` |     `$669` | `InvCompass9`       | Level 9 compass            |
|    `$13` |     `$66A` | `InvMap9`           | Level 9 map                |
|    `$14` |     `$66B` | Unnamed             | Unknown                    |
|    `$15` |     `$66C` | `InvClock`          | Clock pickup state         |
|    `$16` |     `$66D` | `InvRupees`         | Rupee count                |
|    `$17` |     `$66E` | `InvKeys`           | Key count                  |
|    `$18` |     `$66F` | `HeartValues`       | Full hearts and containers |
|    `$19` |     `$670` | `HeartPartial`      | Partial-heart health       |
|    `$1A` |     `$671` | `InvTriforce`       | Triforce-piece flags       |
|    `$1B` |     `$672` | `LastBossDefeated`  | Boss/progression state     |
|    `$1C` |     `$673` | Unnamed             | Unknown                    |
|    `$1D` |     `$674` | `InvBoomerang`      | Wooden Boomerang           |
|    `$1E` |     `$675` | `InvMagicBoomerang` | Magical Boomerang          |
|    `$1F` |     `$676` | `InvMagicShield`    | Magical Shield             |
| `$20–24` | `$677–67B` | Unnamed             | Unknown                    |
|    `$25` |     `$67C` | `MaxBombs`          | Bomb capacity              |
|    `$26` |     `$67D` | `RupeesToAdd`       | Animated rupee additions   |
|    `$27` |     `$67E` | `RupeesToSubtract`  | Animated rupee deductions  |


|    Offset |           RAM | Symbol              | Purpose                    | Values         |
| --------: | ------------: | ------------------- | -------------------------- | -------------- |
|     `$00` |       `$0657` | `Items`             | Sword                      | TBD            |
|     `$01` |       `$0658` | `InvBombs`          | Current bombs              | `0-MaxBombs`   |
|     `$02` |       `$0659` | `InvArrow`          | Arrow upgrade              | TBD            |
|     `$03` |       `$065A` | `Bow`               | Bow ownership              | TBD            |
|     `$04` |       `$065B` | `InvCandle`         | Candle upgrade             | TBD            |
|     `$05` |       `$065C` | Unnamed             | Suspected Recorder         | TBD            |
|     `$06` |       `$065D` | `InvFood`           | Bait                       | TBD            |
|     `$07` |       `$065E` | `Potion`            | Potion level               | TBD            |
|     `$08` |       `$065F` | Unnamed             | Unknown                    | TBD            |
|     `$09` |       `$0660` | `InvRaft`           | Raft                       | TBD            |
|     `$0A` |       `$0661` | `InvBook`           | Book                       | TBD            |
|     `$0B` |       `$0662` | `InvRing`           | Ring upgrade               | TBD            |
|     `$0C` |       `$0663` | `InvLadder`         | Ladder                     | TBD            |
|     `$0D` |       `$0664` | `InvMagicKey`       | Magical Key                | TBD            |
|     `$0E` |       `$0665` | `InvBracelet`       | Power Bracelet             | TBD            |
|     `$0F` |       `$0666` | `InvLetter`         | Letter                     | TBD            |
|     `$10` |       `$0667` | `InvCompass`        | Level 1-8 compass flags    | Bitmask        |
|     `$11` |       `$0668` | `InvMap`            | Level 1-8 map flags        | Bitmask        |
|     `$12` |       `$0669` | `InvCompass9`       | Level 9 compass            | TBD            |
|     `$13` |       `$066A` | `InvMap9`           | Level 9 map                | TBD            |
|     `$14` |       `$066B` | Unnamed             | Unknown                    | TBD            |
|     `$15` |       `$066C` | `InvClock`          | Clock state                | TBD            |
|     `$16` |       `$066D` | `InvRupees`         | Rupees                     | `0-255`        |
|     `$17` |       `$066E` | `InvKeys`           | Keys                       | `0-255`        |
|     `$18` |       `$066F` | `HeartValues`       | Hearts and containers      | Packed nibbles |
|     `$19` |       `$0670` | `HeartPartial`      | Partial heart              | `0-$FF`        |
|     `$1A` |       `$0671` | `InvTriforce`       | Triforce pieces            | Bitmask        |
|     `$1B` |       `$0672` | `LastBossDefeated`  | Boss/progression state     | TBD            |
|     `$1C` |       `$0673` | Unnamed             | Unknown                    | TBD            |
|     `$1D` |       `$0674` | `InvBoomerang`      | Wooden Boomerang           | TBD            |
|     `$1E` |       `$0675` | `InvMagicBoomerang` | Magical Boomerang          | TBD            |
|     `$1F` |       `$0676` | `InvMagicShield`    | Magical Shield             | TBD            |
| `$20-$24` | `$0677-$067B` | Unnamed             | Unknown                    | TBD            |
|     `$25` |       `$067C` | `MaxBombs`          | Maximum bombs              | Numeric        |
|     `$26` |       `$067D` | `RupeesToAdd`       | Pending rupees to add      | Numeric        |
|     `$27` |       `$067E` | `RupeesToSubtract`  | Pending rupees to subtract | Numeric        |

SWORD_NONE     = $00
SWORD_WOODEN   = $01
SWORD_WHITE    = $02
SWORD_MAGICAL  = $03

RING_NONE      = $00
RING_BLUE      = $01
RING_RED       = $02

| `$00` | `$0657` | `Items` / proposed `InvSword` | Sword upgrade | Values pending verification |
| `$0B` | `$0662` | `InvRing` | Ring upgrade | Values pending verification |
| `$0C` | `$0663` | `InvLadder` | Ladder ownership | Boolean value pending verification |

## Sword Storage

The sword uses offset `$00` of the Items block. The disassembly currently
uses the base symbol `Items` rather than a dedicated `InvSword` symbol.

Z1 Dojo may define an alias for clarity:

```asm
InvSword := Items


Once the lookup tables confirm the values, our first real Z1 Dojo include file will look roughly like this:

```asm
; Z1DojoConfig.inc

SWORD_NONE      = $00
SWORD_WOODEN    = $01
SWORD_WHITE     = $02
SWORD_MAGICAL   = $03

RING_NONE       = $00
RING_BLUE       = $01
RING_RED        = $02

ITEM_NOT_OWNED  = $00
ITEM_OWNED      = $01

DOJO_STARTING_HEARTS = $77
DOJO_STARTING_SWORD  = SWORD_WHITE
DOJO_STARTING_RING   = RING_BLUE
DOJO_STARTING_BOMBS  = $08
DOJO_STARTING_LADDER = ITEM_OWNED