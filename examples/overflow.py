from typing import List
from quo import Console, OverflowMethod

console = Console(width=14)
supercali = "supercalifragilisticexpialidocious"

overflow_methods: List[OverflowMethod] = ["fold", "crop", "ellipsis"]
for overflow in overflow_methods:
    console.rule(overflow)
    console.echo(supercali, overflow=overflow, style="bold blue")
    console.echo()
