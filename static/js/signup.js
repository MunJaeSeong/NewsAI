// static/js/signup.js
// 비밀번호 표시/숨기기 토글 및 회원가입 폼 처리

document.addEventListener('DOMContentLoaded', function() {
    const toggleButtons = document.querySelectorAll('.btn-password-toggle');
    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const passwordInput = document.getElementById(targetId);
            if (passwordInput) {
                if (passwordInput.type === 'password') {
                    passwordInput.type = 'text';
                    this.classList.add('show-password');
                } else {
                    passwordInput.type = 'password';
                    this.classList.remove('show-password');
                }
            }
        });
    });

    // 폼 제출 처리
    document.getElementById('signupForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        // 비밀번호 확인
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const passwordConfirm = document.getElementById('password_confirm').value;
        const email = document.getElementById('email').value;
        const name = document.getElementById('name').value;
        if (password !== passwordConfirm) {
            alert('비밀번호가 일치하지 않습니다.');
            return;
        }
        try {
            const response = await fetch('/users/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password, email, name })
            });
            const result = await response.json();
            if (result.success) {
                alert(result.message);
                window.location.href = '/login';
            } else {
                alert('회원가입에 실패했습니다: ' + (result.detail || '알 수 없는 오류'));
            }
        } catch (error) {
            console.error('Error:', error);
            alert('회원가입 처리 중 오류가 발생했습니다.');
        }
    });
});
