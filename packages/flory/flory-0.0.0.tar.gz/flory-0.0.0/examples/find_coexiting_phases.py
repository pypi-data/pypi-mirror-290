import flory

chis = [[0, 4.0], [4.0, 0]]
phi_means = [0.5, 0.5]

volumes, phis = flory.find_coexisting_phases(chis, phi_means, 16)

with open(__file__ + ".out", "w") as f:
    print("Volumes:", volumes, file=f)
    print("Compositons:", phis, file=f)