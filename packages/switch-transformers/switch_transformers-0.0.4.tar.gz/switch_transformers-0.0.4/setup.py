# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['switch_transformers']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'swarms', 'torch', 'torchvision', 'zetascale']

setup_kwargs = {
    'name': 'switch-transformers',
    'version': '0.0.4',
    'description': 'SwitchTransformers - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Switch Transformers\n\n![Switch Transformer](st.png)\n\nImplementation of Switch Transformers from the paper: "Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity" in PyTorch, Einops, and Zeta. [PAPER LINK](https://arxiv.org/abs/2101.03961)\n\n## Installation\n\n```bash\npip install switch-transformers\n```\n\n# Usage\n```python\nimport torch\nfrom switch_transformers import SwitchTransformer\n\n# Generate a random tensor of shape (1, 10) with values between 0 and 100\nx = torch.randint(0, 100, (1, 10))\n\n# Create an instance of the SwitchTransformer model\n# num_tokens: the number of tokens in the input sequence\n# dim: the dimensionality of the model\n# heads: the number of attention heads\n# dim_head: the dimensionality of each attention head\nmodel = SwitchTransformer(\n    num_tokens=100, dim=512, heads=8, dim_head=64\n)\n\n# Pass the input tensor through the model\nout = model(x)\n\n# Print the shape of the output tensor\nprint(out.shape)\n\n\n```\n\n\n\n## Citation\n```bibtex\n@misc{fedus2022switch,\n    title={Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity}, \n    author={William Fedus and Barret Zoph and Noam Shazeer},\n    year={2022},\n    eprint={2101.03961},\n    archivePrefix={arXiv},\n    primaryClass={cs.LG}\n}\n\n```\n\n# License\nMIT\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/SwitchTransformers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
