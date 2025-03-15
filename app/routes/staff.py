from flask import Blueprint, render_template
from app.routes.auth import login_required

staff_bp = Blueprint('staff', __name__)

@staff_bp.route('/staff/dashboard')
@login_required(role=2)  # Only allow staff
def staff_dashboard():
    return render_template('staff/dashboard.html')