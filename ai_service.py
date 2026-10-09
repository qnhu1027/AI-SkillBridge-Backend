import random
import requests


# =====================================================
# OLLAMA SETTINGS
# =====================================================

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
OLLAMA_MODEL = "qwen2.5:1.5b"


# =====================================================
# AI CHAT
# =====================================================

def ask_skillbridge_ai(
    message,
    profile=None,
    history=None
):

    profile = profile or {}
    history = history or []

    full_name = (
        profile.get("full_name")
        or "Sinh viên"
    )

    major = (
        profile.get("major")
        or "Chưa thiết lập"
    )

    target_career = (
        profile.get("target_career")
        or "Chưa thiết lập"
    )

    readiness = (
        profile.get("career_readiness")
        or 0
    )

    system_prompt = f"""
Bạn là SkillBridge AI, trợ giảng AI dành cho sinh viên.

Thông tin sinh viên:
- Tên: {full_name}
- Ngành: {major}
- Nghề mục tiêu: {target_career}
- Career Readiness: {readiness}%

Quy tắc:
- Ưu tiên tiếng Việt.
- Trả lời ngắn gọn, dễ hiểu.
- Trả lời đúng trọng tâm.
- Cá nhân hóa theo ngành và nghề mục tiêu.
- Không tự bịa thông tin cá nhân.

Nếu sinh viên học Công nghệ thông tin:
- ưu tiên ví dụ code khi phù hợp
- hỗ trợ Python, JavaScript, HTML, CSS, SQL
- hỗ trợ Git, Database, API, Web, AI, Networking
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    for item in history[-4:]:

        role = item.get(
            "role",
            "user"
        )

        content = item.get(
            "content",
            ""
        )

        if (
            role in ["user", "assistant"]
            and content
        ):

            messages.append({
                "role": role,
                "content": content
            })

    messages.append({
        "role": "user",
        "content": message
    })

    payload = {

        "model": OLLAMA_MODEL,

        "messages": messages,

        "stream": False,

        "keep_alive": "1h",

        "options": {
            "temperature": 0.4,
            "num_ctx": 1536,
            "num_predict": 180
        }

    }

    try:

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        answer = (
            data
            .get("message", {})
            .get("content", "")
            .strip()
        )

        if not answer:

            return (
                "SkillBridge AI chưa tạo được "
                "câu trả lời."
            )

        return answer

    except requests.exceptions.ConnectionError:

        return (
            "Không kết nối được Ollama. "
            "Hãy kiểm tra Ollama đang chạy."
        )

    except requests.exceptions.Timeout:

        return (
            "AI phản hồi hơi lâu. "
            "Vui lòng thử lại."
        )

    except Exception as error:

        print(
            "OLLAMA CHAT ERROR:",
            error
        )

        return (
            "SkillBridge AI đang gặp lỗi."
        )


# =====================================================
# QUESTION BANK
# =====================================================

QUIZ_BANK = {


    # =================================================
    # PYTHON
    # =================================================

    "python": [

        {
            "question":
                "Lệnh nào dùng để in dữ liệu trong Python?",

            "options": [
                "print()",
                "echo()",
                "console.log()",
                "show()"
            ],

            "answer": 0
        },

        {
            "question":
                "Kiểu dữ liệu nào dùng để lưu danh sách?",

            "options": [
                "list",
                "int",
                "bool",
                "float"
            ],

            "answer": 0
        },

        {
            "question":
                "Kết quả của len([1, 2, 3]) là gì?",

            "options": [
                "2",
                "3",
                "4",
                "6"
            ],

            "answer": 1
        },

        {
            "question":
                "Từ khóa nào dùng để khai báo hàm?",

            "options": [
                "function",
                "def",
                "func",
                "method"
            ],

            "answer": 1
        },

        {
            "question":
                "Đoạn code print(2 + 3 * 2) in ra gì?",

            "options": [
                "10",
                "8",
                "7",
                "12"
            ],

            "answer": 1
        },

        {
            "question":
                "Phương thức nào thêm phần tử cuối list?",

            "options": [
                "append()",
                "push()",
                "add()",
                "insertLast()"
            ],

            "answer": 0
        },

        {
            "question":
                "range(3) tạo ra các giá trị nào?",

            "options": [
                "0, 1, 2",
                "1, 2, 3",
                "0, 1, 2, 3",
                "1, 2"
            ],

            "answer": 0
        },

        {
            "question":
                "Kết quả của print('AI' * 2) là gì?",

            "options": [
                "AIAI",
                "AI2",
                "AI AI",
                "Lỗi"
            ],

            "answer": 0
        },

        {
            "question":
                "Cấu trúc nào lưu dữ liệu key-value?",

            "options": [
                "dictionary",
                "list",
                "tuple",
                "set"
            ],

            "answer": 0
        },

        {
            "question":
                "Điều kiện if x == 5 kiểm tra điều gì?",

            "options": [
                "x bằng 5",
                "gán 5 cho x",
                "x khác 5",
                "x lớn hơn 5"
            ],

            "answer": 0
        },

        {
            "question":
                "Từ khóa nào tạo một lớp trong Python?",

            "options": [
                "class",
                "object",
                "struct",
                "new"
            ],

            "answer": 0
        },

        {
            "question":
                "Đoạn code x = [1,2]; x.append(3) tạo list nào?",

            "options": [
                "[1, 2, 3]",
                "[3, 1, 2]",
                "[1, 2]",
                "[1, 2, [3]]"
            ],

            "answer": 0
        },

        {
            "question":
                "Toán tử nào kiểm tra hai giá trị bằng nhau?",

            "options": [
                "==",
                "=",
                "!=",
                ">="
            ],

            "answer": 0
        },

        {
            "question":
                "Hàm input() thường trả về kiểu dữ liệu nào?",

            "options": [
                "str",
                "int",
                "float",
                "bool"
            ],

            "answer": 0
        },

        {
            "question":
                "Lỗi nào xảy ra khi dùng một biến chưa được khai báo?",

            "options": [
                "NameError",
                "IndexError",
                "KeyError",
                "ZeroDivisionError"
            ],

            "answer": 0
        }

    ],


    # =================================================
    # SQL
    # =================================================

    "sql": [

        {
            "question":
                "Lệnh nào dùng để lấy dữ liệu từ bảng?",

            "options": [
                "SELECT",
                "INSERT",
                "UPDATE",
                "DELETE"
            ],

            "answer": 0
        },

        {
            "question":
                "Mệnh đề nào dùng để lọc dữ liệu?",

            "options": [
                "WHERE",
                "ORDER BY",
                "GROUP BY",
                "FROM"
            ],

            "answer": 0
        },

        {
            "question":
                "Query nào lấy tất cả sinh viên?",

            "options": [
                "SELECT * FROM students;",
                "GET * FROM students;",
                "SELECT students;",
                "SHOW students ALL;"
            ],

            "answer": 0
        },

        {
            "question":
                "Lệnh nào thêm một dòng dữ liệu?",

            "options": [
                "INSERT",
                "SELECT",
                "DROP",
                "ALTER"
            ],

            "answer": 0
        },

        {
            "question":
                "ORDER BY dùng để làm gì?",

            "options": [
                "Sắp xếp dữ liệu",
                "Xóa dữ liệu",
                "Nhóm bảng",
                "Tạo khóa"
            ],

            "answer": 0
        },

        {
            "question":
                "Query nào lấy sinh viên có điểm trên 8?",

            "options": [
                "SELECT * FROM students WHERE score > 8;",
                "SELECT students score > 8;",
                "GET students WHERE score > 8;",
                "SELECT * students IF score > 8;"
            ],

            "answer": 0
        },

        {
            "question":
                "PRIMARY KEY có đặc điểm nào?",

            "options": [
                "Xác định duy nhất mỗi bản ghi",
                "Có thể trùng tự do",
                "Chỉ dùng để sắp xếp",
                "Chỉ lưu văn bản"
            ],

            "answer": 0
        },

        {
            "question":
                "FOREIGN KEY dùng để làm gì?",

            "options": [
                "Liên kết các bảng",
                "Xóa database",
                "Mã hóa dữ liệu",
                "Sắp xếp bảng"
            ],

            "answer": 0
        },

        {
            "question":
                "JOIN được dùng chủ yếu để làm gì?",

            "options": [
                "Kết hợp dữ liệu từ nhiều bảng",
                "Xóa dữ liệu",
                "Đổi tên database",
                "Tạo mật khẩu"
            ],

            "answer": 0
        },

        {
            "question":
                "GROUP BY thường được dùng cùng hàm nào?",

            "options": [
                "COUNT()",
                "PRINT()",
                "INPUT()",
                "APPEND()"
            ],

            "answer": 0
        },

        {
            "question":
                "Lệnh nào sửa dữ liệu đã tồn tại?",

            "options": [
                "UPDATE",
                "SELECT",
                "CREATE",
                "DROP"
            ],

            "answer": 0
        },

        {
            "question":
                "Lệnh nào xóa một dòng dữ liệu?",

            "options": [
                "DELETE",
                "REMOVE",
                "CLEAR",
                "ERASE"
            ],

            "answer": 0
        },

        {
            "question":
                "COUNT(*) dùng để làm gì?",

            "options": [
                "Đếm số dòng",
                "Tính tổng",
                "Tìm giá trị lớn nhất",
                "Sắp xếp dữ liệu"
            ],

            "answer": 0
        },

        {
            "question":
                "Query nào sắp xếp điểm từ cao xuống thấp?",

            "options": [
                "ORDER BY score DESC",
                "ORDER BY score ASC",
                "GROUP BY score",
                "WHERE score DESC"
            ],

            "answer": 0
        },

        {
            "question":
                "INNER JOIN chỉ trả về dữ liệu nào?",

            "options": [
                "Các dòng khớp ở hai bảng",
                "Mọi dòng bảng trái",
                "Mọi dòng bảng phải",
                "Mọi dòng không khớp"
            ],

            "answer": 0
        }

    ],


    # =================================================
    # HTML
    # =================================================

    "html": [

        {
            "question":
                "HTML dùng chủ yếu để làm gì?",

            "options": [
                "Tạo cấu trúc trang web",
                "Quản lý database",
                "Chạy server",
                "Chỉnh sửa video"
            ],

            "answer": 0
        },

        {
            "question":
                "Thẻ nào tạo liên kết?",

            "options": [
                "<a>",
                "<p>",
                "<div>",
                "<span>"
            ],

            "answer": 0
        },

        {
            "question":
                "Thẻ nào hiển thị hình ảnh?",

            "options": [
                "<img>",
                "<image>",
                "<photo>",
                "<picture-text>"
            ],

            "answer": 0
        },

        {
            "question":
                "Thẻ tiêu đề lớn nhất là thẻ nào?",

            "options": [
                "<h1>",
                "<h6>",
                "<head>",
                "<title>"
            ],

            "answer": 0
        },

        {
            "question":
                "Thuộc tính nào chứa URL của liên kết?",

            "options": [
                "href",
                "src",
                "alt",
                "class"
            ],

            "answer": 0
        },

        {
            "question":
                "Thuộc tính nào chứa đường dẫn ảnh?",

            "options": [
                "src",
                "href",
                "link",
                "path"
            ],

            "answer": 0
        },

        {
            "question":
                "Thẻ nào tạo một đoạn văn?",

            "options": [
                "<p>",
                "<text>",
                "<paragraph>",
                "<line>"
            ],

            "answer": 0
        },

        {
            "question":
                "Thẻ nào tạo danh sách không thứ tự?",

            "options": [
                "<ul>",
                "<ol>",
                "<li>",
                "<list>"
            ],

            "answer": 0
        },

        {
            "question":
                "Thẻ nào thường dùng để nhập dữ liệu?",

            "options": [
                "<input>",
                "<output>",
                "<value>",
                "<enter>"
            ],

            "answer": 0
        },

        {
            "question":
                "Thẻ semantic nào thường chứa menu điều hướng?",

            "options": [
                "<nav>",
                "<menuitem>",
                "<route>",
                "<linkbox>"
            ],

            "answer": 0
        },

        {
            "question":
                "Thẻ nào dùng để tạo bảng?",

            "options": [
                "<table>",
                "<grid>",
                "<tab>",
                "<sheet>"
            ],

            "answer": 0
        },

        {
            "question":
                "Thẻ <tr> đại diện cho gì?",

            "options": [
                "Một hàng trong bảng",
                "Một cột",
                "Tiêu đề trang",
                "Một liên kết"
            ],

            "answer": 0
        },

        {
            "question":
                "Thuộc tính alt của ảnh dùng để làm gì?",

            "options": [
                "Mô tả ảnh khi ảnh không hiển thị",
                "Đổi kích thước ảnh",
                "Tạo hyperlink",
                "Đổi màu ảnh"
            ],

            "answer": 0
        },

        {
            "question":
                "Thẻ nào chứa nội dung chính hiển thị trên trang?",

            "options": [
                "<body>",
                "<head>",
                "<meta>",
                "<style>"
            ],

            "answer": 0
        },

        {
            "question":
                "Thẻ nào tạo biểu mẫu?",

            "options": [
                "<form>",
                "<input>",
                "<label>",
                "<fieldset>"
            ],

            "answer": 0
        }

    ],


    # =================================================
    # CSS
    # =================================================

    "css": [

        {
            "question":
                "CSS chủ yếu dùng để làm gì?",

            "options": [
                "Thiết kế giao diện",
                "Lưu database",
                "Tạo API",
                "Chạy Python"
            ],

            "answer": 0
        },

        {
            "question":
                "Thuộc tính nào đổi màu chữ?",

            "options": [
                "color",
                "font-color",
                "text-color",
                "foreground"
            ],

            "answer": 0
        },

        {
            "question":
                "Thuộc tính nào đổi màu nền?",

            "options": [
                "background-color",
                "font-color",
                "text-background",
                "color"
            ],

            "answer": 0
        },

        {
            "question":
                "display: flex dùng để làm gì?",

            "options": [
                "Tạo Flexbox layout",
                "Ẩn phần tử",
                "Đổi font",
                "Tạo database"
            ],

            "answer": 0
        },

        {
            "question":
                "justify-content tác động theo trục nào?",

            "options": [
                "Trục chính",
                "Trục phụ",
                "Trục Z",
                "Không có trục"
            ],

            "answer": 0
        },

        {
            "question":
                "Thuộc tính nào tạo khoảng cách bên trong?",

            "options": [
                "padding",
                "margin",
                "border",
                "gap"
            ],

            "answer": 0
        },

        {
            "question":
                "Thuộc tính nào tạo khoảng cách bên ngoài?",

            "options": [
                "margin",
                "padding",
                "font-size",
                "outline"
            ],

            "answer": 0
        },

        {
            "question":
                "Selector .card chọn phần tử dựa trên gì?",

            "options": [
                "class",
                "id",
                "tag",
                "name"
            ],

            "answer": 0
        },

        {
            "question":
                "Selector #header chọn phần tử dựa trên gì?",

            "options": [
                "id",
                "class",
                "tag",
                "type"
            ],

            "answer": 0
        },

        {
            "question":
                "Thuộc tính nào làm bo góc?",

            "options": [
                "border-radius",
                "corner-radius",
                "radius",
                "border-round"
            ],

            "answer": 0
        },

        {
            "question":
                "Media query thường dùng để làm gì?",

            "options": [
                "Responsive giao diện",
                "Kết nối database",
                "Tạo API",
                "Tạo biến JavaScript"
            ],

            "answer": 0
        },

        {
            "question":
                "position: fixed thường có tác dụng gì?",

            "options": [
                "Giữ phần tử cố định theo viewport",
                "Ẩn phần tử",
                "Xóa phần tử",
                "Căn giữa chữ"
            ],

            "answer": 0
        },

        {
            "question":
                "CSS Grid được bật bằng giá trị nào?",

            "options": [
                "display: grid",
                "position: grid",
                "layout: grid",
                "grid: display"
            ],

            "answer": 0
        },

        {
            "question":
                "Thuộc tính nào thay đổi kích thước chữ?",

            "options": [
                "font-size",
                "text-size",
                "size",
                "font-scale"
            ],

            "answer": 0
        },

        {
            "question":
                "width: 100% thường có nghĩa gì?",

            "options": [
                "Rộng bằng 100% vùng chứa",
                "Rộng 100px",
                "Cao 100%",
                "Ẩn chiều rộng"
            ],

            "answer": 0
        }

    ],


    # =================================================
    # JAVASCRIPT
    # =================================================

    "javascript": [

        {
            "question":
                "Từ khóa nào khai báo biến có thể thay đổi?",

            "options": [
                "let",
                "const",
                "fixed",
                "define"
            ],

            "answer": 0
        },

        {
            "question":
                "console.log() dùng để làm gì?",

            "options": [
                "In dữ liệu ra console",
                "Tạo database",
                "Đổi CSS",
                "Tạo server"
            ],

            "answer": 0
        },

        {
            "question":
                "Kết quả của 2 + 3 * 2 là gì?",

            "options": [
                "8",
                "10",
                "12",
                "7"
            ],

            "answer": 0
        },

        {
            "question":
                "Toán tử so sánh nghiêm ngặt là gì?",

            "options": [
                "===",
                "==",
                "=",
                "!="
            ],

            "answer": 0
        },

        {
            "question":
                "Phương thức nào thêm phần tử cuối array?",

            "options": [
                "push()",
                "append()",
                "add()",
                "insert()"
            ],

            "answer": 0
        },

        {
            "question":
                "document.getElementById() dùng để làm gì?",

            "options": [
                "Lấy phần tử theo id",
                "Tạo database",
                "Đổi URL",
                "Xóa JavaScript"
            ],

            "answer": 0
        },

        {
            "question":
                "Từ khóa nào khai báo hằng số?",

            "options": [
                "const",
                "let",
                "varied",
                "staticValue"
            ],

            "answer": 0
        },

        {
            "question":
                "Kiểu dữ liệu true và false là gì?",

            "options": [
                "Boolean",
                "String",
                "Number",
                "Array"
            ],

            "answer": 0
        },

        {
            "question":
                "Array.isArray([]) trả về gì?",

            "options": [
                "true",
                "false",
                "null",
                "undefined"
            ],

            "answer": 0
        },

        {
            "question":
                "Sự kiện nào thường xảy ra khi nhấn nút?",

            "options": [
                "click",
                "load",
                "resize",
                "scroll"
            ],

            "answer": 0
        },

        {
            "question":
                "Hàm nào chuyển chuỗi JSON thành object?",

            "options": [
                "JSON.parse()",
                "JSON.stringify()",
                "JSON.object()",
                "JSON.read()"
            ],

            "answer": 0
        },

        {
            "question":
                "JSON.stringify() có tác dụng gì?",

            "options": [
                "Chuyển object thành chuỗi JSON",
                "Chuyển chuỗi thành object",
                "Xóa object",
                "Tạo array"
            ],

            "answer": 0
        },

        {
            "question":
                "undefined thường có nghĩa gì?",

            "options": [
                "Giá trị chưa được xác định",
                "Số 0",
                "Chuỗi rỗng",
                "Luôn là false"
            ],

            "answer": 0
        },

        {
            "question":
                "Phương thức map() thường dùng để làm gì?",

            "options": [
                "Tạo array mới từ array hiện tại",
                "Xóa toàn bộ array",
                "Sắp xếp database",
                "Đổi HTML thành CSS"
            ],

            "answer": 0
        },

        {
            "question":
                "addEventListener() dùng để làm gì?",

            "options": [
                "Đăng ký xử lý sự kiện",
                "Tạo biến",
                "Tạo database",
                "Import CSS"
            ],

            "answer": 0
        }

    ],


    # =================================================
    # GIT
    # =================================================

    "git": [

        {
            "question":
                "Git dùng chủ yếu để làm gì?",

            "options": [
                "Quản lý phiên bản",
                "Thiết kế hình ảnh",
                "Tạo database",
                "Chỉnh video"
            ],

            "answer": 0
        },

        {
            "question":
                "Lệnh khởi tạo repository là gì?",

            "options": [
                "git init",
                "git start",
                "git create",
                "git new"
            ],

            "answer": 0
        },

        {
            "question":
                "Lệnh thêm file vào staging area là gì?",

            "options": [
                "git add",
                "git push",
                "git pull",
                "git clone"
            ],

            "answer": 0
        },

        {
            "question":
                "Lệnh tạo commit là gì?",

            "options": [
                "git commit",
                "git save",
                "git store",
                "git upload"
            ],

            "answer": 0
        },

        {
            "question":
                "git status dùng để làm gì?",

            "options": [
                "Xem trạng thái repository",
                "Xóa repository",
                "Đổi mật khẩu",
                "Tạo server"
            ],

            "answer": 0
        },

        {
            "question":
                "Lệnh sao chép repository từ remote là gì?",

            "options": [
                "git clone",
                "git copy",
                "git download",
                "git fetch-all"
            ],

            "answer": 0
        },

        {
            "question":
                "git push dùng để làm gì?",

            "options": [
                "Đẩy commit lên remote",
                "Tải repository về",
                "Xóa branch",
                "Xem status"
            ],

            "answer": 0
        },

        {
            "question":
                "git pull thường dùng để làm gì?",

            "options": [
                "Lấy thay đổi từ remote về",
                "Xóa remote",
                "Tạo commit",
                "Đổi tên repository"
            ],

            "answer": 0
        },

        {
            "question":
                "Lệnh tạo branch mới là gì?",

            "options": [
                "git branch feature",
                "git add feature",
                "git push feature",
                "git commit feature"
            ],

            "answer": 0
        },

        {
            "question":
                "git merge dùng để làm gì?",

            "options": [
                "Gộp các branch",
                "Xóa repository",
                "Tạo database",
                "Đổi URL"
            ],

            "answer": 0
        },

        {
            "question":
                "GitHub là gì?",

            "options": [
                "Nền tảng lưu trữ và cộng tác Git",
                "Ngôn ngữ lập trình",
                "Database",
                "Trình duyệt"
            ],

            "answer": 0
        },

        {
            "question":
                ".gitignore dùng để làm gì?",

            "options": [
                "Bỏ qua file không muốn Git theo dõi",
                "Xóa toàn bộ Git",
                "Tạo branch",
                "Đổi commit"
            ],

            "answer": 0
        },

        {
            "question":
                "Commit nên đại diện cho điều gì?",

            "options": [
                "Một thay đổi có ý nghĩa",
                "Toàn bộ ổ cứng",
                "Mật khẩu GitHub",
                "Một database mới"
            ],

            "answer": 0
        },

        {
            "question":
                "Remote thường có tên mặc định nào?",

            "options": [
                "origin",
                "main",
                "master",
                "remote1"
            ],

            "answer": 0
        },

        {
            "question":
                "Merge conflict xảy ra khi nào?",

            "options": [
                "Các thay đổi xung đột nhau",
                "Không có commit",
                "Internet nhanh",
                "Repository rỗng"
            ],

            "answer": 0
        }

    ]

}


# GitHub dùng chung ngân hàng với Git
QUIZ_BANK["github"] = QUIZ_BANK["git"]


# =====================================================
# SHUFFLE OPTIONS
# =====================================================

def shuffle_question(question):

    correct_answer = (
        question["options"][
            question["answer"]
        ]
    )

    options = (
        question["options"][:]
    )

    random.shuffle(
        options
    )

    new_answer = (
        options.index(
            correct_answer
        )
    )

    return {
        "question":
            question["question"],

        "options":
            options,

        "answer":
            new_answer
    }


# =====================================================
# GENERATE QUIZ
# =====================================================

def generate_skill_quiz(
    skill,
    profile=None
):

    skill_key = (
        skill
        .strip()
        .lower()
    )

    bank = QUIZ_BANK.get(
        skill_key
    )


    if not bank:

        print(
            "QUIZ BANK NOT FOUND:",
            skill
        )

        return None


    # Nếu sau này thêm >15 câu,
    # hệ thống sẽ random 15 câu.
    if len(bank) > 15:

        selected = random.sample(
            bank,
            15
        )

    else:

        selected = bank[:]


    # Trộn thứ tự câu
    random.shuffle(
        selected
    )


    # Trộn luôn đáp án mỗi câu
    final_questions = [

        shuffle_question(
            question
        )

        for question
        in selected

    ]


    print(
        "QUIZ READY:",
        skill,
        "-",
        len(final_questions),
        "questions"
    )


    return final_questions