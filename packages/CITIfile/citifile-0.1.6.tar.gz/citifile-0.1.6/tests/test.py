from CITIfile import read_citifile



# read file
data = read_citifile("data.citi")



# show coordinates and data variables

print('Coordinates:')
for cname in data.coords:
    cdata = data.coords[cname].data
    print(f'- {cname}: {len(cname)} ({cdata}, {cdata.dtype})')

print('Data:')
for vname in data.data_vars:
    vdata = data.data_vars[vname]
    print(f'- {vname}: {vdata.dtype}')



# extract usable 2D data; in this example, we extract S[1,1] vs. freq,
#   at some given coordinates for C_load and C_d2

# select the data variable at the given corrdinates
data_slice = data.data_vars["S[1,1]"].sel(L_load=20, C_d2=1)

# now there is only one coordinate (freq) left as independent variable
x = data_slice.coords["freq"].data

# dependent variable (Y-axis)
y = data_slice.data

for px, py in zip(x, y):
    print(f"freq={px} -> S[1,1]={py}")
