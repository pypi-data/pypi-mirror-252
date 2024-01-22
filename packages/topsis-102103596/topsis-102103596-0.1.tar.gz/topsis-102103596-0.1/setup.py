from distutils.core import setup

setup(
    name="topsis-102103596",  # How you named your package folder (MyLib)
    packages=["topsis"],  # Chose the same as "name"
    version="0.1",  # Start with a small number and increase it with every change you make
    license="MIT",  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description="Calculates the topsis score",  # Give a short description about your library
    author="Hitesh Aggarwal",  # Type in your name
    author_email="haggarwal_be21@thapar.edu",  # Type in your E-Mail
    url="https://github.com/Hitesh-Aggarwal/topsis-102103596",  # Provide either the link to your github or to your website
    download_url="https://github.com/Hitesh-Aggarwal/topsis-102103596/archive/refs/tags/v_01.tar.gz",  # I explain this later on
    keywords=[
        "topsis",
        "Decision",
        "Multi",
        "Criteria",
    ],  # Keywords that define your package best
    install_requires=["pandas", "numpy", "scipy"],  # I get to this in a second
    classifiers=[
        "Development Status :: 3 - Alpha",  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        "Intended Audience :: Developers",  # Define that your audience are developers
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",  # Again, pick a license
        "Programming Language :: Python :: 3.11",  # Specify which pyhton versions that you want to support
        "Programming Language :: Python :: 3.10",  # Specify which pyhton versions that you want to support
        "Programming Language :: Python :: 3.9",  # Specify which pyhton versions that you want to support
        "Programming Language :: Python :: 3.8",  # Specify which pyhton versions that you want to support
        "Programming Language :: Python :: 3.7",  # Specify which pyhton versions that you want to support
        "Programming Language :: Python :: 3.6",  # Specify which pyhton versions that you want to support
        "Programming Language :: Python :: 3.5",  # Specify which pyhton versions that you want to support
    ],
)
