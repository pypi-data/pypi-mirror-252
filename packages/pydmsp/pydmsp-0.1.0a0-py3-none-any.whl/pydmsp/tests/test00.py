from pydmsp import unzip, get_filename
from pydmsp import make_xr_dataset
from pydmsp import make_transform_dataset


filepath = "C:\\Users\\HOME\\PycharmProjects\\dmspreader_repo\\tests\\j4f0787122.gz"
unzip(filepath)
filename = get_filename(filepath)

xr_dataset = make_xr_dataset(filename.replace('.gz', ''))
print(xr_dataset)
print('\n')

xr_transform = make_transform_dataset(filename.replace('.gz', ''))
print(xr_transform)
