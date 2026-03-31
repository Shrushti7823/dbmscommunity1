from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import os
from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)
app.secret_key = 'f9f88869b6851a74e751dc485d655dae'

# MongoDB config
app.config["MONGO_URI"] = "mongodb://localhost:27017/communityDB"
mongo = PyMongo(app)
faculties_collection = mongo.db.faculties
communities_collection = mongo.db.communities
branches_collection = mongo.db.branches

# Upload folder
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ------------------ ROUTES ------------------

@app.route('/')
def index():
    communities = list(mongo.db.communities.find())
    for c in communities:
        c['_id'] = str(c['_id'])
    return render_template('index.html', communities=communities)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'Rutuja' and request.form['password'] == 'rutuja123':
            session['admin_logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash("Invalid credentials", "danger")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

@app.route('/<branch>')
def branch_page(branch):
    branch_lower = branch.lower()
    communities = list(mongo.db.communities.find({'branch': branch_lower}))
    for c in communities:
        c['_id'] = str(c['_id'])
    return render_template('branch.html', communities=communities, branch=branch_lower)

# @app.route('/form/<branch>', methods=['GET', 'POST'])
# def form(branch):
#     branch_lower = branch.lower()
#     if request.method == 'POST':
#         community_name = request.form['community_name']
#         logo = request.files['community_logo']
#         description = request.form['description']
#         photos = request.files.getlist('photos')
#         faculty_name = request.form['faculty_name']
#         faculty_link = request.form['faculty_link']

#         # Save logo
#         if logo.filename:
#             logo_filename = secure_filename(logo.filename)
#             logo_path = os.path.join(app.config['UPLOAD_FOLDER'], logo_filename)
#             logo.save(logo_path)
#             logo_url = f"uploads/{logo_filename}"  # ✅ Corrected
#         else:
#             logo_url = ""

#         # Save photos
#         photo_paths = []
#         for photo in photos:
#             if photo.filename:
#                 filename = secure_filename(photo.filename)
#                 path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#                 photo.save(path)
#                 photo_paths.append(f"uploads/{filename}")  # ✅ Corrected

#         data = {
#             'branch': branch_lower,
#             'community_name': community_name,
#             'description': description,
#             'faculty_name': faculty_name,
#             'faculty_link': faculty_link,
#             'logo_path': logo_url,
#             'photos': photo_paths
#         }

#         inserted = mongo.db.communities.insert_one(data)
#         inserted_id = str(inserted.inserted_id)
#         return redirect(url_for('community_view', community_id=inserted_id))

#     return render_template('form.html', branch=branch_lower)

@app.route('/form/<branch>', methods=['GET', 'POST'])
def form(branch):
    branch_lower = branch.lower()
    if request.method == 'POST':
        community_name = request.form['community_name']
        logo = request.files['community_logo']
        description = request.form['description']
        photos = request.files.getlist('photos')
        faculty_name = request.form['faculty_name']
        faculty_link = request.form['faculty_link']

        # Save logo
        logo_url = ""
        if logo.filename:
            logo_filename = secure_filename(logo.filename)
            logo_path = os.path.join(app.config['UPLOAD_FOLDER'], logo_filename)
            logo.save(logo_path)
            logo_url = f"uploads/{logo_filename}"  # 🔥 don't add /static/

        # Save photos
        photo_paths = []
        for photo in photos:
            if photo.filename:
                filename = secure_filename(photo.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                photo.save(path)
                photo_paths.append(f"uploads/{filename}")  # 🔥 same here

        data = {
            'branch': branch_lower,
            'community_name': community_name,
            'description': description,
            'faculty_name': faculty_name,
            'faculty_link': faculty_link,
            'logo_path': logo_url,
            'photos': photo_paths
        }

        inserted = mongo.db.communities.insert_one(data)
        return redirect(url_for('community_view', community_id=str(inserted.inserted_id)))

    return render_template('form.html', branch=branch_lower)

@app.route('/community/<community_id>')
def community_view(community_id):
    try:
        community = mongo.db.communities.find_one({'_id': ObjectId(community_id)})
        if not community:
            return "Community not found", 404
        return render_template('community.html', data=community)
    except Exception as e:
        print("Error loading community:", e)
        return "Invalid community ID", 400

@app.route('/delete_community/<community_id>', methods=['POST'])
def delete_community(community_id):
    if not session.get('admin_logged_in'):
        flash("You need to be logged in as admin to delete a community.", "danger")
        return redirect(url_for('login'))
    try:
        result = mongo.db.communities.delete_one({'_id': ObjectId(community_id)})
        if result.deleted_count == 1:
            flash("Community deleted successfully.", "success")
        else:
            flash("Community not found.", "warning")
    except Exception as e:
        print("Error deleting community:", e)
        flash("Error deleting community.", "danger")
    return redirect(url_for('index'))

# Static community pages
@app.route('/csi')      
def csi(): return render_template('CSI.html')
@app.route('/debugger') 
def debugger(): return render_template('debugger.html')
@app.route('/iteron')    
def iteron(): return render_template('ITERON.html')
@app.route('/PHOENIX')   
def PHOENIX(): return render_template('phoeni.html')
@app.route('/desoc')     
def desoc(): return render_template('Desoc.html')
@app.route('/telekinesis') 
def telekinesis(): return render_template('Telekinesis.html')
# @app.route('/iet')
# def elec(): return render_template('IET Expo.html')
@app.route('/sara')      
def sara(): return render_template('SARA.html')
@app.route('/chemfest')  
def chem(): return render_template('CHEMFEST.html')
@app.route('/mesa')      
def mesa(): return render_template('MESA.html')
@app.route('/cesa')      
def cesa(): return render_template('CESA.html')


@app.route('/dashboard')
def dashboard():
    # Assuming you use MongoDB
    total_faculties = faculties_collection.count_documents({})
    total_communities = communities_collection.count_documents({})
    total_branches = len(branches_collection.distinct('branch_name'))

    return render_template('dashboard.html',
                           total_faculties=total_faculties,
                           total_communities=total_communities,
                           total_branches=total_branches)

                           
if __name__ == '__main__':
    app.run(debug=True)   