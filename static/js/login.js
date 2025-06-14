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
        const formData = new FormData(this);
        try {
            const response = await fetch('/users/login', {
                method: 'POST',
                body: formData
            });
            const result = await response.json();
            if (result.success) {
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
