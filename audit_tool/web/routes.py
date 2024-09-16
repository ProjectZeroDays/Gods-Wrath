from audit_tool.web import app
from flask import render_template, redirect, url_for, flash, request, session
from audit_tool.database.setup_database import authenticate
from audit_tool.sn1per.scanner import run_sn1per_scan
import pyotp
import json
import os
import requests

# Load configuration
CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "audit_tool")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")
with open(CONFIG_PATH, "r") as config_file:
    config = json.load(config_file)

@app.route('/')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        otp = request.form['otp']
        if authenticate(username, password):
            totp = pyotp.TOTP(config["2fa_secret"])
            if totp.verify(otp):
                session['username'] = username
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid OTP', 'danger')
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        target = request.form['target']
        scan_result = run_sn1per_scan(target)
        flash(f'Scan result: {scan_result}', 'info')
    return render_template('schedule.html')

@app.route('/reports', methods=['GET', 'POST'])
def reports():
    if 'username' not in session:
        return redirect(url_for('login'))
    # Logic to fetch and display reports
    reports = [
        {"date": "2024-09-15", "type": "Vulnerability Scan", "status": "Completed"},
        {"date": "2024-09-14", "type": "Penetration Test", "status": "In Progress"}
    ]
    if request.method == 'POST':
        filter_date = request.form.get('filter_date')
        filter_type = request.form.get('filter_type')
        filter_status = request.form.get('filter_status')
        # Apply filters to reports
        if filter_date:
            reports = [r for r in reports if r['date'] == filter_date]
        if filter_type:
            reports = [r for r in reports if r['type'] == filter_type]
        if filter_status:
            reports = [r for r in reports if r['status'] == filter_status]
    return render_template('reports.html', reports=reports)

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    # Logic to integrate with Rocket.Chat
    rocket_chat_url = "https://chat.example.com"
    return render_template('chat.html', rocket_chat_url=rocket_chat_url)
