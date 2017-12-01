## Installation instructions
### 0. Prerequisite
* Ubuntu Linux 32 Bit (64 Bit not tested)
* Dymola 2017 (DYMOLA_2017_AllLinux.zip)
* Python 3.4.3
* Java 8

###### Utility:
	sudo apt-get install open-vm-tools 
	sudo apt-get install open-vm-tools-desktop 
	sudo apt-get install git vim htop
	sudo apt-get install alien
	//32 Bit Complications 
	 sudo apt-get install g++-multilib libc6-dev-i386


### 1. Install Python and Python modules
###### Install Python (global):
	sudo apt-get update	
	sudo apt-get install python3-pip python3-dev python-virtualenv
	//scipy dependency 
	sudo apt-get install libatlas-base-dev gfortran libffi-dev
	//matpotlib dependency
	sudo apt-get install libfreetype6-dev
	//pyfmi dependency
	sudo apt-get install cmake
	
* Source: 
	* [install scipy](https://www.scipy.org/install.html)
	* [install blas](http://stackoverflow.com/questions/26575587/cant-install-scipy-through-pip)

###### Install moduls:
	sudo pip3 install --upgrade numpy
	sudo pip3 install --upgrade scipy
	sudo pip3 install --upgrade nose
	sudo pip3 install --upgrade pandas
	sudo pip3 install --upgrade matplotlib
	sudo pip3 install --upgrade sympy	
	sudo pip3 install --upgrade jupyter
	sudo pip3 install --upgrade pytest
	sudo pip3 install --upgrade Cython

### 2. Install PyFMI
######  Create working dir:
	mkdir pyfmi

###### Install FMI Library:
	cd ~/pyfmi
	sudo wget http://www.jmodelica.org/downloads/FMIL/FMILibrary-2.0.2b3-src.zip
	sudo unzip FMILibrary-2.0.2b3-src.zip
	cd FMILibrary-2.0.2b3/
	sudo mkdir build-fmilib && cd build-fmilib
	sudo cmake -DFMILIB_INSTALL_PREFIX=../install ../
	sudo make install test
###### Install Sundials:
	cd ~/pyfmi
	sudo wget http://computation.llnl.gov/projects/sundials-suite-nonlinear-differential-algebraic-equation-solvers/download/sundials-2.4.0.tar.gz
	tar xzf sundials-2.4.0.tar.gz
	cd sundials-2.4.0
	sudo ./configure CFLAGS="-fPIC"
	make
	sudo make install
###### Install Assimulo:
	cd ~/pyfmi	
	sudo wget https://pypi.python.org/packages/4c/c0/19a54949817204313efff9f83f1e4a247edebed0a1cc5a317a95d3f374ae/Assimulo-2.9.zip#md5=3f28fd98011d2ec7a01703a1ef1dff45
 	sudo unzip Assimulo-2.9.zip
	cd Assimulo-2.9
	sudo python3 setup.py install --sundials-home=~/pyfmi/sundials-2.4.0 --blas-home=/usr/lib/libblas --lapack-home=/usr/lib/libblas

###### Install PyFMI:
	cd ~/pyfmi
	sudo wget https://pypi.python.org/packages/66/60/26664b2b2cad4a7fae409214e2f8901177322d78bfb11ef61e580115c9b8/PyFMI-2.3.1.zip#md5=577829ee1ee83fbb8c28ddf4b82aa4ee
	sudo unzip PyFMI-2.3.1.zip
	sud	
	sudo python3 setup.py install --fmil-home=/home/yourusername/pyfmi/FMILibrary-2.0b3/install/
	


######  Source: 
* [PyFMI](http://www.jmodelica.org/page/4924)
* [Install pyfmi](http://laht.info/installing-pyfmi-1-5-on-ubuntu-14-04/)
* [Sunidals](http://computation.llnl.gov/projects/sundials-suite-nonlinear-differential-algebraic-equation-solvers/sundials-software)
* [Assimulo](https://pypi.python.org/packages/4c/c0/19a54949817204313efff9f83f1e4a247edebed0a1cc5a317a95d3f374ae/Assimulo-2.9.zip#md5=3f28fd98011d2ec7a01703a1ef1dff45)

### 3. Install OpenAI gym

######  Install OpenAi Gym:

	git clone https://github.com/openai/gym.git
	cd gym
	pip install -e .

######  Install libav-tools:
	sudo apt-get install libav-tools
	git clone https://github.com/openai/gym
	sudo pip3 install -e .
	sudo pip3 install pyglet

######  Source: 
*  <https://gym.openai.com/docs>

### 4. Install java8 jdk
######  Install Java 8: 
	sudo add-apt-repository ppa:webupd8team/java
	sudo apt-get update
	sudo apt-get install oracle-java8-installer
######  Source: 
* [askubuntu](http://askubuntu.com/questions/521145/how-to-install-oracle-java-on-ubuntu-14-04)

### 5. Install Dymola
###### Install Dymola: 
	cd /opt
	sudo unzip DYMOLA_2017_AllLinux.zip -d DYMOLA_2017
	cd DYMOLA_2017/linux_x86_64/
	sudo alien -i -k dymola-2017.1-1.x86_64.rpm

###### Source: 
* [Dymola](http://www.3ds.com/products-services/catia/products/dymola/linux/)

###### Configure Dymola: Add to environment variables to .bashrc:

	export MODELICAPATH=${MODELICAPATH}:/usr/local/Modelica/Library/
	export DYMOLA=/opt/dymola  	
	export LD_LIBRARY_PATH=$DYMOLA/bin/lib:$LD_LIBRARY_PATH

###### Start Dymola:
	/opt/dymola-2017-x86_64/bin/dymola.sh 

--

### Optional: Install pycharm cumminity edition
* Download source [PyCharm](https://www.jetbrains.com/pycharm/download/#section=linux)

		sudo cp pycharm-community-2016.1.2.tar.gz /opt/
		sudo tar -xzvf /opt/pycharm-community-2016.1.2.tar.gz -C /opt
		sudo rm /opt/pycharm-community-2016.1.2.tar.gz 
		./pycharm-community-2016.1.2/bin/pycharm.sh
		
* Run PyCharm:
	
		/opt/pycharm-community-2016.2/bin/pycharm.sh

