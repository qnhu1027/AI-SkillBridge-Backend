from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date


db = SQLAlchemy()


# =====================================================
# USER
# =====================================================

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    # student / admin
    role = db.Column(
        db.String(20),
        default="student",
        nullable=False
    )

    # free / pro
    plan = db.Column(
        db.String(20),
        default="free",
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# =====================================================
# PROFILE
# =====================================================

class Profile(db.Model):

    __tablename__ = "profiles"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    full_name = db.Column(
        db.String(120)
    )

    age = db.Column(
        db.Integer
    )

    major = db.Column(
        db.String(120)
    )

    target_career = db.Column(
        db.String(120)
    )

    career_readiness = db.Column(
        db.Integer,
        default=0
    )


# =====================================================
# AI USAGE
# Free = 3 câu / ngày
# Pro = không giới hạn
# =====================================================

class AIUsage(db.Model):

    __tablename__ = "ai_usage"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    usage_date = db.Column(
        db.Date,
        default=date.today,
        nullable=False
    )

    questions_used = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    __table_args__ = (

        db.UniqueConstraint(
            "user_id",
            "usage_date",
            name="unique_user_ai_usage_day"
        ),

    )


# =====================================================
# AI CHAT HISTORY
# =====================================================

class AIMessage(db.Model):

    __tablename__ = "ai_messages"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # user / assistant
    role = db.Column(
        db.String(20),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# =====================================================
# LEARNING PROGRESS
# =====================================================

class LearningProgress(db.Model):

    __tablename__ = "learning_progress"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    skill = db.Column(
        db.String(120),
        nullable=False
    )

    # not_started / learning / completed
    status = db.Column(
        db.String(30),
        default="not_started",
        nullable=False
    )

    resource_url = db.Column(
        db.Text
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    __table_args__ = (

        db.UniqueConstraint(
            "user_id",
            "skill",
            name="unique_user_skill_progress"
        ),

    )


# =====================================================
# VERIFIED SKILL
# =====================================================

class VerifiedSkill(db.Model):

    __tablename__ = "verified_skills"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    skill = db.Column(
        db.String(120),
        nullable=False
    )

    test_score = db.Column(
        db.Integer,
        default=0
    )

    verified_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    __table_args__ = (

        db.UniqueConstraint(
            "user_id",
            "skill",
            name="unique_verified_user_skill"
        ),

    )


# =====================================================
# PAYMENT REQUEST
# Yêu cầu nâng cấp Free → Pro
# =====================================================

class PaymentRequest(db.Model):

    __tablename__ = "payment_requests"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # pro
    plan = db.Column(
        db.String(20),
        default="pro",
        nullable=False
    )

    # 49000
    amount = db.Column(
        db.Integer,
        default=49000,
        nullable=False
    )

    # pending / approved / rejected
    status = db.Column(
        db.String(20),
        default="pending",
        nullable=False
    )

    # Nội dung chuyển khoản
    transfer_note = db.Column(
        db.String(255)
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    reviewed_at = db.Column(
        db.DateTime,
        nullable=True
    )

    # ID admin xử lý
    reviewed_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )