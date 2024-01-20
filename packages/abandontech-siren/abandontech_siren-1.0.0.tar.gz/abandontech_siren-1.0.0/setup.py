# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['siren', 'siren.tests']

package_data = \
{'': ['*'], 'siren.tests': ['.pytest_cache/*']}

install_requires = \
['pydantic>=2.5.3,<3.0.0']

setup_kwargs = {
    'name': 'abandontech-siren',
    'version': '1.0.0',
    'description': "Async Python bindings for Minecraft's RCON protocol",
    'long_description': '# McRcon\nPython package for authenticating and communicating with a Minecraft server using the Minecraft RCON protocol\n\n# Sample Usage\n\n```python\nimport asyncio\n\nfrom siren import RconClient\n\n\nasync def test_auth() -> None:\n    async with RconClient("123.2.3.4", 25575, "AVeryRealPassword") as client:\n        print(await client.send("list"))\n\n\nif __name__ == \'__main__\':\n    loop = asyncio.new_event_loop()\n    loop.run_until_complete(test_auth())\n\n```\n',
    'author': 'fisher60',
    'author_email': 'kyler@abandontech.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/AbandonTech/siren',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
