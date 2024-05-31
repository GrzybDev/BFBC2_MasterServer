Battlefield: Bad Company 2 Master Server Emulator
=================================================

Master Server Emulator for Battlefield: Bad Company 2 that aims to be complete replacement for the original master server, allowing to play the game without contacting EA servers.
This is based on packets I captured from the original master server and the game itself. Game Clients and Servers need to use [BFBC2_Hook](https://github.com/GrzybDev/BFBC2_Hook) to be able to connect to this server, because we expect that game client and server will use WebSocket reimplementation instead of old Plasma/Theater based protocol.

Demo Server
===========

### Config (for BFBC2_Hook, if you didn't override it in config you don't need to configure it manually):
- Address: `bfbc2.grzyb.app`
- Port: `443`
- Secure: `Yes`

### Serial Keys:
- Activate base game: `ACTIVATE-GAME`
- Activate Vietnam DLC: `ACTIVATE-VIETNAM`
- Activate access to SPECACT kits: `ACTIVATE-SPECACT`
- Activate Premium Edition (some game items are pre-unlocked): `ACTIVATE-PREMIUM`
- Activate veteran rank/weapons (M1 access): `ACTIVATE-VETERAN`

Table of Contents
-----------------
- [Game Info](#game-info)
- [Legal notes](#legal-notes)
- [Requirements](#requirements)
- [Setup](#setup)

Game Info
---------
![Battlefield: Bad Company 2 Cover](https://upload.wikimedia.org/wikipedia/en/b/b3/Battlefield_Bad_Company_2_cover.jpg "Battlefield: Bad Company 2 Cover")

|         Type | Value                                                        |
|-------------:|:-------------------------------------------------------------|
| Developer(s) | EA DICE                                                      |
| Publisher(s) | Electronic Arts                                              |
|    Writer(s) | David Goldfarb                                               |
|  Composer(s) | Mikael Karlsson, Joel Eriksson                               |
|       Series | Battlefield                                                  |
|       Engine | Frostbite 1.5                                                |
|  Platform(s) | Microsoft Windows, PlayStation 3, Xbox 360, iOS, Kindle Fire |
|     Genre(s) | First-person shooter                                         |
|      Mode(s) | Single-player, Multi-Player                                  |

Legal notes
-----------

- The project doesn't contain ***any*** original code from the game!
- To use this project you need to have an original copy of the game (bought from [Origin](https://www.ea.com/games/battlefield/battlefield-bad-company-2)), the project doesn't make piracy easier and doesn't break any of the DRM included in-game.

Requirements
------------

- Docker and Docker Compose

Eventually, running manually:

- Python 3.10+
- Poetry
- Redis server
- SQLAlchemy-compatible or MongoDB database

Setup
-----

- Create .env file with required environment variables

Example docker-compose configuration can be found in 'docker-compose.*.yml' files

Credits
-------

- [GrzybDev](https://grzyb.dev)

Special thanks to:
- Domo and Freaky123 (for sharing the Server Files and the v10.0 source code)
- Aluigi (for the tools that made it possible to view and record the BF:BC2 network traffic)
- DICE (for making the game)
