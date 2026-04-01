import numpy as np
import matplotlib.pyplot as plt

# Dimensioner av nätet
n = 20
rad, kol, höjd = n, n, n
T_o = 0
alfasida = 0.375
alfatop = 0.425
thöger = 76  # Här kan du variera temperaturen för högerkanten

# Skapa koefficientmatrisen och höger sidan
A = np.zeros((rad * kol * höjd, rad * kol * höjd))
b = np.zeros(rad * kol * höjd)

mittpunkt = (rad // 2) * kol * höjd + (kol // 2) * höjd + höjd // 2
toppen_mittpunkt = ((rad // 2) * kol * höjd + (kol // 2) * höjd + höjd - 1)


# Definiera ekvationerna för varje punkt i nätet
def räkna_temp():
    for i in range(rad):
        for j in range(kol):
            for k in range(höjd):
                index = i * kol * höjd + j * höjd + k

                # Hörn
                if (i == 0 and j == 0 and k == 0) or (i == rad - 1 and j == 0 and k == 0) \
                        or (i == 0 and j == 0 and k == höjd - 1) or (i == rad - 1 and j == 0 and k == höjd - 1):
                    A[index, index] = 6 + alfasida

                    if i == 0 and j == 0 and k == 0:  # Övre vänstra hörnet fram
                        A[index, index + 1] = -2
                        A[index, index + kol] = -2
                        A[index, index + kol * höjd] = -2

                    elif i == rad - 2 and j == 0 and k == 0:  # Nedre vänstra hörnet fram
                        A[index, index + 1] = -2
                        A[index, index - kol] = -2
                        A[index, index + kol * höjd] = -2

                    elif i == 0 and j == 0 and k == höjd - 1:  # Övre vänstra hörnet bak
                        A[index, index - 1] = -2
                        A[index, index + kol] = -2
                        A[index, index + kol * höjd] = -2

                    elif i == rad - 2 and j == 0 and k == höjd - 1:  # Nedre vänstra hörnet bak
                        A[index, index - 1] = -2
                        A[index, index - kol] = -2
                        A[index, index + kol * höjd] = -2

                    b[index] = T_o * alfasida

                # 'sidohörn'
                elif (i == 0 and j == 0 and 0 < k < höjd - 1):
                    A[index, index] = 6 + alfasida
                    A[index, index - 1] = -1
                    A[index, index + 1] = -1
                    A[index, index + kol] = -2
                    A[index, index + kol * höjd] = -2
                    b[index] = T_o * alfasida

                elif (i == rad - 1 and j == 0 and 0 < k < höjd - 1):
                    A[index, index] = 6 + alfasida
                    A[index, index - 1] = -1
                    A[index, index + 1] = -1
                    A[index, index + kol] = -2
                    A[index, index - kol * höjd] = -2
                    b[index] = T_o * alfasida


                # varma kanten
                elif j == kol - 1:  # Högerkanten
                    A[index, index] = 1
                    b[index] = thöger

                    # Kanter, ej hörn

                elif (i == 0 and 0 < j < kol - 1 and 0 < k < höjd - 1) or (
                        i == rad - 1 and 0 < j < kol - 1 and 0 < k < höjd - 1):  # fram och bak kanten
                    A[index, index] = 6 + alfasida
                    A[index, index + 1] = -1  # Tsida1
                    A[index, index - 1] = -1  # Tsida2
                    A[index, index + kol] = -1
                    A[index, index - kol] = -1
                    if i == 0:
                        A[index, index + kol * höjd] = -2  # Tin
                    else:
                        A[index, index - kol * höjd] = -2  # Tin
                    b[index] = T_o * alfasida

                elif j == 0 and 0 < i < rad - 1 and 0 < k < höjd - 1:  # Vänstra kanten
                    A[index, index] = 6 + alfasida
                    A[index, index + 1] = -1  # Tsida1
                    A[index, index - 1] = -1  # Tsida2
                    A[index, index + höjd] = -1
                    A[index, index - höjd] = -1
                    A[index, index + kol * höjd] = -2
                    b[index] = T_o * alfasida

                # toppen
                elif k == höjd - 1:
                    A[index, index] = 6 + alfatop
                    if j > 0:
                        A[index, index - höjd] = -1
                    if j < kol - 1:
                        A[index, index + höjd] = -1
                    if i > 0:
                        A[index, index - kol * höjd] = -1
                    if i < rad - 1:
                        A[index, index + kol * höjd] = -1
                    A[index, index - 1] = -2
                    b[index] = T_o * alfatop

                # botten
                elif k == 0:
                    A[index, index] = 6
                    if j > 0:
                        A[index, index - höjd] = -1
                    if j < kol - 1:
                        A[index, index + höjd] = -1
                    if i > 0:
                        A[index, index - kol * höjd] = -1
                    if i < höjd - 1:
                        A[index, index + kol * höjd] = -1
                    A[index, index + 1] = -2
                    b[index] = 0


                else:  # punkter i mitten
                    A[index, index] = 6
                    if i > 0:  # framför
                        A[index, index - kol * höjd] = -1
                    if i < rad - 1:  # bakom
                        A[index, index + kol * höjd] = -1
                    if j > 0:  # Vänster
                        A[index, index - höjd] = -1
                    if j < kol - 1:  # Höger
                        A[index, index + höjd] = -1
                    if k > 0:  # ovanför
                        A[index, index - 1] = -1
                    if k < höjd - 1:  # under
                        A[index, index + 1] = -1


# Funktion för att ställa in och beräkna temperaturerna
def ställ_in_temp_högerkant(thöger):
    for i in range(rad):
        for j in range(kol):
            index = i * kol * höjd + (kol - 1) * höjd + j
            b[index] = thöger
    # Lös systemet av linjära ekvationer
    print(A)

    temperaturer = np.linalg.solve(A, b)
    print(temperaturer)

    # Beräkna temperaturen i mitten
    temp_mittpunkt = temperaturer[mittpunkt]
    temp_topp_mitt = temperaturer[toppen_mittpunkt]

    # Återskapa den fullständiga 2D-matrisen
    temperatur_grid = temperaturer.reshape((rad, kol, höjd))

    return temperatur_grid, temp_mittpunkt, temp_topp_mitt


# Räkna ut temperaturen för varje punkt i nätet
räkna_temp()
# Beräkna temperaturfördelningen med den angivna högerkantstemperaturen
temperatur_grid, temp_mittpunkt, temp_topp_mitt = ställ_in_temp_högerkant(thöger)

# Skriv ut resultaten
print(f"Använd högerkantstemperatur: {thöger}°C")
print(f"Temperaturen i mitten är: {temp_mittpunkt:.2f}°C")

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')
sc = None


def plotta(grid, temp_kant, temp_mitt):
    """Visar temperaturnätet som en värmekarta och skriver ut högerkantens temperatur."""
    global sc
    ax.clear()

    x, y, z = np.meshgrid(range(grid.shape[0]), range(grid.shape[1]), range(grid.shape[2]))

    x_rot = y
    y_rot = x
    z_rot = z
    x_rot = x_rot.flatten()
    y_rot = y_rot.flatten()
    z_rot = z_rot.flatten()
    c = grid.flatten()

    sc = ax.scatter(x_rot, y_rot, z_rot, c=c, cmap='hot', alpha=0.99)

    if not hasattr(plotta, 'colorbar') or plotta.colobar is None:
        plotta.colorbar = plt.colorbar(sc, ax=ax, label='Temperatur (°C)')
    else:
        sc.set_array(c)

    ax.invert_yaxis()
    plt.title(
        f'3D Temperatur Distribution\nHögerkantens Temperatur: {temp_kant:.2f}°C, Mittens temperatur: {temp_mitt:.2f} °C\n Yttemperatur:{temp_topp_mitt:.2f} °C')
    plt.show()


# Plotta det beräknade temperaturfördelningen
plotta(temperatur_grid, thöger, temp_mittpunkt)