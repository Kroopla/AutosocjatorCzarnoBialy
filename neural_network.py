import numpy as np
import pickle


class LinearPixelMachine:
    def __init__(self):
        self.weights = np.random.rand(3)  # trzy wagi dla R, G, B
        self.bias = np.random.rand(3)  # trzy biasy dla R, G, B

    def train(self, input_pixel, true_pixel, epochs, learning_rate):
        for _ in range(epochs):
            prediction = self.predict(input_pixel)
            error = true_pixel - prediction
            self.weights += learning_rate * error * input_pixel
            self.bias += learning_rate * error

    def predict(self, input_pixel):
        return input_pixel * self.weights + self.bias

    def threshold(self, prediction):
        # Suma wartości RGB i porównanie z trzykrotnością połowy maksymalnej wartości
        return np.where(prediction.sum() > (3 * 0.5), 1, 0)  # Prog 1.5, gdzie 3 to liczba kanałów


def trening(pixels, bad_pixels):
    assert len(pixels) == len(bad_pixels), "Listy 'pixels' i 'bad_pixels' muszą mieć tę samą długość"
    # Tworzenie i trenowanie maszyn liniowych dla każdego piksela
    pixel_machines = [LinearPixelMachine() for _ in pixels]
    for i, (pixel, bad_pixel) in enumerate(zip(pixels, bad_pixels)):
        pixel_machines[i].train(np.array(bad_pixel) / 255.0, np.array(pixel) / 255.0, epochs=1000, learning_rate=0.1)
        if i % 50 == 0:
            print(f"Pixel {i}, RGB: {pixel}")

    # Zapisanie wytrenowanych maszyn do pliku
    with open('trained_pixel_machines.pkl', 'wb') as file:
        pickle.dump(pixel_machines, file)
    print("Koniec Treningu")


def przetwarzaj(pixeltest):
    # Odczytanie wytrenowanych maszyn z pliku
    with open('trained_pixel_machines.pkl', 'rb') as file:
        trained_pixel_machines = pickle.load(file)

    # Przewidywane kolorry dla każdego piksela
    predicted_pixels = [machine.threshold(machine.predict(np.array(pixel) / 255.0)) for machine, pixel in
                        zip(trained_pixel_machines, pixeltest)]
    predicted_pixels = np.array(predicted_pixels) * 255  # Odwrotna normalizacja i ograniczenie wartości

    # Przedstawienie odtworzonych pikseli
    predicted_pixels_arranged = [(p, p, p) for p in predicted_pixels]
    print("Obraz otrzymany:")
    print(predicted_pixels_arranged)

    # Zapisanie odtworzonych pikseli do pliku tekstowego
    with open('predicted_pixels_arranged.txt', 'w') as file:
        for pixel in predicted_pixels_arranged:
            file.write(f'{pixel}\n')
