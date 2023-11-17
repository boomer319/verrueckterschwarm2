from setuptools import find_packages, setup

package_name = 'crazyflie_flight_path'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='aurelio',
    maintainer_email='aureliostrazzeri@gmail.com',
    description='Accumulation of scripts to test out different methods of coordinating the crazyflies movement',
    license='TODO: License declaration',
    tests_require=['pytest'],
)
