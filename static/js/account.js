let isEmailAvailable = false;
let isAuth = false;

//회원가입 이메일 중복확인 및 인증번호 발송
window.sendEmail = function () {
    // 이메일 유효성 검사 및 인증번호 발송
    const emailInput = document.getElementById("email-input");
    const emailError = document.getElementById("email-error");
    const verificationSection = document.getElementById("verification-section");
    const emailValue = emailInput.value.trim();

    // 이메일 유효성 검사
    if (!emailValue || emailValue.includes("@") || emailValue.includes(" ")) {
        emailInput.classList.add("is-invalid"); // 빨간 테두리
        emailError.classList.remove("d-none"); // 오류 메시지 표시
    } else {
        emailInput.classList.remove("is-invalid"); // 빨간 테두리 제거
        emailError.classList.add("d-none"); // 오류 메시지 숨김

        // AJAX로 이메일 중복 확인 요청
        $.ajax({
        url: "/check-duplication",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ email: emailValue }),
        success: function (response) {
            if (response.success) {
            isEmailAvailable = true;

            // 인증번호 발송 로직
            alert(`인증번호가 ${emailValue}@kyonggi.ac.kr 로 발송되었습니다.`);

            // 인증번호 입력 섹션 표시
            verificationSection.classList.remove("d-none");

            $.ajax({
                url: "/send-email",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify({ email: emailValue }),
                success: function (response) {},
                error: function () {
                alert("중복 확인 중 문제가 발생했습니다.");
                isEmailAvailable = false;
                },
            });
            } else {
            alert("이미 가입된 이메일입니다.");
            }
        },
        error: function () {
            alert("중복 확인 중 문제가 발생했습니다.");
            isEmailAvailable = false;
        },
        });
    }
};

// 인증번호 확인
window.checkAuth = function() {
    const verificationCode = document.getElementById('verification-code').value.trim();
    const verificationError = document.getElementById('verification-error');
    const verificationCheckIcon = document.getElementById('verification-check-icon');
    const signupBtn = document.getElementById('signup-btn');
    email = $('#email-input').val();


    $.ajax({
        url: '/check-auth',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ email: email, authCode: verificationCode }),
        success: function (response) {
            if(response.success) {
                alert("인증번호가 확인되었습니다.")
                verificationError.classList.add('d-none'); // 오류 메시지 숨김
                verificationCheckIcon.classList.remove('d-none'); // 체크 아이콘 표시
                isAuth = true;
                signupBtn.disabled = false;
                $('#email-input').prop("disabled", true);
                $('#send-code-btn').prop("disabled", true);
                $('#verification-code').prop("disabled", true);
                $('#verify-code-btn').prop("disabled", true);
            } else {
                verificationError.classList.remove('d-none'); // 오류 메시지 표시
                verificationCheckIcon.classList.add('d-none'); // 체크 아이콘 숨김
                isAuth = false;
                signupBtn.disabled = true;
            }
        },
        error: function () {
            alert("인증과정에서 오류가 발생하였습니다.")
        }
    });
}

//회원가입
window.checkSignup = function () {
    //유효성 검사
    const email = $("#email-input").val();
    const PW = $("#password").val();
    if (!email) {
        alert("이메일을 입력해주세요.");
        return;
    } else if (!isEmailAvailable || !isAuth) {
        alert("이메일 인증을 완료해주세요.");
        alert(isEmailAvailable);
        alert(isAuth);
        return;
    } else if (!PW) {
        alert("패스워드를 입력해주세요.");
        return;
    }

    //회원가입 프로세스
    $.ajax({
        url: "/signup-process",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ email: email, PW: PW }),
        success: function (response) {
        if (response.success) {
            alert("성공적으로 가입되었습니다!");
            window.location.href = "/";
        } else {
            alert("회원가입에 실패했습니다.");
            return false;
        }
        },
    });
};

//로그인
window.login = function () {
    const email = $("#username").val();
    const PW = $("#password").val();
    var emailTest =
        /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$/i;

    //유효성 검사
    if (!email) {
        alert("이메일을 입력해주세요.");
        return;
    } else if (!emailTest.test(email)) {
        alert("아이디를 이메일 형식으로 입력해주세요.");
        return;
    } else if (!PW) {
        alert("패스워드를 입력해주세요.");
        return;
    }

    //로그인 프로세스
    $.ajax({
        url: "/login-process",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ email: email, PW: PW }),
        success: function (response) {
        if (response.success) {
            alert("성공적으로 로그인 되었습니다!");
            window.location.href = "/";
        } else {
            alert("로그인에 실패했습니다.");
            return false;
        }
        },
        error: function () {
        alert("로그인 도중 오류가 발생했습니다.");
        },
    });
};

//로그아웃
window.logout = function () {
    //회원가입 프로세스
    $.ajax({
        url: "/logout",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({}),
        success: function (response) {
        if (response.success) {
            alert("성공적으로 로그아웃 되었습니다!");
            window.location.href = "/";
        } else {
            alert("로그아웃에 실패했습니다.");
            return false;
        }
        },
    });
};