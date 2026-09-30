
# ==========================================
# SUPPORT TICKETING SYSTEM
# ==========================================

@app.route('/lecturer/support', methods=['GET', 'POST'])
@login_required
def lecturer_support():
    if current_user.role != 'lecturer':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
        
    lecturer = Lecturer.query.filter_by(user_id=current_user.id).first()
    if not lecturer:
        flash('Lecturer profile not found', 'error')
        return redirect(url_for('logout'))
        
    if request.method == 'POST':
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        if not subject or not message:
            flash('Subject and message are required', 'error')
        else:
            ticket = SupportTicket(
                lecturer_id=lecturer.id,
                subject=subject,
                message=message,
                status='Open'
            )
            db.session.add(ticket)
            db.session.commit()
            flash('Support ticket submitted successfully', 'success')
            return redirect(url_for('lecturer_support'))
            
    tickets = SupportTicket.query.filter_by(lecturer_id=lecturer.id).order_by(SupportTicket.created_at.desc()).all()
    return render_template('lecturer_support.html', tickets=tickets)

@app.route('/admin/support')
@login_required
def admin_support():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
        
    tickets = SupportTicket.query.order_by(
        db.case(
            (SupportTicket.status == 'Open', 1),
            else_=2
        ),
        SupportTicket.created_at.desc()
    ).all()
    
    return render_template('admin_support.html', tickets=tickets)

@app.route('/admin/support/resolve/<int:ticket_id>', methods=['POST'])
@login_required
def admin_resolve_ticket(ticket_id):
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
        
    ticket = SupportTicket.query.get_or_404(ticket_id)
    ticket.status = 'Resolved'
    ticket.resolved_at = datetime.utcnow()
    ticket.resolved_by = current_user.id
    
    db.session.commit()
    flash(f'Ticket #{ticket.id} marked as resolved', 'success')
    return redirect(url_for('admin_support'))

