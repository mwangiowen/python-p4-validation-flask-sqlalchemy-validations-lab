from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates("name")
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Author must have a name")
        return name

    @validates("phone_number")
    def validate_phone_number(self, key, phone_number):
        if not phone_number or not phone_number.isdigit() or len(phone_number) != 10:
            raise ValueError(
                "Invalid phone number format. It must be exactly ten digits."
            )
        return phone_number

    def __repr__(self):
        return f"Author(id={self.id}, name={self.name})"


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"))
    author = db.relationship("Author", back_populates="posts")

    @validates("title")
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Post must have a title")

        # Ensure the title is sufficiently clickbait-y
        clickbait_keywords = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(keyword in title for keyword in clickbait_keywords):
            raise ValueError(
                "Title must be sufficiently clickbait-y. It should contain one of: 'Won't Believe', 'Secret', 'Top [number]', 'Guess'"
            )

        return title

    @validates("content")
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Post content must be at least 250 characters long")
        return content

    @validates("summary")
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Post summary cannot exceed 250 characters")
        return summary

    @validates("category")
    def validate_category(self, key, category):
        allowed_categories = ["Fiction", "Non-Fiction"]
        if category not in allowed_categories:
            raise ValueError(
                f"Invalid category. Allowed categories are: {', '.join(allowed_categories)}"
            )
        return category

    def __repr__(self):
        return f"Post(id={self.id}, title={self.title}, content={self.content}, summary={self.summary})"
