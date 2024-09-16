#!/bin/bash

# Function to detect the local path of a given repository
detect_repo_path() {
    local repo_name=$1
    local repo_path=$(find ~ -type d -name "$repo_name" 2>/dev/null | head -n 1)
    echo $repo_path
}

# Detect paths
VENGENCE_PATH=$(detect_repo_path "vengence")
SN1PER_PATH=$(detect_repo_path "Sn1per")

# Check if paths are detected
if [ -z "$VENGENCE_PATH" ] || [ -z "$SN1PER_PATH" ]; then
    echo "Error: Could not detect Vengence or Sn1per repository paths."
    exit 1
fi

WEB_PANEL_PATH="$VENGENCE_PATH/web_panel"

# Clone Sn1per repository if not already present
if [ ! -d "$SN1PER_PATH" ]; then
    git clone https://github.com/1N3/Sn1per.git $SN1PER_PATH
    cd $SN1PER_PATH
    bash install.sh
fi

# Create Sn1per integration module
cat <<EOL > $VENGENCE_PATH/modules/sn1per_integration.py
import subprocess

class Sn1perIntegration:
    def __init__(self, target):
        self.target = target

    def run_sn1per_scan(self, mode='normal'):
        command = f'sniper -t {self.target} -m {mode}'
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return stdout, stderr

    def parse_results(self, results):
        # Implement parsing logic for Sn1per results
        parsed_results = {}
        return parsed_results

    def integrate_with_vengence(self, parsed_results):
        # Implement integration logic with Vengence
        pass

# Example usage
# sn1per = Sn1perIntegration(target='example.com')
# stdout, stderr = sn1per.run_sn1per_scan()
# parsed_results = sn1per.parse_results(stdout)
# sn1per.integrate_with_vengence(parsed_results)
EOL

# Add Sn1per scan functions to the web panel
cat <<EOL > $WEB_PANEL_PATH/sn1per_scans.html
<!DOCTYPE html>
<html>
<head>
    <title>Sn1per Scans</title>
</head>
<body>
    <h1>Sn1per Scans</h1>
    <form action="/run_sn1per_scan" method="post">
        <label for="target">Target:</label>
        <input type="text" id="target" name="target"><br><br>
        <label for="mode">Mode:</label>
        <select id="mode" name="mode">
            <option value="normal">Normal</option>
            <option value="osint">OSINT</option>
            <option value="recon">Recon</option>
            <option value="stealth">Stealth</option>
        </select><br><br>
        <input type="submit" value="Run Scan">
    </form>
</body>
</html>
EOL

# Update web panel routes to handle Sn1per scans
cat <<EOL >> $WEB_PANEL_PATH/routes.py
from flask import request, render_template
from modules.sn1per_integration import Sn1perIntegration

@app.route('/sn1per_scans')
def sn1per_scans():
    return render_template('sn1per_scans.html')

@app.route('/run_sn1per_scan', methods=['POST'])
def run_sn1per_scan():
    target = request.form['target']
    mode = request.form['mode']
    sn1per = Sn1perIntegration(target=target)
    stdout, stderr = sn1per.run_sn1per_scan(mode=mode)
    parsed_results = sn1per.parse_results(stdout)
    sn1per.integrate_with_vengence(parsed_results)
    return f"Scan completed. Results: {parsed_results}"
EOL

# Commit and push changes to the repository
cd $VENGENCE_PATH
git add .
git commit -m "Integrated Sn1per with Vengence framework"
git push origin main

echo "Sn1per integration completed successfully."
