# Z1 Training Lab

> **A purpose-built training environment for *The Legend of Zelda* (NES), designed to help players develop real skills through focused, repeatable practice.**

---

## Overview

**Z1 Training Lab** is an open-source practice platform created for players of the original **The Legend of Zelda** and the **Zelda 1 Randomizer (Z1R)**.

Instead of requiring players to repeatedly play full seeds just to practice a single difficult mechanic, Z1 Training Lab provides a controlled environment where individual skills can be practiced in seconds instead of hours.

Whether you're learning your very first block clip, trying to master Blue Wizzrobes, or preparing for tournament races, this project is designed to reduce the time between:

> **"I want to practice this."**

and

> **Actually practicing it.**

---

# Project Philosophy

This project is **not** intended to make Zelda easier.

It is intended to make **practice better**.

Learning Zelda Randomizer today often looks like this:

* Play a random seed.
* Spend an hour routing.
* Finally encounter the mechanic you wanted to practice.
* Fail.
* Start another seed.

That is a poor learning environment.

The goal of Z1 Training Lab is to transform that process into:

* Choose a skill.
* Press Start.
* Practice immediately.
* Reset instantly.
* Measure improvement.

The project is built around the principles of deliberate practice rather than normal gameplay.

---

# Planned Features

## Combat Training

Practice individual enemy types under configurable conditions.

Examples include:

* Blue Wizzrobes
* Red Wizzrobes
* Blue Lynels
* Red Lynels
* Blue Darknuts
* Like Likes
* Pols Voice
* Gibdos
* Vires
* Gleeok
* Patra
* Ganon

Configurable options may include:

* Enemy count
* Room layout
* Sword
* Ring
* Heart containers
* Bombs
* Inventory
* Difficulty presets

---

## Movement Training

Dedicated practice environments for advanced movement techniques.

Examples include:

* Upward block clipping
* T-Room ladder clipping
* Overworld screen scrolling
* Bomb placement
* Recorder setups

Each drill is designed for rapid repetition with minimal downtime.

---

## Dungeon Training

Practice common dungeon situations without replaying entire seeds.

Examples:

* Bomb hole searching
* Staircase recognition
* Recorder rooms
* Maze navigation
* Dangerous combat rooms
* Decision making

---

## Boss Training

Instant access to boss encounters including:

* Aquamentus
* Dodongo
* Manhandla
* Gleeok
* Patra
* Ganon

---

## Custom Practice Arena *(Long-Term Goal)*

Eventually players will be able to configure:

* Enemy type
* Enemy count
* Equipment
* Hearts
* Bombs
* Room type
* Practice rules

allowing nearly unlimited combinations.

---

## Statistics

One of the long-term goals of the project is to provide measurable improvement.

Examples:

* Attempts
* Success rate
* Clear rate
* Best completion time
* Average completion time
* Damage taken
* Practice streaks

The idea is not simply to practice more—

it is to practice smarter.

---

# Development Philosophy

This project is intentionally being developed like a software product rather than a traditional ROM hack.

Every feature must answer one question:

> **Does this reduce the time between wanting to practice something and actually practicing it?**

If the answer is "no," it probably doesn't belong in the project.

---

# Roadmap

## Version 0.1

* Build system
* Development environment
* Initial ROM modifications
* Configurable starting hearts

---

## Version 0.2

* Configurable starting inventory
* White Sword
* Blue Ring
* Bomb count
* Ladder

---

## Version 0.3

* Dedicated practice rooms

---

## Version 0.4

* Instant retry system

---

## Version 0.5

* Block Clip Trainer

---

## Version 0.6

* Ladder Clip Trainer

---

## Version 0.7

* Screen Scroll Trainer

---

## Version 0.8

* Combat Arenas

---

## Version 0.9

* Statistics
* Timers
* Practice tracking

---

## Version 1.0

The first complete release of Z1 Training Lab.

---

# Who This Project Is For

* Zelda 1 players
* Zelda 1 Randomizer players
* Tournament racers
* New players
* Speedrunners
* TAS researchers
* ROM hacking enthusiasts
* Anyone interested in learning NES game programming

---

# Building

This project is intended for developers.

A legally obtained copy of the supported ROM is required.

The project is built using:

* cc65
* ca65
* ld65
* FCEUX
* Git

Detailed build instructions will be documented in the `docs/` directory.

---

# Legal

## ROMs

This repository **does not contain** any Nintendo ROMs.

You must provide your own legally obtained copy of the supported game.

Do **not** open issues requesting ROMs.

They will be closed immediately.

---

## Patches

Releases are distributed as patch files only.

Examples:

* BPS
* IPS

No playable ROM images will ever be distributed through this project.

---

## Nintendo Assets

Nintendo owns all rights to:

* The Legend of Zelda
* Zelda
* Link
* Ganon
* The game's graphics
* Music
* Sound effects
* Original code
* Story
* Trademarks

Nothing in this project is intended to claim ownership of those properties.

---

## This Project

The original source code written specifically for Z1 Training Lab is released under the license included in this repository.

That license **does not** apply to Nintendo intellectual property.

---

## Disclaimer

This is an unofficial fan project.

It is not affiliated with, sponsored by, endorsed by, licensed by, or approved by Nintendo.

"The Legend of Zelda," "Zelda," "Link," and all related properties are trademarks and copyrights of Nintendo.

---

# Contributing

Contributions are welcome.

Ideas, bug reports, feature requests, documentation improvements, and pull requests are appreciated.

If you have an idea that would improve practice or make learning Zelda easier for new players, please open an issue.

---

# Vision

The long-term goal is simple:

To become the definitive practice environment for the original NES Zelda.

The hope is that someday players will say:

> "Before your first race...
>
> Spend an hour in the Training Lab."

If this project helps even one player become more confident, learn a difficult technique, or enjoy Zelda Randomizer a little more, then it has succeeded.

---

# Acknowledgements

Special thanks to:

* The Zelda 1 Randomizer community
* The NES development community
* The authors and maintainers of the Zelda disassembly project
* Everyone who continues to document and preserve classic games

Without the work of these communities, this project would not be possible.

---

# License

See the LICENSE file for details regarding the original source code included with this project.

Nintendo assets, trademarks, copyrighted material, and game data remain the property of Nintendo.
