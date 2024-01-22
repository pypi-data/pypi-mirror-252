from pydmsp import unzip
from pydmsp import make_xr_dataset
from pydmsp import make_transform_dataset


def print_raw_and_shape(filepath, mode='to_ram'):
    res = unzip(filepath, mode=mode)
    print(res)
    print(res.shape)
    return (res.shape[0], res)


filepath1 = 'j4f0787122.gz'
filepath2 = 'j4f0787124.gz'
filepath3 = 'j4f0787138.gz'

shape1, res1 = print_raw_and_shape(filepath1)
records_count1, _reminder1 = divmod(shape1, 2640)
print(records_count1, _reminder1)
res1 = res1.reshape(records_count1, 2640)
print(res1)
res1 = res1[:, 1]
print(*res1, res1.shape)
# print(res1.shape[1]/60, res1.shape[1]%60)
# res1 = res1[:, 15:2595].reshape(shape1, 43, 60)
# print(shape1, shape1/2640, shape1%2640, res1/60, res1%60)
#
# shape2, res2 = print_raw_and_shape(filepath2)
# res2 = res2[:, 15:2595].reshape(shape2, 43, 60)
# print(shape2, shape2/2640, shape2%2640)
#
# shape3, res3 = print_raw_and_shape(filepath3)
# res3 = res3[:, 15:2595].reshape(shape3, 43, 60)
# print(shape3, shape3/2640, shape3%2640)


# res1 = unzip(filepath1, mode='to_ram')
# print(res1)
# print(res1.shape)
# print()

# res2 = unzip(filepath2, mode='to_ram')
# print(res2)
# print(res2.shape)

# xr_dataset = make_xr_dataset(filepath)
# print(xr_dataset)
# print('\n')
#
# xr_transform = make_transform_dataset(filepath)
# print(xr_transform)
