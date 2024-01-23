# %%
import random
from typing import List

import numpy as np

# fmt: off
COLORS = [
    "red", "blue", "green", "yellow", "black", "white", "purple", "orange", "pink", "gray",
    "brown", "cyan", "magenta", "lime", "olive", "navy", "teal", "maroon", "violet", "gold",
    "silver", "beige", "coral", "peach", "turquoise", "tan", "lavender", "indigo", "charcoal", "azure",
    "amber", "emerald", "jade", "bronze", "plum", "orchid", "mint", "ivory", "burgundy", "raspberry",
    "rose", "mustard", "slate", "cobalt", "ruby", "saffron", "crimson", "fuchsia", "mauve"
]

ADJECTIVES = [
    "fast", "slow", "hot", "cold", "dry", "wet", "soft", "big", "small", "short", "high", "low",
    "near", "far", "deep", "flat", "old", "new", "good", "bad", "sad", "happy", "easy", "hard",
    "dark", "light", "early", "late", "loud", "quiet", "bright", "dull", "busy", "lazy", "rich",
    "poor", "thin", "tight", "loose", "full", "empty", "strong", "weak", "clean",
    "heavy", "safe", "risky", "wide", "narrow", "rare", "common", "fine", "sharp",
    "blunt", "flat", "round", "tall", "short", "huge", "tiny", "kind", "mean", "brave", "shy", 
    "calm", "wild", "firm", "gentle", "warm", "cool", "fresh", "stale", "clear", "foggy", "sweet",
    "sour", "bitter", "salty", "plain", "fancy", "simple", "neat", "messy", "quick", "slow",
    "bright", "dim", "young", "fun", "near", "far", "loud", "silent", "smooth",
    "rough", "solid", "liquid",
]

ING_WORDS = [
    "amazing", "charming", "dazzling", "exciting", "glowing", "laughing",  "shining",
     "climbing", "jumping", "marching", "napping", "singing", "twirling",
    "zooming", "grinning", "waving", "painting", "reading", "dancing",
]

ANIMALS = [
    "dog", "cat", "fish", "bird", "fox", "bear", "lion", "wolf", "horse", "frog",
    "deer", "owl", "rat", "bat", "hare", "boar", "mole", "seal", "hawk", "crow",
    "toad", "duck", "goat", "swan", "mule", "moose", "lark", "wasp", "bull", "calf",
    "crab", "dove", "eagle", "finch", "guppy", "heron", "ibis", "jay", "kiwi", "lemur",
    "lynx", "newt", "orca", "pike", "quail", "raven", "shark", "tiger", "urchin", "viper",
    "whale", "yak", "zebra", "ant", "ape", "bee", "boar", "clam", "crab", "dove",
    "elk", "gull", "hawk", "ibex", "joey", "kite", "llama", "mite", "otter",
    "panda", "ram", "sloth", "snail", "tapir", "turtle", "vole", "wombat", "zebu",
    "adder", "bison", "dingo", "eagle", "ferret", "gecko", "hyena", "impala", "jackal",
    "koala", "lemur", "macaw", "nymph", "ocelot", "python", "quetzal", "rhino", "squid", "toucan", 
]

FOODS = [
    "apple", "banana", "pear", "peach", "grape", "melon", "berry", "lemon", "lime",
    "kiwi", "plum", "mango", "papaya", "grapefruit", "apricot",
    "bread", "rice", "pasta", "pizza", "burger", "steak", "chicken", "pork", "bacon", "ham",
    "fish", "shrimp", "crab", "lobster", "oyster", "salmon", "tuna", "trout", "mackerel", "sardine",
    "egg", "cheese", "milk", "yogurt", "butter", "tofu", "honey", "sugar",
    "salt", "pepper", "garlic", "onion", "carrot", "potato", "tomato", "cucumber", "lettuce", "spinach",
    "kale", "cabbage", "broccoli", "mushroom", "peas", "bean", "corn", "squash", "zucchini",
    "rice", "quinoa", "oat", "wheat", "barley", "rye", "noodle", "soup", "stew", "curry",
    "salad", "sandwich", "taco", "burrito", "wrap", "pancake", "waffle", "scone", "cake", "pie",
    "cookie", "brownie", "donut", "pudding", "chocolate",
]

SIMPLE_NOUNS = [
    "cat", "dog", "house", "car", "tree", "book", "phone", "ball", "shoe", "door",
    "window", "chair", "table", "light", "road", "river", "sky", "sun", "moon", "star",
    "bird", "fish", "mouse", "forest", "mountain", "beach", "sand", "wave", "grass", "flower",
    "fruit", "leaf", "branch", "root", "seed", "soil", "rain", "snow", "wind", "cloud",
    "hill", "lake", "sea", "ocean", "island", "field", "farm", "garden", "park", "yard",
    "street", "town", "city", "country", "earth", "world", "space", "universe", "fire", "ice",
    "water", "air", "smoke", "steam", "rock", "stone", "metal", "iron", "gold", "silver",
    "copper", "wood", "cloth", "paper", "glass", "plastic", "leather", "wool", "silk",
    "oil", "gas", "fuel", "energy", "heat", "light", "sound", "voice", "word",
    "eye", "ear", "nose", "hand", "foot", "heart","quasar", "neutron", "atom", "molecule",
]
# fmt: on

ALL_ADJECTIVES = np.unique(ADJECTIVES + COLORS + ING_WORDS)
ALL_NOUNS = np.unique(ANIMALS + FOODS + SIMPLE_NOUNS)

MAX_TRIES = 1000


class RandomNameGenerator:
    def __init__(self, random_seed: int = 1) -> None:
        random.seed(random_seed)
        self.random_seed = random_seed
        self.used_names: List[str] = []

    def new_name(self) -> str:
        for i in range(MAX_TRIES):
            random_adjective = random.choice(ALL_ADJECTIVES)
            random_noun = random.choice(ALL_NOUNS)
            random_name = f"{random_adjective.capitalize()}{random_noun.capitalize()}"
            if random_name not in self.used_names:
                self.used_names.append(random_name)
                return random_name
            print("USED")
        raise ValueError(f"Could not generate a new name after {MAX_TRIES} tries.")


if __name__ == "__main__":
    generator = RandomNameGenerator(1000 * 128)
    for i in range(10):
        print(generator.new_name())
