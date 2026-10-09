from getpass import getpass

from app import app
from models import db, User, Profile

from werkzeug.security import generate_password_hash


with app.app_context():

    print("=== TẠO TÀI KHOẢN ADMIN ===")

    full_name = input(
        "Tên Admin: "
    ).strip()

    email = input(
        "Email Admin: "
    ).strip().lower()

    password = getpass(
        "Mật khẩu Admin: "
    )


    if not full_name or not email or not password:

        print(
            "Không được để trống thông tin."
        )

        exit()


    if len(password) < 6:

        print(
            "Mật khẩu phải có ít nhất 6 ký tự."
        )

        exit()


    existing_user = (
        User.query
        .filter_by(
            email=email
        )
        .first()
    )


    if existing_user:

        existing_user.role = "admin"

        existing_user.password = (
            generate_password_hash(
                password
            )
        )

        existing_user.plan = "pro"


        profile = (
            Profile.query
            .filter_by(
                user_id=existing_user.id
            )
            .first()
        )


        if profile:

            profile.full_name = full_name

        else:

            profile = Profile(

                user_id=existing_user.id,

                full_name=full_name,

                career_readiness=0
            )

            db.session.add(
                profile
            )


        db.session.commit()


        print(
            "Đã chuyển tài khoản thành Admin."
        )


    else:

        new_admin = User(

            email=email,

            password=
                generate_password_hash(
                    password
                ),

            role="admin",

            plan="pro"
        )


        db.session.add(
            new_admin
        )

        db.session.flush()


        profile = Profile(

            user_id=new_admin.id,

            full_name=full_name,

            career_readiness=0
        )


        db.session.add(
            profile
        )

        db.session.commit()


        print(
            "Tạo tài khoản Admin thành công."
        )


    print(
        "Email:",
        email
    )