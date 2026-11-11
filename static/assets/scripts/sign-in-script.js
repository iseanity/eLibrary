const form = document.getElementById('autorForm');
        const passwordInput = document.getElementById('password');

        form.addEventListener('submit', function (event) {
            event.preventDefault();

            const passwordValue = passwordInput.value;

            if (passwordValue.length < 8) {
                alert('Пароль должен содержать минимум 8 символов');
                return;
            }

            alert('Вход успешен!');
            window.location.href = 'index.html';
        });