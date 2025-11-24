<div align="center">
  <img src="https://raw.githubusercontent.com/lucasrodes/whatstk/develop/assets/logo.svg" width="30%" alt="whatstk logo">

  # whatstk

  **Parse, analyze, and visualize WhatsApp chats with Python**

  [![PyPI](https://img.shields.io/badge/pypi-v0.8.1-25D366?logo=whatsapp)](https://pypi.org/project/whatstk/)
  [![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg?logo=python&logoColor=yellow)](https://www.python.org/downloads/)
  [![Build](https://img.shields.io/github/actions/workflow/status/lucasrodes/whatstk/ci-full.yml?branch=main)](https://github.com/lucasrodes/whatstk/actions)
  [![codecov](https://codecov.io/gh/lucasrodes/whatstk/branch/master/graph/badge.svg)](https://codecov.io/gh/lucasrodes/whatstk)
  [![Documentation](https://readthedocs.org/projects/whatstk/badge/?version=latest)](https://whatstk.readthedocs.io/en/latest/)
  [![License](https://img.shields.io/github/license/lucasrodes/whatstk)](https://github.com/lucasrodes/whatstk/blob/master/LICENSE)
  [![Downloads](https://pepy.tech/badge/whatstk)](https://pepy.tech/project/whatstk)

  [Documentation](https://whatstk.readthedocs.io/en/latest/) • [Try Live Demo](https://whatstk.streamlit.app/) • [Tutorial](https://medium.com/data-science/analyzing-whatsapp-chats-with-python-20d62ce7fe2d)

</div>

<!-- --- -->

## Features

- 📱 **Parse WhatsApp exports** from Android and iOS (including zip files)
- 🐼 **Convert to pandas DataFrames** for easy analysis
- 📊 **Interactive visualizations** powered by Plotly
- 🔧 **Command-line tools** for quick CSV conversions
- 🌍 **Multi-language support** for various WhatsApp date formats
- 🚀 **Fast and efficient** processing of large chat histories


## Installation

```bash
pip install whatstk
```

**Requirements:** Python 3.11+

<details>
<summary>Install development version</summary>

```bash
pip install git+https://github.com/lucasrodes/whatstk.git@develop
```

</details>

## Quick Start

### Export your WhatsApp chat

Follow the [export instructions](https://whatstk.readthedocs.io/en/stable/source/getting_started/export_chat.html) for your device.

### Load and analyze

```python
from whatstk import df_from_whatsapp

# Load chat into a DataFrame
df = df_from_whatsapp("path/to/chat.txt")

# Or directly from iOS zip export
df = df_from_whatsapp("path/to/chat.zip")

# Now use pandas to analyze
print(df.head())
```

### Convert to CSV

```bash
whatstk-to-csv input_chat.txt output.csv
```

### Visualize

```python
from whatstk.graph import plot_user_message_count

# Interactive message count chart
fig = plot_user_message_count(df)
fig.show()
```

## Documentation

Full documentation available at [whatstk.readthedocs.io](https://whatstk.readthedocs.io/en/stable/)

- [Getting Started Guide](https://whatstk.readthedocs.io/en/stable/source/getting_started/index.html)
- [Code Examples](https://whatstk.readthedocs.io/en/stable/source/code_examples/index.html)
- [API Reference](https://whatstk.readthedocs.io/en/stable/source/code/index.html)

## Contributing

We welcome contributions! See our [contribution guide](https://whatstk.readthedocs.io/en/stable/source/contribute.html) to get started.

## License

This project is licensed under the [GPL-3.0 License](LICENSE).

## Citation

If you use whatstk in your research or project, please cite:

```bibtex
@software{whatstk,
  author = {Rodés-Guirao, Lucas},
  title = {whatstk: WhatsApp analysis and parsing toolkit},
  url = {https://github.com/lucasrodes/whatstk},
  year = {2025}
}
```

or as 

> Lucas Rodés-Guirao. "whatstk, WhatsApp analysis and parsing toolkit", https://github.com/lucasrodes/whatstk

## Featured Projects

- [Your WhatsApp Chat History in Cool Graphs](https://deepnote.com/@batmanscode/Your-Whatsapp-Chat-History-in-Cool-Graphs-mQoSsYjUSw29D4nZDs_KwA) by [@batmanscode](https://github.com/batmanscode)
- [WhatsAppening to the news](https://whatsappening.joltetn.eu/) by [@enric1994](https://github.com/enric1994)
- [Summary Analysis of My WhatsApp Chats](https://nmdanial.medium.com/summary-analysis-of-nik-and-afyas-whatsapp-chats-eb3928b18421) by [N.M. Danial](https://nmdanial.medium.com/)
- [From Chat to Insights: Analyzing WhatsApp Group Conversations](https://medium.com/@barklight/cracking-the-conversation-973839be5b88) by [Erland Sada](https://medium.com/@barklight)
- [Building a Chatbot: Fine-Tune LLMs with WhatsApp Data](https://www.linkedin.com/pulse/building-chatbot-fine-tune-llms-whatsapp-data-daniel-pleus/) by [Daniel Pleus](https://www.linkedin.com/in/daniel-pleus/)

> [!NOTE]
> If you have created a project using whatstk, I'd love to know that and add it this list! Thanks a lot!

---

<div align="center">

  ⭐ **Star this repo if you find it useful!**

  Made with ❤️ by [Lucas Rodés-Guirao](https://github.com/lucasrodes)

</div>
