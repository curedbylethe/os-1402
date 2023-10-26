class Interface:
    number_of_homeworks = 1
    homeworks = [["Fetching weather", "Generating Processes"], ]

    def __init__(self):
        pass

    def print_homeworks(self):
        print("Hi, which homework task are you checking?!")
        for i in range(self.number_of_homeworks):
            print(f"{i + 1}. HW{i + 1}")

    def print_problems(self, homework_number: int):
        print(f"HW{homework_number} had {len(self.homeworks[homework_number - 1])} " 
              "problems, which one are you interested in?")
        for i in range(len(self.homeworks[homework_number - 1])):
            print(f"{i + 1}. {self.homeworks[homework_number - 1][i]}")

    @classmethod
    def handle_hw1(cls, problem_number: int):
        if problem_number == 1:
            print("Fetching weather for Iranian cities...")
            from hw1.fetch import fetch
            fetch()
        elif problem_number == 2:
            print("Generating processes isn't implemented yet!")
        else:
            print("Invalid problem number!")

    def run(self):
        self.print_homeworks()
        homework_number = int(input("Enter the number of the task: "))
        self.print_problems(homework_number)
        problem_number = int(input("Enter the number of the problem: "))
        if homework_number == 1:
            self.handle_hw1(problem_number)
        else:
            print("Invalid homework number!")
