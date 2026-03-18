class Room:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.connections: dict[str, 'Room'] = {}
        self.treasure: dict | None = None
        self.enemy: Enemy | None = None # type: ignore
        
    def connect(self, direction: str, room: 'Room'):
        self.connections[direction] = room
    
    def get_room_in_direction(self, direction: str) -> 'Room | None':
        return self.connections.get(direction)
    
    def describe(self):
        print(f"\n┌─ {self.name} ─{'─' * (len(self.name) + 2)}")
        print(f"|   {self.description}")
        print("└──────────────────────────────────────────────")
        
        if self.connections:
            exits = ", ".join(f"[{d.upper()}]" for d in sorted(self.connections))
            print(f"Exits: {exits}")
        else:
            print("\nNo obvious exits...")
        print()