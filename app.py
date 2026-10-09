from flask import Flask, request, jsonify
from flask_cors import CORS

from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from datetime import datetime, date, timedelta
import os

from models import (
    db,
    User,
    Profile,
    AIUsage,
    AIMessage,
    LearningProgress,
    VerifiedSkill,
    PaymentRequest
)

from ai_service import (
    ask_skillbridge_ai,
    generate_skill_quiz
)


# =====================================================
# APP
# =====================================================

app = Flask(__name__)
CORS(app)


# =====================================================
# DATABASE
# =====================================================

BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///" +
    os.path.join(
        BASE_DIR,
        "skillbridge.db"
    )
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


# =====================================================
# JWT
# =====================================================

app.config["JWT_SECRET_KEY"] = (
    "skillbridge-super-secret-key-2026-ai-platform-secure"
)

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7)

jwt = JWTManager(app)


# =====================================================
# SETTINGS
# =====================================================

FREE_AI_LIMIT = 3
PRO_PRICE = 49000


# =====================================================
# NGÀNH → NGHỀ
# =====================================================

MAJOR_CAREERS = {

    "Công nghệ thông tin": [
        "Frontend Developer",
        "Backend Developer",
        "AI Engineer",
        "DevOps Engineer",
        "Data Analyst"
    ],

    "Kinh tế": [
        "Business Analyst",
        "Financial Analyst",
        "Sales Executive"
    ],

    "Marketing": [
        "Digital Marketing Specialist",
        "Content Marketing Specialist",
        "SEO Specialist"
    ],

    "Kế toán": [
        "Accountant",
        "Auditor",
        "Tax Specialist"
    ],

    "Thiết kế đồ họa": [
        "Graphic Designer",
        "UI/UX Designer",
        "Brand Designer"
    ],

    "Công nghệ kỹ thuật ô tô": [
        "Automotive Engineer",
        "Automotive Technician",
        "Service Advisor"
    ],

    "Ngôn ngữ Anh": [
        "English Teacher",
        "Translator",
        "Content Writer"
    ]
}


# =====================================================
# NGHỀ → KỸ NĂNG
# =====================================================

CAREERS = {

    "Frontend Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "Git",
        "GitHub",
        "React",
        "REST API",
        "Responsive Design"
    ],

    "Backend Developer": [
        "Python",
        "SQL",
        "Git",
        "REST API",
        "Flask",
        "Database",
        "Authentication"
    ],

    "AI Engineer": [
        "Python",
        "SQL",
        "Git",
        "NumPy",
        "Pandas",
        "Machine Learning",
        "Deep Learning",
        "TensorFlow"
    ],

    "DevOps Engineer": [
        "Linux",
        "Git",
        "Docker",
        "AWS",
        "Networking",
        "CI/CD"
    ],

    "Data Analyst": [
        "Excel",
        "SQL",
        "Python",
        "Pandas",
        "Power BI",
        "Data Visualization"
    ],

    "Business Analyst": [
        "Excel",
        "Data Analysis",
        "Communication",
        "Business Process",
        "Problem Solving",
        "SQL"
    ],

    "Financial Analyst": [
        "Excel",
        "Financial Analysis",
        "Accounting",
        "Data Analysis",
        "Financial Modeling",
        "Power BI"
    ],

    "Sales Executive": [
        "Communication",
        "Negotiation",
        "Customer Service",
        "Sales",
        "Presentation",
        "CRM"
    ],

    "Digital Marketing Specialist": [
        "Digital Marketing",
        "Social Media",
        "Content Creation",
        "Google Analytics",
        "Advertising",
        "SEO"
    ],

    "Content Marketing Specialist": [
        "Content Writing",
        "Content Strategy",
        "Social Media",
        "SEO",
        "Canva",
        "Communication"
    ],

    "SEO Specialist": [
        "SEO",
        "Keyword Research",
        "Google Analytics",
        "Content Writing",
        "Technical SEO",
        "Data Analysis"
    ],

    "Accountant": [
        "Accounting",
        "Excel",
        "Financial Reporting",
        "Tax",
        "Bookkeeping",
        "Attention to Detail"
    ],

    "Auditor": [
        "Accounting",
        "Auditing",
        "Excel",
        "Risk Analysis",
        "Financial Reporting",
        "Critical Thinking"
    ],

    "Tax Specialist": [
        "Tax",
        "Accounting",
        "Excel",
        "Tax Law",
        "Financial Reporting",
        "Attention to Detail"
    ],

    "Graphic Designer": [
        "Photoshop",
        "Illustrator",
        "Typography",
        "Color Theory",
        "Layout Design",
        "Creativity"
    ],

    "UI/UX Designer": [
        "Figma",
        "UI Design",
        "UX Research",
        "Wireframing",
        "Prototyping",
        "User Flow"
    ],

    "Brand Designer": [
        "Illustrator",
        "Photoshop",
        "Brand Identity",
        "Typography",
        "Logo Design",
        "Visual Design"
    ],

    "Automotive Engineer": [
        "Automotive Systems",
        "Mechanical Engineering",
        "CAD",
        "Diagnostics",
        "Electrical Systems",
        "Problem Solving"
    ],

    "Automotive Technician": [
        "Vehicle Diagnostics",
        "Engine Systems",
        "Electrical Systems",
        "Maintenance",
        "Repair",
        "Safety"
    ],

    "Service Advisor": [
        "Automotive Knowledge",
        "Customer Service",
        "Communication",
        "Problem Solving",
        "Sales",
        "Scheduling"
    ],

    "English Teacher": [
        "English",
        "Grammar",
        "Speaking",
        "Teaching",
        "Lesson Planning",
        "Communication"
    ],

    "Translator": [
        "English",
        "Translation",
        "Grammar",
        "Writing",
        "Research",
        "Attention to Detail"
    ],

    "Content Writer": [
        "English",
        "Content Writing",
        "Grammar",
        "SEO",
        "Research",
        "Storytelling"
    ]
}


