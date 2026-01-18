class Animal:
    def __init__(self):
        self.num_eye = 2

    def breath(self):
        print("inhale , exhale")
class Fish(Animal):
    def __init__(self):
        super().__init__()
    def breath(self):
        super().breath()
        print("doing this underwater")
    def swim(self):
        print("Moving in water.")

nemo = Fish()
nemo.swim()
nemo.breath()
print(nemo.num_eye)