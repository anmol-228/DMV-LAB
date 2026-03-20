import numpy as np
import matplotlib.pyplot as plt

print("=== Complete Graph Generator ===")

n = int(input("Enter number of vertices (greater than 3): "))

if n <= 3:
    print("Number of vertices must be greater than 3")
else:
    plt.figure(figsize=(6, 6))
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    points = np.column_stack((np.cos(angles), np.sin(angles)))

    for i in range(n):
        for j in range(i + 1, n):
            plt.plot(
                [points[i, 0], points[j, 0]],
                [points[i, 1], points[j, 1]],
                color="gray",
                linewidth=0.8,
                alpha=0.7,
            )

    plt.scatter(points[:, 0], points[:, 1], s=800, color="skyblue", edgecolors="black")

    for idx, (x_pos, y_pos) in enumerate(points):
        plt.text(x_pos, y_pos, str(idx), ha="center", va="center", fontsize=12)

    plt.title(f"Complete Graph with {n} Vertices")
    plt.axis("off")
    plt.gca().set_aspect("equal")
    plt.show()
