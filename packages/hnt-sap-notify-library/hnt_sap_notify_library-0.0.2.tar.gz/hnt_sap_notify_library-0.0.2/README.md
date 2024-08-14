# Setup the development env win10
```sh
python -m venv venv
. .\venv\Scripts\activate
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python.exe -m pip install --upgrade pip
pip install pytest
pip install python-dotenv
pip install robotframework-sapguilibrary
copy .\.env.template .\.env
```