# Monty Hall Simulation

This project simulates the famous Monty Hall problem, allowing you to experiment with the two main strategies: keeping your initial choice or switching after the host reveals a goat. The app is built with Streamlit for an interactive web experience.

## Features

- Run multiple simulations of the Monty Hall game
- Compare success rates when keeping or switching doors
- Visualize results and averages in real time
- Simple, interactive interface

## Requirements

- Python 3.8+
- [Poetry](https://python-poetry.org/)
- [Streamlit](https://streamlit.io/)

## Installation

Clone the repository and install dependencies using Poetry:

```bash
git clone https://github.com/yourusername/monty-hall.git
cd monty-hall
poetry install
```

## Usage

Start the Streamlit app with Poetry:

```bash
poetry run streamlit run app.py
```

Then open the provided local URL in your browser.

## Project Structure

- `app.py` — Main Streamlit application
- `monty_hall.py` — Core simulation logic
- `pyproject.toml` — Poetry configuration and dependencies

## License

MIT License

---

Feel free to contribute or open issues!