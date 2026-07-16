from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'cv'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
        glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='gooman84',
    maintainer_email='matthewmartin@mines.edu',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
             # format: 'command_name = package.module:function'
            'yolo_node = cv.yoloNode:main',
            'yolo_depth_node = cv.yoloNodeDepth:main'
        ],
    },
)
