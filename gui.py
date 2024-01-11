from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap, QColor, QImage
import sys
import neural_network


class Example(QWidget):
    def __init__(self):
        super().__init__()

        # Poziomy układ dla obrazów i przycisków
        hbox = QHBoxLayout()

        # Pionowy układ dla przycisków
        vbox = QVBoxLayout()

        # Etykiety dla obrazów
        self.label1 = QLabel(self)
        self.label2 = QLabel(self)

        # Przyciski
        button1 = QPushButton('Test', self)
        button2 = QPushButton('Drzewo', self)
        button3 = QPushButton('Odszumiaj', self)
        button4 = QPushButton('Wyjście na Wejście', self)
        button5 = QPushButton('Przetwarzaj Obraz', self)
        button6 = QPushButton('Trening', self)

        # Łączenie przycisków z funkcjami
        button1.clicked.connect(self.load_dom_images)
        button2.clicked.connect(self.load_drzewo_images)
        # button3.clicked.connect(self.)
        button4.clicked.connect(self.copy_image_from_label2_to_label1)
        button5.clicked.connect(lambda: neural_network.trening(self.process_image("label1"),
                                                               self.process_image("lebel2")))
        # button6.clicked.connect(neural_network.trening(*self.odszumaj()))

        # Dodawanie widżetów do układów
        hbox.addWidget(self.label1)
        hbox.addWidget(self.label2)
        vbox.addWidget(button1)
        vbox.addWidget(button2)
        vbox.addWidget(button3)
        vbox.addWidget(button4)
        vbox.addWidget(button5)
        vbox.addWidget(button6)

        # Dodawanie układu pionowego do poziomego
        hbox.addLayout(vbox)

        # Ustawienie układu dla okna
        self.setLayout(hbox)
        self.setWindowTitle('Przykład PyQt')
        self.setGeometry(300, 300, 300, 200)

    def load_dom_images(self):
        # Ładowanie obrazów 'Dom'
        self.label1.setPixmap(QPixmap('test.png'))
        self.label2.setPixmap(QPixmap('test_szum.png'))

    def load_drzewo_images(self):
        # Ładowanie obrazów 'Drzewo'
        self.label1.setPixmap(QPixmap('Drzewo.png'))
        self.label2.setPixmap(QPixmap('Drzewo_Szum.png'))

    def copy_image_from_label2_to_label1(self):
        # Kopiowanie obrazu z label2 do label1
        self.label1.setPixmap(self.label2.pixmap())

    def process_image(self, label_name):
        # Wybór odpowiedniego labela
        label = self.label1 if label_name == 'label1' else self.label2

        # Konwersja pixmapy do obiektu QImage
        image = label.pixmap().toImage()
        # Pusta tablica do przechowywania kolorów pikseli
        pixel_colors = []

        # Przechodzenie przez każdy piksel obrazu
        for x in range(image.width()):
            for y in range(image.height()):
                color = image.pixelColor(x, y)
                pixel_colors.append((color.red(), color.green(), color.blue()))

        # W tym miejscu 'pixel_colors' zawiera kolory wszystkich pikseli
        # print(image.width(), image.height())
        # print(pixel_colors[0:25])
        return pixel_colors

    def create_image_from_pixels(pixel_values):
        width = 50
        height = 50
        # Utworzenie pustego obrazu o wymiarach width x height
        image = QImage(width, height, QImage.Format_RGB32)
        if len(pixel_values) != width * height:
            print("Liczba pikseli w tablicy nie odpowiada wymiarom obrazu.")
            return None

        # Wypełnienie obrazu kolorami z tablicy
        for y in range(height):
            for x in range(width):
                # Obliczenie indeksu dla jednowymiarowej tablicy
                index = y * width + x
                # Pobranie koloru (R, G, B) z tablicy
                color = QColor(*pixel_values[index])
                # Ustawienie koloru piksela
                image.setPixelColor(x, y, color)
                pixmap = QPixmap.fromImage(image)
                pixel_values.label2.setPixmap(pixmap)
                print("1")
                QApplication.processEvents()

        return image


def run():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