# =====================================================
# HELPER
# =====================================================

def current_user():

    user_id = int(
        get_jwt_identity()
    )

    return db.session.get(
        User,
        user_id
    )


def require_admin():

    user = current_user()

    if not user:

        return None, (
            jsonify({
                "error": "Không tìm thấy tài khoản."
            }),
            404
        )

    if user.role != "admin":

        return None, (
            jsonify({
                "error": "Bạn không có quyền Admin."
            }),
            403
        )

    return user, None


# =====================================================
# HOME
# =====================================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message":
            "AI SkillBridge Backend is running"
    }), 200


# =====================================================
# OPTIONS
# =====================================================

@app.route(
    "/api/options",
    methods=["GET"]
)
def get_options():

    return jsonify({
        "majors": MAJOR_CAREERS
    }), 200


# =====================================================
# REGISTER
# =====================================================

@app.route(
    "/api/register",
    methods=["POST"]
)
def register():

    data = request.get_json() or {}

    full_name = (
        data.get(
            "full_name",
            ""
        ).strip()
    )

    email = (
        data.get(
            "email",
            ""
        ).strip().lower()
    )

    password = data.get(
        "password",
        ""
    )

    if (
        not full_name
        or not email
        or not password
    ):

        return jsonify({
            "error":
                "Vui lòng nhập đầy đủ thông tin."
        }), 400

    if len(password) < 6:

        return jsonify({
            "error":
                "Mật khẩu phải có ít nhất 6 ký tự."
        }), 400

    existing_user = (
        User.query
        .filter_by(
            email=email
        )
        .first()
    )

    if existing_user:

        return jsonify({
            "error":
                "Email này đã được đăng ký."
        }), 409

    new_user = User(

        email=email,

        password=
            generate_password_hash(
                password
            ),

        role="student",

        plan="free"
    )

    db.session.add(
        new_user
    )

    db.session.commit()

    profile = Profile(

        user_id=new_user.id,

        full_name=full_name,

        career_readiness=0
    )

    db.session.add(
        profile
    )

    db.session.commit()

    return jsonify({

        "message":
            "Đăng ký tài khoản thành công.",

        "user": {

            "id":
                new_user.id,

            "full_name":
                full_name,

            "email":
                new_user.email,

            "role":
                new_user.role,

            "plan":
                new_user.plan
        }

    }), 201


