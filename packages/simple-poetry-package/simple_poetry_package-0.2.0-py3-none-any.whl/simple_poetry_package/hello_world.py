class HelloWorld:

    name: str

    def __init__(self, name: str) -> None:
        self.name = name

    def print_name(self) -> None:
        print(f"Welcome to world: {self.name}")

    def get_name(self) -> str:
        return self.name
