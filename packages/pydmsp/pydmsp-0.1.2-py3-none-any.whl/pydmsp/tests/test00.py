from pydmsp import unzip
from pydmsp import make_xr_dataset
from pydmsp import make_transform_dataset


filepath = 'C:\\Users\\HOME\\PycharmProjects\\dmspreader_repo\\pydmsp\\tests\\j4f0787122.gz'
unzip(filepath)

xr_dataset = make_xr_dataset(filepath)
print(xr_dataset)
print('\n')

xr_transform = make_transform_dataset(filepath)
print(xr_transform)
