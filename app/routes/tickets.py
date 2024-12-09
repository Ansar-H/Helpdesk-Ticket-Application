from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Ticket, Comment
from app.forms import TicketForm, CommentForm
from app import db
from datetime import datetime
from flask import session

bp = Blueprint('tickets', __name__)

# Route to list all tickets
@bp.route('/tickets')
@login_required
def list_tickets():
    if current_user.is_admin:
        # Makes sure only the admin can see all tickets
        tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    else:
        # Regular users can only see their own tickets
        tickets = Ticket.query.filter_by(author=current_user).order_by(Ticket.created_at.desc()).all()
    return render_template('tickets/list.html', tickets=tickets)

# The route to create a new ticket
@bp.route('/tickets/create', methods=['GET', 'POST'])
@login_required
def create_ticket():
    form = TicketForm()
    if form.validate_on_submit():
        ticket = Ticket(
            title=form.title.data,
            description=form.description.data,
            priority=form.priority.data,
            author=current_user
        )
        db.session.add(ticket)
        db.session.commit()
        
        # Clear existing flash messages and add new one
        session.pop('_flashes', None)
        flash('Ticket has been created!', 'success')
        
        return redirect(url_for('tickets.list_tickets'))
    return render_template('tickets/create.html', form=form)

# Route to add a comment to a ticket
@bp.route('/tickets/<int:ticket_id>/comment', methods=['POST'])
@login_required
def add_comment(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    form = CommentForm()
    
    if form.validate_on_submit():
        # Create and save the new comment
        comment = Comment(
            content=form.content.data,
            author=current_user,
            ticket=ticket
        )
        db.session.add(comment)
        db.session.commit()
        flash('Comment added successfully!', 'success')
    
    return redirect(url_for('tickets.view_ticket', id=ticket_id))

# The route to view a psecific ticket
@bp.route('/tickets/<int:id>')
@login_required
def view_ticket(id):
    ticket = Ticket.query.get_or_404(id)
    form = CommentForm()
    return render_template('tickets/view.html', ticket=ticket, form=form)

# The route to update an existing ticket
@bp.route('/tickets/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_ticket(id):
    ticket = Ticket.query.get_or_404(id)
    # Check that the user has permission to edit this ticket
    if not current_user.is_admin and ticket.author != current_user:
        flash('You cannot modify this ticket.')
        return redirect(url_for('tickets.view_ticket', id=id))
    
    form = TicketForm()
    if form.validate_on_submit():
        # This updates the ticket fields with form data
        ticket.title = form.title.data
        ticket.description = form.description.data
        ticket.priority = form.priority.data
        ticket.updated_at = datetime.now()
        db.session.commit()
        flash('Ticket has been updated successfully.', 'success')
        return redirect(url_for('tickets.view_ticket', id=id))
    elif request.method == 'GET':
        form.title.data = ticket.title
        form.description.data = ticket.description
        form.priority.data = ticket.priority
    return render_template('tickets/update.html', form=form, ticket=ticket)

# The final route to delete a ticket
@bp.route('/tickets/<int:id>/delete', methods=['GET'])
@login_required
def delete_ticket(id):
    # This statement makes sure that only an admin can delete tikcets
    if not current_user.is_admin:
        flash('Only administrators can delete tickets.')
        return redirect(url_for('tickets.list_tickets'))
    
    ticket = Ticket.query.get_or_404(id)
    db.session.delete(ticket)
    db.session.commit()
    flash('Ticket has been deleted successfully.', 'success')
    return redirect(url_for('tickets.list_tickets'))