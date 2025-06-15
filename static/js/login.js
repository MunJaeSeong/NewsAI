// static/js/login.js
// 비밀번호 표시/숨기기 토글

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
    document.getElementById('loginForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        try {
            const response = await fetch('/users/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            const result = await response.json();
            if (result.id || result.username) {
                window.location.href = '/';
            } else {
                alert('로그인 실패: ' + (result.detail || '아이디 또는 비밀번호를 확인해주세요.'));
            }
        } catch (error) {
            console.error('Error:', error);
            alert('로그인 처리 중 오류가 발생했습니다.');
        }
    });
});
