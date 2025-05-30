from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import Contact
from schemas import IdentifyRequest
from datetime import datetime


def identify_contact_logic(req: IdentifyRequest, db: Session):
    email = req.email
    phone = req.phonenumber

    if not email and not phone:
        raise ValueError("At least one of email or phoneNumber is required.")

    # 1. Fetch matching contacts
    matched_contacts = db.query(Contact).filter(
        or_(
            Contact.email == email,
            Contact.phonenumber == phone
        )
    ).all()

    if not matched_contacts:
        # 2. No contact exists, create a new primary
        new_contact = Contact(
            email=email,
            phonenumber=phone,
            linkprecedence='primary',
            createdat=datetime.utcnow()
        )
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)

        return {
            "contact": {
                "primarycontactid": new_contact.id,
                "emails": [new_contact.email] if new_contact.email else [],
                "phonenumbers": [new_contact.phonenumber] if new_contact.phonenumber else [],
                "secondarycontactids": []
            }
        }

    # 3. Determine primary contact (minimum createdAt)
    primary_contact = min(
        [c for c in matched_contacts if c.linkprecedence == 'primary'],
        key=lambda c: c.createdat,
        default=matched_contacts[0]
    )

    all_related_contacts = db.query(Contact).filter(
        or_(
            Contact.email.in_([c.email for c in matched_contacts if c.email]),
            Contact.phonenumber.in_([c.phonenumber for c in matched_contacts if c.phonenumber])
        )
    ).all()

    # 4. Check if this email+phone combination already exists
    existing = next((c for c in all_related_contacts if c.email == email and c.phonenumber == phone), None)

    if not existing:
        # New unique email+phone: create a secondary contact
        new_secondary = Contact(
            email=email,
            phonenumber=phone,
            linkedid=primary_contact.id,
            linkprecedence="secondary",
            createdat=datetime.utcnow()
        )
        db.add(new_secondary)
        db.commit()
        db.refresh(new_secondary)
        all_related_contacts.append(new_secondary)

    # 5. Normalize contacts
    emails = []
    phones = []
    secondary_ids = []
    for c in all_related_contacts:
        if c.linkprecedence == "primary" and c.id != primary_contact.id:
            # Convert to secondary
            c.linkprecedence = "secondary"
            c.linkedid = primary_contact.id
            db.add(c)
            db.commit()

        if c.email and c.email not in emails:
            emails.append(c.email)

        if c.phonenumber and c.phonenumber not in phones:
            phones.append(c.phonenumber)

        if c.linkprecedence == "secondary":
            secondary_ids.append(c.id)

    return {
        "contact": {
            "primarycontactid": primary_contact.id,
            "emails": [primary_contact.email] + [e for e in emails if e != primary_contact.email],
            "phonenumbers": [primary_contact.phonenumber] + [p for p in phones if p != primary_contact.phonenumber],
            "secondarycontactids": secondary_ids
        }
    }
