# Intrinsically stable MPC

## Download

```
git clone --recursive https://github.com/neverorfrog/is-mpc-nao.git
```

## Install dependencies

- Install conda env, activate it and install requirements with 
```
pip install -r requirements.txt
```

- Install apt packages: 
```
sudo apt install cmake libeigen3-dev python3-dev --install-recommends
```

## Build the code

To use also the python bindings, you need to call the setup.py script. This in turn launches the conanfile.py script. Whenever you have new dependencies in the conanfile or you want to build for a new configuration, run
```
conan install conanfile.py --build=missing -s build_type=<cfg>
```
To build the code, from the root folder run
```
python3 setup.py build --cfg=<cfg>
```
To install the python binding package, check that the conda env is activated and from the root folder run
```
python3 setup.py install --cfg=<cfg>
```
`<cfg>` can be Release or Debug
