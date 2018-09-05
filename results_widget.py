import matplotlib.pyplot as plt
import matplotlib.widgets as w
import numpy as np

# Get the data

data = []

with open('data.csv') as fid:
    while True:
        line = fid.readline()
        if line.strip().startswith('#'):
            continue

        if line.strip() == '':
            break

        line = line.strip().split(',')
        sim_nr = int(line.pop(0))
        alpha = float(line.pop(0))
        vf = float(line.pop(0))
        nr = int(line.pop(0))
        r = [float(line.pop(0)) for i in range(nr)]
        Inu = [float(line.pop(0)) for i in range(nr)]

        data += [[
            sim_nr,
            alpha,
            vf,
            nr,
            r,
            Inu
            ]]


# Make the figure

f = plt.figure()

ax = f.add_axes([0.1, 0.5, 0.5, 0.4])

# make up the isella profile

r_isella = [0.5, 3, 10, 15]
Inu_isella = [20, 10, 12, 8]

# plot the isella profile

ax.plot(r_isella, Inu_isella, 'k--')

# now we need to make a variable number of buttons

simnr_values = sorted(list(set([d[0] for d in data])))
alpha_values = sorted(list(set([d[1] for d in data])))
vf_values = sorted(list(set([d[2] for d in data])))

# to avoid garbage collection
ax._widgets = []

# create buttons

sim_buttons = []
button_width = 0.1

# create the axes for the button
_ax = f.add_axes([0.1, 0.1, button_width, len(simnr_values) * button_width])
sim_buttons = w.CheckButtons(_ax, [str(s) for s in simnr_values], [False for s in simnr_values])
for r in sim_buttons.rectangles:
    r.set_facecolor("blue")
    r.set_edgecolor("k")
    r.set_alpha(0.2)

ax._widgets += [sim_buttons]  # avoids garbage collection


def callback(event):
    """
    The callback for the simulation buttons
    """
    states = sim_buttons.get_status()
    selected_values = np.array(simnr_values)[states]

    # delete all simulation lines (keeping the observational line)

    for _line in ax.get_lines()[1:]:
        _line.remove()

    # plot all lines that match the selected values

    for d in data:
        if d[0] in selected_values:
            ax.plot(d[-2], d[-1])

    plt.draw()


# now link the callback to the buttons

sim_buttons.on_clicked(callback)


plt.show()
