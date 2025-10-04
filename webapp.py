from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import tempfile
import os
import sys
import secrets
from absence_extractor import run_full_flow, make_compact_mail

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(32))  # Change this in production
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user = request.form.get('user')
        password = request.form.get('password')
        signer = request.form.get('signer')
        headful = bool(request.form.get('headful'))
        gen_mail = bool(request.form.get('gen_mail'))
        offer_file = bool(request.form.get('offer_file'))
        if not user or not password or not signer:
            flash('All fields are required!', 'danger')
            return redirect(url_for('index'))
        try:
            rows = run_full_flow(user, password, headful=headful)
            absences = [(date_iso, nu) for date_iso, nu in rows if nu > 0]
            if not absences:
                return render_template('result.html', message='There are no absences.')
            mail_body = None
            if gen_mail:
                mail_body = make_compact_mail(rows, signer=signer)
            result_file = None
            if offer_file:
                with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8', suffix='.txt') as f:
                    for date_iso, nu in absences:
                        f.write(f"{date_iso}\t{nu}\n")
                    result_file = os.path.basename(f.name)
            return render_template('result.html', absences=absences, mail_body=mail_body, result_file=result_file)
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        flash('File not found.', 'danger')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False)