# =====================================================
# LOGIN
# =====================================================

@app.route(
    "/api/login",
    methods=["POST"]
)
def login():

    data = request.get_json() or {}

    email = (
        data.get(
            "email",
            ""
        ).strip().lower()
    )

    password = data.get(
        "password",
        ""
    )

    user = (
        User.query
        .filter_by(
            email=email
        )
        .first()
    )

    if (
        not user
        or not check_password_hash(
            user.password,
            password
        )
    ):

        return jsonify({
            "error":
                "Email hoặc mật khẩu không đúng."
        }), 401

    profile = (
        Profile.query
        .filter_by(
            user_id=user.id
        )
        .first()
    )

    token = create_access_token(
        identity=str(
            user.id
        )
    )

    return jsonify({

        "message":
            "Đăng nhập thành công.",

        "token":
            token,

        "user": {

            "id":
                user.id,

            "email":
                user.email,

            "role":
                user.role,

            "plan":
                user.plan,

            "full_name":
                (
                    profile.full_name
                    if profile
                    else ""
                )
        }

    }), 200


# =====================================================
# ME
# =====================================================

@app.route(
    "/api/me",
    methods=["GET"]
)
@jwt_required()
def get_me():

    user = current_user()

    if not user:

        return jsonify({
            "error":
                "Không tìm thấy tài khoản."
        }), 404

    profile = (
        Profile.query
        .filter_by(
            user_id=user.id
        )
        .first()
    )

    return jsonify({

        "user": {

            "id":
                user.id,

            "email":
                user.email,

            "role":
                user.role,

            "plan":
                user.plan
        },

        "profile": {

            "full_name":
                profile.full_name
                if profile
                else "",

            "age":
                profile.age
                if profile
                else None,

            "major":
                profile.major
                if profile
                else "",

            "target_career":
                profile.target_career
                if profile
                else "",

            "career_readiness":
                profile.career_readiness
                if profile
                else 0
        }

    }), 200


# =====================================================
# ANALYZE
# =====================================================

@app.route(
    "/api/analyze",
    methods=["POST"]
)
@jwt_required()
def analyze():

    user = current_user()

    data = request.get_json() or {}

    name = (
        data.get(
            "name",
            ""
        ).strip()
    )

    age = data.get(
        "age"
    )

    major = (
        data.get(
            "major",
            ""
        ).strip()
    )

    career = (
        data.get(
            "career",
            ""
        ).strip()
    )

    current_skills = data.get(
        "skills",
        []
    )

    if major not in MAJOR_CAREERS:

        return jsonify({
            "error":
                "Ngành học không tồn tại."
        }), 400

    if career not in CAREERS:

        return jsonify({
            "error":
                "Nghề nghiệp không tồn tại."
        }), 400

    if career not in MAJOR_CAREERS[major]:

        return jsonify({
            "error":
                "Nghề nghiệp không thuộc ngành đã chọn."
        }), 400

    required_skills = CAREERS[
        career
    ]

    user_skills = [

        skill.strip().lower()

        for skill in current_skills

        if (
            isinstance(
                skill,
                str
            )
            and skill.strip()
        )
    ]

    matched = [

        skill

        for skill
        in required_skills

        if skill.lower()
        in user_skills
    ]

    missing = [

        skill

        for skill
        in required_skills

        if skill.lower()
        not in user_skills
    ]

    readiness = round(

        len(matched)
        /
        len(required_skills)
        *
        100

    ) if required_skills else 0

    profile = (
        Profile.query
        .filter_by(
            user_id=user.id
        )
        .first()
    )

    if not profile:

        profile = Profile(
            user_id=user.id
        )

        db.session.add(
            profile
        )

    profile.full_name = (
        name or
        profile.full_name
    )

    if age:

        try:

            profile.age = int(
                age
            )

        except (
            ValueError,
            TypeError
        ):

            pass

    profile.major = major

    profile.target_career = career

    profile.career_readiness = (
        readiness
    )

    db.session.commit()

    return jsonify({

        "name":
            name,

        "major":
            major,

        "career":
            career,

        "requiredSkills":
            required_skills,

        "matchedSkills":
            matched,

        "missingSkills":
            missing,

        "readiness":
            readiness,

        "matchedCount":
            len(matched),

        "missingCount":
            len(missing),

        "totalRequiredSkills":
            len(required_skills)

    }), 200


