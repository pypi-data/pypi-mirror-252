from torch.cuda import CudaError

from echo_logger import *


@monit_feishu()
def foo(a, b):
    raise CudaError('CUDA error: no kernel image is available for execution on the device')


if __name__ == '__main__':
    foo(1, 2)
