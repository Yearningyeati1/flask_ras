from flask import Blueprint, render_template
from app.routes.auth import login_required

supplier_bp = Blueprint('supplier', __name__)

@supplier_bp.route('/supplier/dashboard')
@login_required(role=3)  # Only allow suppliers
def supplier_dashboard():
    return render_template('supplier/dashboard.html')