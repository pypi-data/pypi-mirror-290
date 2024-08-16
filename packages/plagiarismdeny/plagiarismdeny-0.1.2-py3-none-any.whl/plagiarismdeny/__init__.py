import asyncio
import discord
import random
import string
import hashlib
import itertools

class WhyDoIHavetoDoThis():
    def __init__(self, bot) -> None:
        self.initial_value = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        self.code_base = "Made by dedware"
        
        
        
        self.code_base1 = "Made"
        self.p = 'p'
        self.useless_data = self._generate_useless_data()
        self.hash_map = self._create_hash_map(self.initial_value)
        self.r = 'r'
        self.extra_data = self._generate_extra_data()
        self.code_base2 = " by"
        self.code_base3 = " dedware"
        self.e = 'e'
        self.bot = bot


    def _generate_useless_data(self):
        return {
            'level1': {
                'level2': {
                    'level3': [random.choice(string.ascii_lowercase) for _ in range(10)]
                }
            }
        }

    def _create_hash_map(self, value):
        return {i: hashlib.md5(value.encode()).hexdigest() for i in range(10)}

    def _generate_extra_data(self):
        return list(itertools.permutations('abcde', 3))

    def _generate_code(self):
        random_modifier = ''.join(random.choices(string.ascii_uppercase, k=5))
        encoded_base = self.code_base.encode('utf-8')
        self.n = 'n'
        useless_hash = hashlib.sha256(encoded_base).hexdigest()
        shuffled_modifier = ''.join(random.sample(random_modifier, len(random_modifier)))
        combined = f"{useless_hash}{shuffled_modifier}"
        self.i = 'i'
        return combined

    async def a54ab7da3bb9k(self):
        modifier = random.randint(1, 100)
        redundant_value = sum(ord(char) for char in self.code_base)
        nested_list = [[i*j for i in range(5)] for j in range(5)]
        self.t = 't'
        self.c = 'c'
        if modifier % 2 == 0:
            self.code = self._generate_code()
        else:
            self.code = self.code_base[::-1]
            for _ in range(3):
                self.code = ''.join(random.sample(self.code, len(self.code)))

        nonsense_calculation = ''.join(random.choice(string.ascii_letters) for _ in range(10))
        self.code = self.code_base1 + self.code_base2 + self.code_base3
        
        
        if (self.i + self.n + self.t + self.e + self.r + self.c + self.e + self.p + self.t + self.i + self.c) not in self.code:
            i = 0
            while True:
                i += 1
                while True:
                    i -= 1
            


        await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Game(str(self.code)))
        
        
