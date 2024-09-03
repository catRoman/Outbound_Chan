# Outbound Chan -- Diamond Delivery Automation Bot

## Overview

The **Outbound Chan Diamond Delivery Automation Bot** is a tool designed to streamline the process of booking trailers, manifesting, and linehauls for diamond deliveries. This bot integrates with Excel for scheduling trailer bookings and automates interactions with MSB for managing manifests and linehauls using GUI automation.

## Features

- **Trailer Booking**: Automates the process of booking trailers on Seaspan based on data from an Excel worksheet.
- **Manifesting**: Generates and manages manifests automatically.
- **Linehaul Automation**: Handles linehauls efficiently by integrating with MSB.
- **GUI Automation**: Utilizes GUI automation to interact with MSB and FileMaker Pro.

## Installation

### Prerequisites

- Python 3.8 or higher
- Required Python packages (`pandas`, `openpyxl`, `pyautogui`, etc.)
- Microsoft Excel
- MSB and FileMaker Pro installed on your system

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/diamond-delivery-automation-bot.git
   cd diamond-delivery-automation-bot

   ```

2. **Install Dependencies**

   It’s recommended to use a virtual environment. First, install pip if you haven’t already:

   ```bash
   python -m pip install --upgrade pip
   Then, install the required packages:

   ```

   ```bash
   pip install -r requirements.txt

   ```

3. **Configuration**

Create a configuration file config.json in the root directory with the following structure:

    ```json

    {
        "excel_file_path": "path/to/your/excel_file.xlsx",
        "msb_config": {
        "some_setting": "value"
        },
        "filemaker_config": {
        "some_setting": "value"
        }
    }

    ````

Ensure that you have the appropriate access and permissions for MSB and FileMaker Pro.

## Usage

1. Prepare the Excel Worksheet

2. Ensure that your Excel worksheet is properly formatted according to the template provided. The bot expects specific columns for trailer booking.

3. Run the Bot

4. Execute the script to start the automation process:

   ```bash
       python main.py
   ```

The bot will read data from the Excel file, book trailers, and automate manifesting and linehauls.

## Contributing

We welcome contributions to the Diamond Delivery Automation Bot! Please follow these steps to contribute:

1. Fork the Repository: Create a personal fork of the repository on GitHub.
2. Clone Your Fork: Clone your fork to your local machine.
3. Create a Branch: Create a new branch for your changes.
4. Make Changes: Implement your changes or fixes.
5. Submit a Pull Request: Push your changes and submit a pull request to the main repository.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For any questions or issues, please contact catlinroman84@gmail.com or croman@rdiamonddelivery.com.
