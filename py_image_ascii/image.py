import PIL

class Image:
    def __init__(self, file) -> None:
        self.image = PIL.Image.open(file)
