from flask import Flask, render_template, request, redirect, url_for, flash
import boto3
import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

app = Flask(__name__)
app.secret_key = 'aws'


AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
S3_BUCKET = os.environ.get('S3_BUCKET')


s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part in the request')
        return redirect(url_for('index'))

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))

    if file:
        try:
            s3_client.upload_fileobj(
                file,
                S3_BUCKET,
                file.filename
            )
            flash(f'File {file.filename} uploaded successfully!')
            return redirect(url_for('index'))
        except (NoCredentialsError, PartialCredentialsError):
            flash('AWS credentials not provided or invalid.')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error occurred: {str(e)}')
            return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
