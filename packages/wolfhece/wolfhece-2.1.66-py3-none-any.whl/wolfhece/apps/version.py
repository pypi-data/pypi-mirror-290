
class WolfVersion():

    def __init__(self):

        self.major = 2
        self.minor = 1
        self.patch = 66

    def __str__(self):

        return self.get_version()

    def get_version(self):

        return f'{self.major}.{self.minor}.{self.patch}'

    def print_version(self):

        print(f'WolfHece version {self.major}.{self.minor}.{self.patch}')
