import os
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# In-memory user data (for demonstration purposes)
user_profile = {
    'name': '',
    'email': '',
    'gender': ''
}

knowledge_list = []  # In-memory storage for shared knowledge
case_study_links = []  # Store case study links

# Store links for SustainShe categories
sustain_she_links = {
    "empowerment_resources": [],  # Updated keys
    "success_stories": [],         # Updated keys
    "upcoming_events": [],         # Updated keys
    "educational_resources": []     # Updated keys
}

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Profile route
@app.route('/profile')
def profile():
    return render_template('profile.html', profile=user_profile)

# Edit Profile route
@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    if request.method == 'POST':
        user_profile['name'] = request.form.get('name')
        user_profile['email'] = request.form.get('email')
        user_profile['gender'] = request.form.get('gender')
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    return render_template('edit-profile.html', profile=user_profile)

# Case Studies route
@app.route('/case-studies', methods=['GET', 'POST'])
def case_studies():
    if request.method == 'POST':
        link = request.form.get('link')
        if link:
            case_study_links.append(link)
            flash('Case study added successfully!', 'success')
        return redirect(url_for('case_studies'))
    return render_template('case-studies.html', case_study_links=case_study_links)

# Knowledge Sharing route
@app.route('/knowledge-sharing', methods=['GET'])
def knowledge_sharing():
    return render_template('knowledge-sharing.html', knowledge_list=knowledge_list)

# Submit Knowledge route
@app.route('/submit-knowledge', methods=['POST'])
def submit_knowledge():
    knowledge = request.form.get('knowledge')
    name = request.form.get('name')
    image = request.files.get('image')

    if image and allowed_file(image.filename):
        image.save(os.path.join('static/uploads', image.filename))
        knowledge_list.append({'name': name, 'knowledge': knowledge, 'image': image.filename})
    else:
        knowledge_list.append({'name': name, 'knowledge': knowledge, 'image': None})
    
    return redirect(url_for('knowledge_sharing'))

# Function to check allowed file types for image uploads
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png'}

# SustainShe route
@app.route('/sustainshe', methods=['GET', 'POST'])
def sustainshe():
    if request.method == 'POST':
        topic = request.form.get('topic')
        link = request.form.get('link')
        if topic in sustain_she_links and link:
            sustain_she_links[topic].append(link)
            flash(f'Link added to {topic} successfully!', 'success')
        return redirect(url_for('sustainshe'))
    return render_template('sustainshe.html', sustain_she_links=sustain_she_links)

if __name__ == '__main__':
    app.run(debug=True)
