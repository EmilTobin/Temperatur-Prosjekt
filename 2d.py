import numpy as np
import matplotlib.pyplot as plt
import math

# Dimensioner av nätet
n = 80
rad, kol = n, n
T_o = 5
alfa = 2.5 / n  # utgångspunk är 0.5 för n = 5, gjort funktion så alfa relaterar till avståndet mellan punkterna
thöger = 80  # Här kan du variera temperaturen för högerkanten

# Skapa koefficientmatrisen och höger sidan
A = np.zeros((rad * kol, rad * kol))
b = np.zeros(rad * kol)

mittpunkt = (rad // 2) * kol + kol // 2


# Definiera ekvationerna för varje punkt i nätet
def räkna_temp():
    """Skapar koeefficientmatris samt sätter värden på b-vektorn."""
    for i in range(rad):
        for j in range(kol):
            index = i * n + j

            if (i == 0 and j == 0) or (i == rad - 1 and j == 0):
                # Hörn
                A[index, index] = 4 + alfa
                if i == 0 and j == 0:  # Övre vänstra hörnet
                    A[index, index + 1] = -2
                    A[index, index + kol] = -2

                elif i == rad - 1 and j == 0:  # Nedre vänstra hörnet
                    A[index, index + 1] = -2
                    A[index, index - kol] = -2

                b[index] = T_o * alfa

            elif j == kol - 1:  # Högerkanten
                A[index, index] = 1
                b[index] = 0  # Placeholder, ska justeras senare

            else:  # punkter i mitten
                A[index, index] = 4
                if i > 0:  # Ovanför
                    A[index, index - kol] = -1
                if i < rad - 1:  # Nedanför
                    A[index, index + kol] = -1
                if j > 0:  # Vänster
                    A[index, index - 1] = -1
                if j < kol - 1:  # Höger
                    A[index, index + 1] = -1

                # Kanter, ej hörn
                if i == 0 or i == rad - 1 or j == 0:
                    if (i == 0 and 0 < j < kol - 1) or (i == rad - 1 and 0 < j < kol - 1):  # Övre och nedre kanten
                        A[index, index] = 4 + alfa
                        A[index, index + 1] = -1  # Tsida1
                        A[index, index - 1] = -1  # Tsida2
                        if i == 0:
                            A[index, index + kol] = -2  # Tin
                        else:
                            A[index, index - kol] = -2  # Tin
                        b[index] = T_o * alfa

                    if j == 0 and 0 < i < rad - 1:  # Vänstra kanten
                        A[index, index] = 4 + alfa
                        A[index, index + kol] = -1  # Tsida1
                        A[index, index - kol] = -1  # Tsida2
                        A[index, index + 1] = -2  # Tin
                        b[index] = T_o * alfa


# Funktion för att ställa in och beräkna temperaturerna
def ställ_in_temp_högerkant(thöger):
    """Ställer in högerkantens temperatur korrekt i b-vektorn."""
    for i in range(rad):
        index = i * kol + (kol - 1)
        b[index] = thöger

    # Lös systemet av linjära ekvationer
    temperaturer = np.linalg.solve(A, b)

    # Beräkna temperaturen i mitten
    temp_mittpunkt = temperaturer[mittpunkt]

    # Återskapa den fullständiga 2D-matrisen
    temperatur_grid = temperaturer.reshape((rad, kol))

    return temperatur_grid, temp_mittpunkt


# Räkna ut temperaturen för varje punkt i nätet
räkna_temp()

# Beräkna temperaturfördelningen med den angivna högerkantstemperaturen
temperatur_grid, temp_mittpunkt = ställ_in_temp_högerkant(thöger)

# Skriv ut resultaten
print(f"Använd högerkantstemperatur: {thöger}°C")
print(f"Temperaturen i mitten är: {temp_mittpunkt:.2f}°C")


def plotta(grid, temp_kant):
    """Visar temperaturnätet som en värmekarta och skriver ut högerkantens temperatur."""
    plt.imshow(grid, cmap='hot', interpolation='bilinear')
    plt.colorbar(label='Temperatur (°C)')
    plt.title(
        f'2D Temperatur Distribution\nHögerkantens Temperatur: {temp_kant:.2f}°C\nMittens temperatur: {temp_mittpunkt:.2f}')
    plt.show()


# Plotta det beräknade temperaturfördelningen
plotta(temperatur_grid, thöger)