# =====================================================
# AI USAGE
# =====================================================

@app.route(
    "/api/ai/usage",
    methods=["GET"]
)
@jwt_required()
def ai_usage():

    user = current_user()

    today = date.today()

    usage = (
        AIUsage.query
        .filter_by(
            user_id=user.id,
            usage_date=today
        )
        .first()
    )

    used = (
        usage.questions_used
        if usage
        else 0
    )

    if user.plan == "pro":

        return jsonify({

            "plan":
                "pro",

            "questions_used":
                used,

            "remaining":
                None,

            "limit":
                None,

            "unlimited":
                True

        }), 200

    remaining = max(

        FREE_AI_LIMIT -
        used,

        0
    )

    return jsonify({

        "plan":
            user.plan,

        "questions_used":
            used,

        "limit":
            FREE_AI_LIMIT,

        "remaining":
            remaining,

        "unlimited":
            False

    }), 200


# =====================================================
# AI HISTORY
# =====================================================

@app.route(
    "/api/ai/history",
    methods=["GET"]
)
@jwt_required()
def ai_history():

    user = current_user()

    data = (

        AIMessage.query
        .filter_by(
            user_id=user.id
        )
        .order_by(
            AIMessage.id.asc()
        )
        .limit(50)
        .all()

    )

    messages = []

    for item in data:

        messages.append({

            "id":
                item.id,

            "role":
                item.role,

            "content":
                item.content,

            "created_at":
                (
                    item.created_at.isoformat()
                    if item.created_at
                    else None
                )
        })

    return jsonify({
        "messages":
            messages
    }), 200


@app.route(
    "/api/ai/history",
    methods=["DELETE"]
)
@jwt_required()
def delete_ai_history():

    user = current_user()

    AIMessage.query.filter_by(
        user_id=user.id
    ).delete()

    db.session.commit()

    return jsonify({
        "message":
            "Đã xóa lịch sử."
    }), 200


# =====================================================
# AI CHAT
# =====================================================

@app.route(
    "/api/ai/chat",
    methods=["POST"]
)
@jwt_required()
def ai_chat():

    user = current_user()

    data = request.get_json() or {}

    message = (
        data.get(
            "message",
            ""
        ).strip()
    )

    if not message:

        return jsonify({
            "error":
                "Vui lòng nhập câu hỏi."
        }), 400

    today = date.today()

    usage = (
        AIUsage.query
        .filter_by(
            user_id=user.id,
            usage_date=today
        )
        .first()
    )

    if not usage:

        usage = AIUsage(

            user_id=user.id,

            usage_date=today,

            questions_used=0
        )

        db.session.add(
            usage
        )

    if (
        user.plan != "pro"
        and
        usage.questions_used
        >= FREE_AI_LIMIT
    ):

        return jsonify({

            "error":
                "Bạn đã sử dụng hết 3 lượt hỏi AI hôm nay.",

            "remaining":
                0,

            "upgrade_required":
                True

        }), 429

    profile = (
        Profile.query
        .filter_by(
            user_id=user.id
        )
        .first()
    )

    profile_data = {

        "full_name":
            (
                profile.full_name
                if profile
                else "Sinh viên"
            ),

        "major":
            (
                profile.major
                if profile
                else ""
            ),

        "target_career":
            (
                profile.target_career
                if profile
                else ""
            ),

        "career_readiness":
            (
                profile.career_readiness
                if profile
                else 0
            )
    }

    old_messages = (

        AIMessage.query
        .filter_by(
            user_id=user.id
        )
        .order_by(
            AIMessage.id.desc()
        )
        .limit(12)
        .all()

    )

    old_messages.reverse()

    history = [

        {
            "role":
                item.role,

            "content":
                item.content
        }

        for item
        in old_messages
    ]

    try:

        answer = ask_skillbridge_ai(

            message=message,

            profile=profile_data,

            history=history
        )

    except Exception as error:

        print(
            "AI ERROR:",
            error
        )

        return jsonify({
            "error":
                "SkillBridge AI đang gặp lỗi."
        }), 500

    db.session.add(

        AIMessage(

            user_id=user.id,

            role="user",

            content=message
        )
    )

    db.session.add(

        AIMessage(

            user_id=user.id,

            role="assistant",

            content=answer
        )
    )

    usage.questions_used += 1

    db.session.commit()

    remaining = (

        None

        if user.plan == "pro"

        else max(
            FREE_AI_LIMIT -
            usage.questions_used,
            0
        )
    )

    return jsonify({

        "answer":
            answer,

        "plan":
            user.plan,

        "questions_used":
            usage.questions_used,

        "remaining":
            remaining,

        "unlimited":
            user.plan == "pro"

    }), 200


