# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['moe_mamba']

package_data = \
{'': ['*']}

install_requires = \
['swarms', 'zetascale']

setup_kwargs = {
    'name': 'moe-mamba',
    'version': '0.0.1',
    'description': 'Paper - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# MoE Mamba\nImplementation of MoE Mamba from the paper: "MoE-Mamba: Efficient Selective State Space Models with Mixture of Experts" in Pytorch and Zeta. \n\n[PAPER LINK](https://arxiv.org/abs/2401.04081)\n\n\n## Install\n\n```bash\npip install moe-mamba\n```\n\n# Usage\n```python\nprint("hello world")\n\n```\n\n\n\n## Code Quality 🧹\n\n- `make style` to format the code\n- `make check_code_quality` to check code quality (PEP8 basically)\n- `black .`\n- `ruff . --fix`\n\n\n## Citation\n```bibtex\n@misc{pióro2024moemamba,\n    title={MoE-Mamba: Efficient Selective State Space Models with Mixture of Experts}, \n    author={Maciej Pióro and Kamil Ciebiera and Krystian Król and Jan Ludziejewski and Sebastian Jaszczur},\n    year={2024},\n    eprint={2401.04081},\n    archivePrefix={arXiv},\n    primaryClass={cs.LG}\n}\n\n```\n\n\n# License\nMIT\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/MoE-Mamba',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
