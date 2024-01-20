from setuptools import setup, find_packages

setup(
    name = 'cerebralWave',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'datetime>=5.4',
        'wikipedia>=1.4.0',
        'PyPDF2>=1.28.2',
        'urllib3>=1.26.9',
        'requests>=2.31.0',
        'webbrowser'

    ],
    author="Dhairya Raj Maloo",
    author_email="drm281208@gmail.com",
    description="This is a library which can help with common chatbot functions.",
    url='https://github.com/dhairyaraj281208/Cerebral_wave',
)