# =====================================================
# PAYMENT - USER
# =====================================================

@app.route(
    "/api/payments/request",
    methods=["POST"]
)
@jwt_required()
def request_payment():

    user = current_user()

    if user.plan == "pro":

        return jsonify({
            "error":
                "Tài khoản của bạn đã là Pro."
        }), 400

    existing = (
        PaymentRequest.query
        .filter_by(
            user_id=user.id,
            status="pending"
        )
        .first()
    )

    if existing:

        return jsonify({

            "message":
                "Bạn đã có yêu cầu đang chờ xác nhận.",

            "payment": {

                "id":
                    existing.id,

                "status":
                    existing.status,

                "amount":
                    existing.amount
            }

        }), 200

    transfer_note = (
        f"SKILLBRIDGE PRO USER {user.id}"
    )

    payment = PaymentRequest(

        user_id=user.id,

        plan="pro",

        amount=PRO_PRICE,

        status="pending",

        transfer_note=transfer_note
    )

    db.session.add(
        payment
    )

    db.session.commit()

    return jsonify({

        "message":
            "Đã gửi yêu cầu nâng cấp Pro.",

        "payment": {

            "id":
                payment.id,

            "status":
                payment.status,

            "amount":
                payment.amount,

            "transfer_note":
                payment.transfer_note
        }

    }), 201


# =====================================================
# PAYMENT STATUS USER
# =====================================================

@app.route(
    "/api/payments/my",
    methods=["GET"]
)
@jwt_required()
def my_payment():

    user = current_user()

    payment = (

        PaymentRequest.query
        .filter_by(
            user_id=user.id
        )
        .order_by(
            PaymentRequest.id.desc()
        )
        .first()

    )

    if not payment:

        return jsonify({
            "payment":
                None
        }), 200

    return jsonify({

        "payment": {

            "id":
                payment.id,

            "plan":
                payment.plan,

            "amount":
                payment.amount,

            "status":
                payment.status,

            "transfer_note":
                payment.transfer_note,

            "created_at":
                (
                    payment.created_at.isoformat()
                    if payment.created_at
                    else None
                ),

            "reviewed_at":
                (
                    payment.reviewed_at.isoformat()
                    if payment.reviewed_at
                    else None
                )
        }

    }), 200


# =====================================================
# ADMIN - PAYMENT LIST
# =====================================================

@app.route(
    "/api/admin/payments",
    methods=["GET"]
)
@jwt_required()
def admin_payments():

    admin, error = (
        require_admin()
    )

    if error:
        return error

    payments = (

        PaymentRequest.query
        .order_by(
            PaymentRequest.id.desc()
        )
        .all()

    )

    result = []

    for payment in payments:

        user = db.session.get(
            User,
            payment.user_id
        )

        profile = (
            Profile.query
            .filter_by(
                user_id=payment.user_id
            )
            .first()
        )

        result.append({

            "id":
                payment.id,

            "user_id":
                payment.user_id,

            "email":
                (
                    user.email
                    if user
                    else ""
                ),

            "full_name":
                (
                    profile.full_name
                    if profile
                    else ""
                ),

            "amount":
                payment.amount,

            "status":
                payment.status,

            "plan":
                payment.plan,

            "transfer_note":
                payment.transfer_note,

            "created_at":
                (
                    payment.created_at.isoformat()
                    if payment.created_at
                    else None
                )
        })

    return jsonify({
        "payments":
            result
    }), 200


