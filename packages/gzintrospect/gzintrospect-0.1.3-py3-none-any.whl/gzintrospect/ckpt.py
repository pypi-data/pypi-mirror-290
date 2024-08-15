import tensorflow as tf
import numpy as np
import warnings

warnings.filterwarnings('ignore')


class Ckpt:
    def __init__(self, path):
        self.ckpt_reader = tf.train.load_checkpoint(path)
        self.var_map = {name: shape for name, shape in tf.train.list_variables(path)}  # {var_name: var_shape}

    def get(self, name):
        return self.ckpt_reader.get_tensor(name)

    def list_var(self, adam=False):
        if adam:
            print(self.var_map)
        else:
            print({k: v for k, v in self.var_map.items() if ('Adam' not in k)})

    def summary(self):
        for name in self.var_map.keys():
            info = self.summary_single(name)
            print(info)

    def summary_single(self, name):
        tensor = self.get(name)
        info = f'[{name}] shape = {tensor.shape}, parameters = {np.prod(tensor.shape)}, '
        if np.prod(tensor.shape <= 10):
            info += f'value = {tensor}'
        else:
            info += (
                f'min={np.min(tensor)}, '
                f'25%%={np.quantile(tensor, 0.25)}, '
                f'50%%={np.quantile(tensor, 0.50)}, '
                f'75%%={np.quantile(tensor, 0.75)}, '
                f'max={np.max(tensor)}'
            )
        return info

    def get_param_num(self):
        num = sum([np.prod(shape) for shape in self.var_map.values()])
        if num < 1024:
            print(f"param_num = %i" % num)
        elif num < 1024 ** 2:
            print(f"param_num = %.2fK" % (num / 1024))
        elif num < 1024 ** 3:
            print(f"param_num = %.2fM" % (num / 1024 / 1024))
        return num



