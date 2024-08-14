import tensorflow as tf
import numpy as np
import os
import warnings

warnings.filterwarnings('ignore')


class Ckpt:
    def __init__(self, path) -> None:
        self.ckpt_reader = tf.train.load_checkpoint(path)
        self.vars = [v for v in tf.train.list_variables(path)]
        self.var_map = {name: shape for name, shape in self.vars}  # {var_name: var_shape}

    def filter(self, include=None, exclude=None, field=0):
        assert field in (0, 1)
        vars = self.vars
        if exclude:
            vars = [v for v in vars if exclude not in v[field]]
        if include:
            vars = [v for v in vars if include in v[field] or include == v[field]]
        return vars

    def get(self, name):
        return self.ckpt_reader.get_tensor(name)

    def list_var(self):
        print(self.var_map)

    def get_param_num(self):
        return sum([np.prod(shape) for shape in self.var_map.values()]) / 2 ** 20

    def hack(self, exist):
        for name, _ in self.filter():
            if name in exist:
                continue
            var = tf.compat.v1.Variable(self.show(name), name=name)

    def dump(self, path, name):
        assert len(self.filter()) == len(tf.compat.v1.global_variables())
        saver = tf.compat.v1.train.Saver()
        sess = tf.compat.v1.Session()
        sess.run(tf.compat.v1.global_variables_initializer())
        os.makedirs(path)
        saver.save(sess, os.path.join(path, name))

    def get_diff(self, base_ckpt):
        res_dict = {}  # name: tensor
        hack_dict = {}  # name: (array, base_array)

        for name, shape in self.vars:
            base_shape = base_ckpt.var_map.get(name)
            if base_shape is None:
                print(name, '[init]')
                if 'Adam' in name:
                    res_dict[name] = tf.Variable(np.zeros_like(self.get(name)), name=name)
                else:
                    res_dict[name] = tf.compat.v1.get_variable(name=name, shape=shape)
            elif shape == base_shape:
                res_dict[name] = tf.Variable(base_ckpt.get(name), name=name)
            else:
                print(name, '[hack]')
                hack_dict[name] = (self.get(name), base_ckpt.get(name))
        return res_dict, hack_dict

    def show_diff(self, base_ckpt, var_type=['new', 'diff'], filter_adam=False):
        base_num = base_ckpt.get_param_num()
        target_num = self.get_param_num()
        print(
            f'target_num = {target_num:.2f}M, base num = {base_num:.2f}M, num diff = {target_num - base_num:.2f}M ({(target_num / base_num - 1) * 100:.2f}%)')

        if type(var_type) is not list:
            var_type = [var_type]

        if 'new' in var_type:
            print("\n============= New Variables ==============\n")
            for name, shape in self.vars:
                if name not in base_ckpt.var_map:
                    if not ('Adam' in name and filter_adam):
                        print('%s: %s' % (name, shape))

        if 'diff' in var_type:
            print("\n============== Different Shape Variables =============\n")
            for name, shape in self.vars:
                if name in base_ckpt.var_map:
                    base_shape = base_ckpt.var_map[name]
                    if base_shape != shape:
                        if not ('Adam' in name and filter_adam):
                            shape_diff = np.array(shape) - np.array(base_shape)
                            print('[%s]: base_shape = %s, target_shape = %s, shape_diff = %s'
                                  % (name, shape, base_shape, shape_diff.tolist()))