# =====================================================
# ADMIN - APPROVE
# =====================================================

@app.route(
    "/api/admin/payments/<int:payment_id>/approve",
    methods=["POST"]
)
@jwt_required()
def approve_payment(
    payment_id
):

    admin, error = (
        require_admin()
    )

    if error:
        return error

    payment = db.session.get(
        PaymentRequest,
        payment_id
    )

    if not payment:

        return jsonify({
            "error":
                "Không tìm thấy yêu cầu thanh toán."
        }), 404

    if payment.status == "approved":

        return jsonify({
            "message":
                "Yêu cầu này đã được duyệt."
        }), 200

    user = db.session.get(
        User,
        payment.user_id
    )

    if not user:

        return jsonify({
            "error":
                "Không tìm thấy người dùng."
        }), 404

    payment.status = "approved"

    payment.reviewed_at = (
        datetime.utcnow()
    )

    payment.reviewed_by = (
        admin.id
    )

    user.plan = "pro"

    db.session.commit()

    return jsonify({

        "message":
            "Đã duyệt thanh toán. Tài khoản đã được nâng cấp Pro.",

        "user": {

            "id":
                user.id,

            "email":
                user.email,

            "plan":
                user.plan
        }

    }), 200


# =====================================================
# ADMIN - REJECT
# =====================================================

@app.route(
    "/api/admin/payments/<int:payment_id>/reject",
    methods=["POST"]
)
@jwt_required()
def reject_payment(
    payment_id
):

    admin, error = (
        require_admin()
    )

    if error:
        return error

    payment = db.session.get(
        PaymentRequest,
        payment_id
    )

    if not payment:

        return jsonify({
            "error":
                "Không tìm thấy yêu cầu thanh toán."
        }), 404

    payment.status = "rejected"

    payment.reviewed_at = (
        datetime.utcnow()
    )

    payment.reviewed_by = (
        admin.id
    )

    db.session.commit()

    return jsonify({
        "message":
            "Đã từ chối yêu cầu thanh toán."
    }), 200

# =====================================================
# SKILL TEST - VERIFY SKILL
# =====================================================

# =====================================================
# AI GENERATE SKILL TEST
# =====================================================

@app.route(
    "/api/tests/generate",
    methods=["POST"]
)
@jwt_required()
def generate_test():

    user = current_user()

    if not user:

        return jsonify({
            "error":
                "Không tìm thấy người dùng."
        }), 404


    data = request.get_json() or {}

    skill = (
        data
        .get("skill", "")
        .strip()
    )


    if not skill:

        return jsonify({
            "error":
                "Vui lòng chọn kỹ năng."
        }), 400


    profile_model = (
        Profile.query
        .filter_by(
            user_id=user.id
        )
        .first()
    )


    profile = {}


    if profile_model:

        profile = {

            "full_name":
                profile_model.full_name,

            "major":
                profile_model.major,

            "target_career":
                profile_model.target_career,

            "career_readiness":
                profile_model.career_readiness

        }


    questions = generate_skill_quiz(
        skill,
        profile
    )


    if not questions:

        return jsonify({
            "error":
                "AI chưa tạo được bài kiểm tra. Vui lòng thử lại."
        }), 500


    return jsonify({

        "skill":
            skill,

        "total_questions":
            len(questions),

        "questions":
            questions

    }), 200
