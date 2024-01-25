# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fuyu']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'torch', 'transformers', 'zetascale']

setup_kwargs = {
    'name': 'fuyu',
    'version': '0.0.7',
    'description': 'fuyu - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Fuyu\n![FUYU](/architecture.png)\n\nA implementation of Fuyu, the multimodal AI model from Adept in pytorch and zeta. The architecture is basically instead of using an encoder like VIT or CLIP they just patch the image then project it then feed it into the transformer decoder. The architecture is image patch embeddings -> linear projection -> decoder llm. \n\n**UPDATE**\n- [Fuyu-Heavy:](https://www.adept.ai/blog/adept-fuyu-heavy) proposes that scaling up the model architecture works but with some caveats. They need more stabilization during training. I have refactored the base Fuyu model implementation to include RMSNorm, LayerNorm, Swish, and a vast array of other techniques to radically increase multi-modal training such as normalizing the image during the shape rearrange and after.\n\n- DPO Confirmed [HERE](https://twitter.com/code_monet/status/1750218951832035580)\n\n\n\n[Blog paper code](https://www.adept.ai/blog/fuyu-8b)\n\n# Appreciation\n* Lucidrains\n* Agorians\n* Adept\n\n# Install\n`pip install fuyu`\n\n## Usage\n```python\nimport torch\nfrom fuyu import Fuyu\n\n# Initialize model\nmodel = Fuyu(\n    num_tokens=20342,\n    max_seq_len=4092,\n    dim=640,\n    depth=8,\n    dim_head=128,\n    heads=6,\n    use_abs_pos_emb=False,\n    alibi_pos_bias=True,\n    alibi_num_heads=3,\n    rotary_xpos=True,\n    attn_flash=True,\n    attn_kv_heads=2,\n    qk_norm=False,\n    attn_qk_norm=False,\n    attn_qk_norm_dim_scale=False,\n    patches=16,\n)\n\n# Text shape: [batch, seq_len, dim]\ntext = torch.randint(0, 20342, (1, 4092))\n\n# Img shape: [batch, channels, height, width]\nimg = torch.randn(1, 3, 256, 256)\n\n# Apply model to text and img\ny = model(text, img)\n\n# Output shape: [batch, seq_len, dim]\nprint(y)\n\n\n```\n\n# License\nMIT\n\n# Citations\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/fuyu',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
