# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vision_mamba']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'swarms', 'torch', 'zetascale']

setup_kwargs = {
    'name': 'vision-mamba',
    'version': '0.0.1',
    'description': 'Vision Mamba - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Vision Mamba\nImplementation of Vision Mamba from the paper: "Vision Mamba: Efficient Visual Representation Learning with Bidirectional State Space Model" It\'s 2.8x faster than DeiT and saves 86.8% GPU memory when performing batch inference to extract features on high-res images\n\n\n\n## Installation\n\nYou can install the package using pip\n\n```bash\npip install -e .\n```\n\n# Usage\n```python\n\n```\n\n\n\n### Code Quality 🧹\n\n- `make style` to format the code\n- `make check_code_quality` to check code quality (PEP8 basically)\n- `black .`\n- `ruff . --fix`\n\n### Tests 🧪\n\n[`pytests`](https://docs.pytest.org/en/7.1.x/) is used to run our tests.\n\n# License\nMIT\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/VisionMamba',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
