"""
Procedural Maze Generator for Agents

This module generates random file system mazes with configurable:
- Depth levels (3-10 directories deep)
- Branching factor (2-5 paths per directory)
- Puzzle complexity (simple to expert)
- Red herring density (low to high)
- Various puzzle types (coordinates, riddles, patterns, math, logic)

Each generated maze is unique and solvable with multiple valid paths.
"""

import json
import random
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional


class DifficultyLevel(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


class PuzzleType(Enum):
    COORDINATES = "coordinates"
    RIDDLE = "riddle"
    PATTERN = "pattern"
    MATH = "math"
    LOGIC = "logic"


@dataclass
class MazeConfig:
    """Configuration for procedural maze generation."""
    depth: int = 5  # How many levels deep
    branching_factor: int = 3  # Average paths per directory
    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM
    red_herring_ratio: float = 0.4  # Ratio of false paths
    puzzle_density: float = 0.6  # How many directories have puzzles
    treasure_name: str = "GOLDEN_IDOL"
    theme: str = "fantasy"  # fantasy, sci-fi, mystery, etc.
    enable_coordinates: bool = True
    enable_riddles: bool = True
    enable_math: bool = False


@dataclass
class MazeNode:
    """Represents a directory node in the maze."""
    name: str
    path: str
    depth: int
    is_treasure_path: bool = False
    children: List['MazeNode'] = field(default_factory=list)
    files: Dict[str, str] = field(default_factory=dict)
    puzzle_type: Optional[PuzzleType] = None
    clue_content: str = ""
    red_herring: bool = False


class ProceduralMazeGenerator:
    """Generates random file system mazes for AI agent competitions."""
    
    def __init__(self, config: MazeConfig):
        self.config = config
        self.treasure_path: List[str] = []
        self.all_nodes: List[MazeNode] = []
        
        # Theme-based content
        self.themes = {
            "fantasy": {
                "locations": ["forest", "cavern", "ruins", "temple", "tower", "dungeon", "shrine", "castle"],
                "objects": ["crystal", "scroll", "altar", "statue", "rune", "gem", "orb", "throne"],
                "creatures": ["dragon", "phoenix", "unicorn", "wizard", "guardian", "spirit", "oracle"],
                "treasures": ["GOLDEN_IDOL", "CRYSTAL_CROWN", "ANCIENT_TOME", "MYSTIC_ORB"]
            },
            "sci-fi": {
                "locations": ["station", "lab", "core", "bridge", "engine", "bay", "vault", "chamber"],
                "objects": ["console", "data", "crystal", "module", "drive", "scanner", "beacon"],
                "creatures": ["ai", "android", "alien", "cyborg", "robot", "entity", "probe"],
                "treasures": ["QUANTUM_CORE", "DATA_CRYSTAL", "FUSION_CELL", "NEURAL_MATRIX"]
            },
            "mystery": {
                "locations": ["office", "library", "study", "vault", "basement", "attic", "gallery", "salon"],
                "objects": ["clue", "evidence", "document", "key", "safe", "painting", "diary", "letter"],
                "creatures": ["detective", "witness", "suspect", "butler", "guard", "curator"],
                "treasures": ["MISSING_WILL", "STOLEN_PAINTING", "SECRET_FORMULA", "HIDDEN_TRUTH"]
            }
        }
    
    def generate_maze(self, maze_path: str = "./procedural_maze") -> MazeNode:
        """Generate a complete procedural maze."""
        print(f"🎲 Generating procedural maze (depth={self.config.depth}, theme={self.config.theme})")
        
        # Clear previous state
        self.treasure_path = []
        self.all_nodes = []
        
        # Generate treasure path first
        self._generate_treasure_path()
        
        # Create root node
        root = MazeNode(name="entrance", path="", depth=0)
        self.all_nodes.append(root)
        
        # Build maze tree
        self._build_maze_tree(root)
        
        # Add puzzles and clues
        self._add_puzzles_and_clues()
        
        # Add red herrings
        self._add_red_herrings()
        
        # Create file system
        self._create_file_system(root, Path(maze_path))
        
        print(f"✅ Generated maze with {len(self.all_nodes)} nodes")
        print(f"🎯 Treasure path: {' → '.join(self.treasure_path)}")
        
        return root
    
    def _generate_treasure_path(self):
        """Generate the correct path to the treasure."""
        theme_data = self.themes[self.config.theme]
        locations = theme_data["locations"].copy()
        random.shuffle(locations)
        
        # Generate path of appropriate depth
        for i in range(self.config.depth):
            if i == 0:
                self.treasure_path.append("entrance")
            elif i == self.config.depth - 1:
                # Final treasure chamber
                treasure = random.choice(theme_data["treasures"])
                self.treasure_path.append(f"{treasure.lower()}_chamber")
            else:
                # Intermediate locations
                location = locations[i % len(locations)]
                self.treasure_path.append(location)
    
    def _build_maze_tree(self, node: MazeNode):
        """Recursively build the maze tree structure."""
        if node.depth >= self.config.depth:
            return
        
        # Determine if this is on the treasure path
        is_treasure_node = node.depth < len(self.treasure_path) - 1
        
        if is_treasure_node:
            # Add the correct path child
            next_treasure_name = self.treasure_path[node.depth + 1]
            treasure_child = MazeNode(
                name=next_treasure_name,
                path=f"{node.path}/{next_treasure_name}" if node.path else next_treasure_name,
                depth=node.depth + 1,
                is_treasure_path=True
            )
            node.children.append(treasure_child)
            self.all_nodes.append(treasure_child)
            
            # Recursively build treasure path
            self._build_maze_tree(treasure_child)
        
        # Add additional children (some correct, some red herrings)
        num_additional = random.randint(1, self.config.branching_factor)
        theme_data = self.themes[self.config.theme]
        
        for _ in range(num_additional):
            # Generate a random location name
            location_pool = theme_data["locations"] + theme_data["objects"]
            child_name = random.choice(location_pool)
            
            # Avoid duplicates
            existing_names = [child.name for child in node.children]
            while child_name in existing_names:
                child_name = random.choice(location_pool)
            
            child = MazeNode(
                name=child_name,
                path=f"{node.path}/{child_name}" if node.path else child_name,
                depth=node.depth + 1,
                is_treasure_path=False,
                red_herring=random.random() < self.config.red_herring_ratio
            )
            node.children.append(child)
            self.all_nodes.append(child)
            
            # Recursively build (with decreasing probability for deeper levels)
            if random.random() > (node.depth * 0.2):
                self._build_maze_tree(child)
    
    def _add_puzzles_and_clues(self):
        """Add puzzles and clues throughout the maze."""
        treasure_nodes = [node for node in self.all_nodes if node.is_treasure_path]
        
        for i, node in enumerate(treasure_nodes[:-1]):  # Exclude final treasure chamber
            if random.random() < self.config.puzzle_density:
                next_node = treasure_nodes[i + 1]
                puzzle_type = self._choose_puzzle_type()
                clue = self._generate_clue(puzzle_type, next_node, node)
                
                node.puzzle_type = puzzle_type
                node.clue_content = clue
                
                # Add clue file
                node.files[f"clue_{puzzle_type.value}.txt"] = clue
        
        # Always add welcome message to entrance
        entrance = self.all_nodes[0]
        theme_data = self.themes[self.config.theme]
        treasure_name = random.choice(theme_data["treasures"])
        entrance.files["welcome.txt"] = f"Welcome, brave explorer! The {treasure_name} awaits those clever enough to solve the ancient puzzles."
        entrance.files["rules.txt"] = "Use your tools wisely. Beware of false paths and red herrings!"
        
        # Add final treasure
        final_node = treasure_nodes[-1]
        final_node.files[f"{self.config.treasure_name}.txt"] = self._generate_treasure_text()
    
    def _choose_puzzle_type(self) -> PuzzleType:
        """Choose a random puzzle type based on configuration."""
        available_types = []
        
        if self.config.enable_coordinates:
            available_types.append(PuzzleType.COORDINATES)
        if self.config.enable_riddles:
            available_types.append(PuzzleType.RIDDLE)
        if self.config.enable_math:
            available_types.append(PuzzleType.MATH)
        
        # Default fallbacks
        available_types.extend([PuzzleType.PATTERN, PuzzleType.LOGIC])
        
        return random.choice(available_types)
    
    def _generate_clue(self, puzzle_type: PuzzleType, target_node: MazeNode, current_node: MazeNode) -> str:
        """Generate a clue based on puzzle type."""
        if puzzle_type == PuzzleType.COORDINATES:
            return self._generate_coordinate_clue(target_node)
        elif puzzle_type == PuzzleType.RIDDLE:
            return self._generate_riddle_clue(target_node.name)
        elif puzzle_type == PuzzleType.PATTERN:
            return self._generate_pattern_clue(target_node.name)
        elif puzzle_type == PuzzleType.MATH:
            return self._generate_math_clue(target_node.name)
        else:
            return self._generate_logic_clue(target_node.name)
    

    
    def _generate_coordinate_clue(self, target_node: MazeNode) -> str:
        """Generate a coordinate-based clue."""
        # Split path for coordinates
        path_parts = target_node.path.split('/')
        if len(path_parts) >= 2:
            x, y = path_parts[-2], path_parts[-1]
        else:
            x, y = "target", target_node.name
        
        clue_templates = [
            f"The coordinates are marked: X={x}, Y={y}",
            f"Ancient map shows location at ({x}, {y})",
            f"The compass points to coordinates: {x} by {y}",
            f"Treasure lies where {x} meets {y}"
        ]
        
        return random.choice(clue_templates)
    
    def _generate_riddle_clue(self, target_name: str) -> str:
        """Generate a riddle clue."""
        riddle_templates = [
            f"I am not shallow but ___. I am not new but ___. Seek the {target_name}.",
            f"Where {target_name} dwells, wisdom flows. Look where the ancients chose.",
            f"Three letters start my name, {target_name[0:3].upper()}. Find where I remain.",
            f"Neither high nor low, but where {target_name} grows."
        ]
        
        return random.choice(riddle_templates)
    
    def _generate_pattern_clue(self, target_name: str) -> str:
        """Generate a pattern-based clue."""
        pattern_templates = [
            f"The pattern spells: {' '.join(target_name.upper())}",
            f"Follow the sequence to: {target_name.upper()}",
            f"The symbols form: {'-'.join(target_name.upper())}",
            f"Decoded pattern reveals: {target_name.upper()}"
        ]
        
        return random.choice(pattern_templates)
    
    def _generate_math_clue(self, target_name: str) -> str:
        """Generate a math-based clue."""
        # Simple math that gives letters
        letter_values = {chr(i): i-64 for i in range(65, 91)}  # A=1, B=2, etc.
        
        if target_name and target_name[0].upper() in letter_values:
            target_value = letter_values[target_name[0].upper()]
            equation = f"{target_value * 2} ÷ 2 = {target_value} = {target_name[0].upper()}"
            return f"Solve: {equation}. First letter of your destination."
        
        return f"Calculate the path to {target_name.upper()}"
    
    def _generate_logic_clue(self, target_name: str) -> str:
        """Generate a logic puzzle clue."""
        logic_templates = [
            f"If not A and not B, then {target_name.upper()}",
            f"The path of exclusion leads to {target_name.upper()}",
            f"When all else fails, seek {target_name.upper()}",
            f"The logical conclusion: {target_name.upper()}"
        ]
        
        return random.choice(logic_templates)
    

    
    def _add_red_herrings(self):
        """Add misleading clues and fake treasures."""
        red_herring_nodes = [node for node in self.all_nodes if node.red_herring]
        
        fake_treasures = ["fool's_gold.txt", "empty_chest.txt", "broken_relic.txt", "false_idol.txt"]
        misleading_clues = [
            "This path leads nowhere useful.",
            "A dead end disguised as progress.",
            "You're going in circles. Turn back.",
            "This treasure is just an illusion.",
            "The real prize lies elsewhere."
        ]
        
        for node in red_herring_nodes:
            if random.random() < 0.3:  # 30% chance of fake treasure
                fake_treasure = random.choice(fake_treasures)
                node.files[fake_treasure] = "❌ This is not the real treasure! Keep searching elsewhere."
            
            if random.random() < 0.5:  # 50% chance of misleading clue
                clue_file = f"misleading_clue_{random.randint(1,9)}.txt"
                node.files[clue_file] = random.choice(misleading_clues)
    
    def _generate_treasure_text(self) -> str:
        """Generate the final treasure text."""
        theme_data = self.themes[self.config.theme]
        treasure_name = random.choice(theme_data["treasures"])
        
        return f"""🏆 CONGRATULATIONS! You found the {treasure_name}! 🏆

The legendary treasure has been claimed by a worthy explorer.
This {treasure_name.lower().replace('_', ' ')} grants great power to its finder.

You have successfully navigated the procedural maze and proven your intelligence!

Maze Statistics:
- Depth: {self.config.depth} levels
- Theme: {self.config.theme}
- Difficulty: {self.config.difficulty.value}
- Branching Factor: {self.config.branching_factor}
"""
    
    def _create_file_system(self, root: MazeNode, base_path: Path):
        """Create the actual file system from the maze tree."""
        import shutil
        
        # Clean up existing maze
        if base_path.exists():
            shutil.rmtree(base_path)
        
        # Create directories and files
        def create_node(node: MazeNode, current_path: Path):
            current_path.mkdir(parents=True, exist_ok=True)
            
            # Create files for this node
            for filename, content in node.files.items():
                (current_path / filename).write_text(content)
            
            # Create child directories
            for child in node.children:
                child_path = current_path / child.name
                create_node(child, child_path)
        
        create_node(root, base_path)
    
    def get_solution_path(self) -> List[str]:
        """Get the solution path through the maze."""
        return self.treasure_path.copy()
    
    def get_maze_stats(self) -> Dict[str, Any]:
        """Get statistics about the generated maze."""
        treasure_nodes = len([n for n in self.all_nodes if n.is_treasure_path])
        red_herring_nodes = len([n for n in self.all_nodes if n.red_herring])
        total_files = sum(len(node.files) for node in self.all_nodes)
        
        return {
            "total_nodes": len(self.all_nodes),
            "treasure_path_nodes": treasure_nodes,
            "red_herring_nodes": red_herring_nodes,
            "total_files": total_files,
            "max_depth": self.config.depth,
            "theme": self.config.theme,
            "solution_path": self.treasure_path
        }


# Example usage and testing
if __name__ == "__main__":
    print("🎲 Procedural Maze Generator Test")
    print("=" * 40)
    
    # Test different configurations
    configs = [
        MazeConfig(depth=3, difficulty=DifficultyLevel.EASY, theme="fantasy"),
        MazeConfig(depth=5, difficulty=DifficultyLevel.MEDIUM, theme="sci-fi"),
        MazeConfig(depth=7, difficulty=DifficultyLevel.HARD, theme="mystery", enable_math=True),
    ]
    
    for i, config in enumerate(configs, 1):
        print(f"\nTest {i}: {config.difficulty.value.upper()} {config.theme.upper()} maze")
        
        generator = ProceduralMazeGenerator(config)
        root = generator.generate_maze(f"./test_maze_{i}")

        stats = generator.get_maze_stats()
        print(f"Stats: {stats['total_nodes']} nodes, {stats['total_files']} files")
        print(f"Solution: {' → '.join(stats['solution_path'])}")
        
        print("Maze generated successfully!") 
