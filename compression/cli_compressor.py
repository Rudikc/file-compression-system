from compression.compressor import Compressor


class CliCompressor(Compressor):
    def __init__(self, files, output, direction, password=None, algorithm=None):
        super().__init__()
        self.files = files
        self.algorithm = algorithm
        self.output = output
        self.password = password
        self.direction = direction

    def run(self):
        if self.direction == "compress":
            self.compress(self.files, self.algorithm, self.output, self.password)
        elif self.direction == "decompress":
            self.decompress(self.files[0], self.output, self.password)
        else:
            print("Invalid direction. Please choose 'compress' or 'decompress'")
            return
