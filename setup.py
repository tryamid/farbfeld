import setuptools
import subprocess

setuptools.setup(
    name= 'py-farbfeld',
    version= subprocess.check_output(['git', 'describe', '--tags']).strip() \
            .decode('utf-8') \
            .split('-g')[0],
    description= "Implementation of the Suckelss Farbfeld image format in pure Python",
    author= "Shantanu Biswas",
    author_email= "bsantanu381@gmail.com",
    packages= [
        'farbfeld'
    ],
    url= "https://github.com/tryamid/farbfeld",
    license= 'WTFPL',
    python_requires= ">=3.5"
)