@app.route(
    "/api/tests/verify",
    methods=["POST"]
)
@jwt_required()
def verify_skill():

    user = current_user()

    data = request.get_json() or {}

    skill = (
        data.get(
            "skill",
            ""
        ).strip()
    )

    score = data.get(
        "score",
        0
    )

    if not skill:

        return jsonify({
            "error": "Không có kỹ năng."
        }), 400


    try:

        score = int(score)

    except (
        ValueError,
        TypeError
    ):

        return jsonify({
            "error": "Điểm không hợp lệ."
        }), 400


    if score < 70:

        return jsonify({
            "error":
                "Cần đạt ít nhất 70% để xác thực kỹ năng."
        }), 400


    verified = (
        VerifiedSkill.query
        .filter_by(
            user_id=user.id,
            skill=skill
        )
        .first()
    )


    if verified:

        if score > verified.test_score:

            verified.test_score = score

            verified.verified_at = (
                datetime.utcnow()
            )

    else:

        verified = VerifiedSkill(

            user_id=user.id,

            skill=skill,

            test_score=score
        )

        db.session.add(
            verified
        )


    db.session.commit()


    return jsonify({

        "message":
            "Kỹ năng đã được xác thực.",

        "verified_skill": {

            "skill":
                verified.skill,

            "score":
                verified.test_score,

            "verified":
                True
        }

    }), 200

# =====================================================
# GET VERIFIED SKILLS
# =====================================================

@app.route(
    "/api/tests/verified",
    methods=["GET"]
)
@jwt_required()
def get_verified_skills():

    user = current_user()

    skills = (
        VerifiedSkill.query
        .filter_by(
            user_id=user.id
        )
        .order_by(
            VerifiedSkill.verified_at.desc()
        )
        .all()
    )

    result = []

    for item in skills:

        result.append({

            "id":
                item.id,

            "skill":
                item.skill,

            "score":
                item.test_score,

            "verified_at":
                (
                    item.verified_at.isoformat()
                    if item.verified_at
                    else None
                )

        })

    return jsonify({

        "verified_skills":
            result

    }), 200

# =====================================================
# ADMIN - THỐNG KÊ
# =====================================================

@app.route(
    "/api/admin/stats",
    methods=["GET"]
)
@jwt_required()
def admin_stats():

    admin, error = require_admin()

    if error:
        return error


    students = (
        User.query
        .filter_by(
            role="student"
        )
        .all()
    )


    total_users = len(students)


    free_users = len([
        user
        for user in students
        if user.plan == "free"
    ])


    pro_users = len([
        user
        for user in students
        if user.plan == "pro"
    ])


    verified_skills = (
        VerifiedSkill.query.count()
    )


    pending_payments = (
        PaymentRequest.query
        .filter_by(
            status="pending"
        )
        .count()
    )


    return jsonify({

        "total_users":
            total_users,

        "free_users":
            free_users,

        "pro_users":
            pro_users,

        "verified_skills":
            verified_skills,

        "pending_payments":
            pending_payments

    }), 200


# =====================================================
# ADMIN - DANH SÁCH NGƯỜI DÙNG
# =====================================================

@app.route(
    "/api/admin/users",
    methods=["GET"]
)
@jwt_required()
def admin_users():

    admin, error = require_admin()

    if error:
        return error


    users = (
        User.query
        .filter_by(
            role="student"
        )
        .order_by(
            User.id.desc()
        )
        .all()
    )


    result = []


    for user in users:

        profile = (
            Profile.query
            .filter_by(
                user_id=user.id
            )
            .first()
        )


        verified_count = (
            VerifiedSkill.query
            .filter_by(
                user_id=user.id
            )
            .count()
        )


        result.append({

            "id":
                user.id,

            "email":
                user.email,

            "plan":
                user.plan,

            "full_name":
                (
                    profile.full_name
                    if profile
                    else ""
                ),

            "major":
                (
                    profile.major
                    if profile
                    else ""
                ),

            "target_career":
                (
                    profile.target_career
                    if profile
                    else ""
                ),

            "career_readiness":
                (
                    profile.career_readiness
                    if profile
                    else 0
                ),

            "verified_skills":
                verified_count,

            "created_at":
                (
                    user.created_at.isoformat()
                    if user.created_at
                    else None
                )

        })


    return jsonify({

        "users":
            result

    }), 200

# =====================================================
# RUN
# =====================================================

if __name__ == "__main__":

    with app.app_context():

        db.create_all()

    print(
        "Database ready!"
    )

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True
    )