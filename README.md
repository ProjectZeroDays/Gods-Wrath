# God's Wrath Audit Tool

## Overview

This tool provides a comprehensive framework for automated offensive and defensive cybersecurity testing and auditing. It integrates open-source and low-cost resources to ensure scalability, cost-effectiveness, and high-quality metrics and reporting.

## Features

- **User Authentication**: Secure login with encrypted credentials.
- **Audit Scheduling**: Schedule audits with a user-friendly interface.
- **Notifications**: Email and SMS notifications for audit results and updates.
- **Payment Processing**: Handle payments securely through integrated payment gateways.
- **AI Piloting**: Automated scanning and testing with AI-driven insights.
- **Report Generation**: Generate comprehensive audit reports in various formats.
- **Collaboration Tools**: Integrated messaging platform for team communication.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ProjectZeroDays/Vengence.git
   cd Vengence
   ```

2. **Run the Install Script**:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

3. **Set Up the Database**:
   ```bash
   python3 audit_tool/database/setup_database.py
   ```

## Usage

1. **Run the Main Script**:
   ```bash
   python3 audit_tool/main.py
   ```

2. **Login**:
   - Use the GUI to log in with your credentials.

## Configuration

- **Email and SMS Notifications**:
  - Update the `config.json` file in the `audit_tool/config` directory with your email and SMS API credentials.

## Contributing

We welcome contributions! Please fork the repository and submit pull requests.

## License

This project is licensed under the MIT License.
