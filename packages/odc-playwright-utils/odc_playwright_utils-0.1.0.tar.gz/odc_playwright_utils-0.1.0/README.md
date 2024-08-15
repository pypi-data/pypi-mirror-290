# My ODC Playwright Utils

This package provides a set of utility functions for UI automation based on Playwright. It encapsulates common methods such as element interaction, waiting for conditions, and page navigation to simplify automated testing tasks.

## Features

- Wait for elements to be visible or clickable
- Interact with input fields, dropdowns, and other web elements
- Manage page navigation and URLs
- Take screenshots, upload files, and more

## Installation

```bash
pip install odc_playwright_utils
```

## Dependencies

- `playwright==1.45.1`

## Usage

Here's an example of how to use the package:
```python
from module.playwright_utils import PlaywrightUtils
from module.WebDriverManager import WebDriverManager

# Initialize the browser and page
page = WebDriverManager.get_page()

# Use PlaywrightUtils to interact with elements
utils = PlaywrightUtils(page)
utils.click("#submit-button")