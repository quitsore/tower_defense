```plantuml
class Monster {
+ location: Location
}

class Goblin

class Map {
+ is_available(location: Location): bool
+ is_trap(location: Location): bool
+ is_free(location: Location): bool
}

class Location

Goblin --|> Monster
Monster -- Location
Map -- Location

```