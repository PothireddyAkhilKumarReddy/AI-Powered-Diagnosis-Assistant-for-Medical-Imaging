import tensorflow as tf
import os

print(f"TensorFlow Version: {tf.__version__}")
print("CUDA Available: ", tf.test.is_built_with_cuda())
print("GPU Available: ", tf.test.is_gpu_available())
print("Physical Devices:")
for device in tf.config.list_physical_devices():
    print(f"  - {device}")

try:
    from tensorflow.python.client import device_lib
    print("\nDevice Lib List:")
    print(device_lib.list_local_devices())
except Exception as e:
    print(f"Error checking device_lib: {e}")
