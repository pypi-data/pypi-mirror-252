import setuptools
    
setuptools.setup(
    name="oimbot",
    version="10.5.7",
    author="Aeroz",
    long_description="For Create Fortnite LobbyBot",
    description="Lobby_Bot_Ftn",
    url="https://bot.aerozoff.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'crayons',
        'BenBotAsync',
        'FortniteAPIAsync',
        'sanic==21.6.2',
        'colorama',
        'aiohttp',
    ],
    include_package_data=True
)
