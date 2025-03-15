from flask import Blueprint, render_template
from app.routes.auth import login_required

manager_bp = Blueprint('manager', __name__)

@manager_bp.route('/manager/dashboard')
@login_required(role=1)  # Only allow managers
def manager_dashboard():
    return render_template('manager/dashboard.html')