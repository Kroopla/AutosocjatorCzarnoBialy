from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap, QColor, QImage
import sys
import neural_network
import re


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
        button3.clicked.connect(self.aktualizuj_label2)
        button4.clicked.connect(self.copy_image_from_label2_to_label1)
        button5.clicked.connect(lambda: neural_network.przetwarzaj(self.process_image("lebel2")))
        button6.clicked.connect(
            lambda: neural_network.trening(self.process_training(False), self.process_training(True)))

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
        # self.label1.setPixmap(QPixmap('150.png'))
        # self.label2.setPixmap(QPixmap('150_szum.png'))

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
        print("Obraz wysyłany:")
        print(pixel_colors)
        return pixel_colors

    def process_training(self, has_humid):
        filenames = []
        if has_humid:
            filenames = ['test.png', '2.png', '3.png', '4.png', '5.png']
            else filenames = ['test_szum.png', '2.png_szum', '3.png_szum', '4_szum.png', '5_szum.png']
        all_pixel_colors = []
        for filename in filenames:
            # Wczytanie obrazu z pliku
            image = QImage(filename)

            # Sprawdzenie, czy obraz został poprawnie wczytany
            if image.isNull():
                print(f"Nie udało się wczytać obrazu: {filename}")
                continue

            # Pusta tablica do przechowywania kolorów pikseli dla tego obrazu
            pixel_colors = []

            # Przechodzenie przez każdy piksel obrazu
            for y in range(image.height()):
                for x in range(image.width()):
                    color = image.pixelColor(x, y)
                    all_pixel_colors.append((color.red(), color.green(), color.blue()))
            # Dodawanie kolorów pikseli tego obrazu do głównej listy
        # with open("all_pixel_colors", "w") as plik:
        #     plik.write(all_pixel_colors)
        print("test")
        return all_pixel_colors

    def aktualizuj_label2(self):
        file_path = 'predicted_pixels_arranged.txt'
        self.odszumiaj(self.label2, file_path)

    def odszumiaj(self, label, file_path):
        # Odczytanie wartości pikseli z pliku
        with open(file_path, 'r') as file:
            lines = file.readlines()

        pixel_values = []
        for line in lines:
            # Konwersja linii tekstu na krotkę RGB
            rgb_values = re.findall(r'\d+', line)
            if rgb_values and len(rgb_values) == 3:
                pixel_values.append(tuple(map(int, rgb_values)))

        # Tworzenie obrazu
        width, height = 50, 50
        image = QImage(width, height, QImage.Format_RGB32)

        if len(pixel_values) != width * height:
            print("Liczba pikseli w pliku nie odpowiada wymiarom obrazu 50x50.")
            return

        for y in range(width):
            for x in range(height):
                index = y * width + x
                color = QColor(*pixel_values[index])
                image.setPixelColor(y, x, color)

                # Aktualizacja label2 po każdej zmianie piksela
                pixmap = QPixmap.fromImage(image)
                label.setPixmap(pixmap)

                # Odświeżenie aplikacji, aby pokazać zmiany w czasie rzeczywistym
                QApplication.processEvents()


def run():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
