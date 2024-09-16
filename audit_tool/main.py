#!/usr/bin/env python3

from audit_tool.database.setup_database import setup_database, add_admin_user
from audit_tool.gui.login_gui import login_gui
from audit_tool.sn1per.scanner import run_sn1per_scan
from audit_tool.web import app

if __name__ == "__main__":
    setup_database()
    add_admin_user()
    login_gui()
    # Example usage of the Sn1per scanner
    target = "example_target"
    scan_result = run_sn1per_scan(target)
    print(scan_result)
    # Run the web server
    app.run(debug=True)
