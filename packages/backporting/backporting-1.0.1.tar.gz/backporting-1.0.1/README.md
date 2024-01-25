
### Install the package:

    pip3 install backporting
    
#### After the command `backporting` should be available from CLI. 




## Additional commands to create venv if it's needed 

### Create www directory where project sites and environment dir

    mkdir /var/envs && mkdir /var/envs/bin

### Install virtualenvwrapper

    sudo pip3 install virtualenvwrapper
    sudo pip3 install --upgrade virtualenv

### Add these to your bashrc virutualenvwrapper work

    export WORKON_HOME=/var/envs
    export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
    export PROJECT_HOME=/var/www
    export VIRTUALENVWRAPPER_HOOK_DIR=/var/envs/bin
    source /usr/local/bin/virtualenvwrapper.sh

### Create virtualenv
    mkvirtualenv --python=python3 test_env
