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
button_width = 0.05
for i, simnr in enumerate(simnr_values):

        # create the axes for the button
        _ax = f.add_axes([0.1 + i * 1.1 * button_width, 0.1, button_width, button_width])

        # create the button
        sim_buttons += [w.Button(_ax, str(simnr), color='b', hovercolor='r')]

ax._widgets += sim_buttons  # avoids garbage collection

# define the callback


def callback(event):
    sim_button_states = [_b.active for _b in sim_buttons]
    selected_values = np.array(simnr_values)[sim_button_states]

    # delete all simulation lines (keeping the observational line)

    for _line in ax.get_lines()[1:]:
        del(_line)

    # plot all lines that match the selected values

    for d in data:
        if d[0] in selected_values:
            ax.plot(d[-2], d[-1])

    plt.draw()


# now link the callback to the buttons

for _b in sim_buttons:
    _b.on_clicked(callback)


plt.show()
