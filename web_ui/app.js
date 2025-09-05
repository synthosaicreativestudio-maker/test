// Внешний скрипт для страницы авторизации с поддержкой Telegram Mini App
// Экспортируем функцию инициализации, чтобы можно было переиспользовать в других страницах

// Инициализация Telegram Web App
let tg = window.Telegram?.WebApp;
if (tg) {
  tg.ready();
  tg.expand();
  // Устанавливаем цвета темы
  document.body.style.backgroundColor = tg.backgroundColor;
  // Показываем главную кнопку
  tg.MainButton.setText('Авторизоваться');
  tg.MainButton.show();
}

function initAuthForm({formId = 'authForm', resultId = 'result', codeId = 'code', phoneId = 'phone'} = {}){
  const form = document.getElementById(formId);
  const codeInput = document.getElementById(codeId);
  const phoneInput = document.getElementById(phoneId);
  const result = document.getElementById(resultId);
  const submitBtn = document.getElementById('submitBtn');

  phoneInput.addEventListener('focus', ()=>{
    if(!phoneInput.value) phoneInput.value = '8';
  });

  // Валидация в реальном времени
  function validateForm() {
    const code = (codeInput.value || '').trim();
    const phone = (phoneInput.value || '').trim();
    
    const isValid = /^[0-9]+$/.test(code) && 
                   phone.length === 11 && 
                   phone.startsWith('8') && 
                   /^[0-9]+$/.test(phone);
    
    if (tg && tg.MainButton) {
      if (isValid) {
        tg.MainButton.enable();
        tg.MainButton.color = tg.themeParams.button_color || '#0088cc';
      } else {
        tg.MainButton.disable();
        tg.MainButton.color = '#999999';
      }
    }
    
    return isValid;
  }

  // Слушатели для валидации
  codeInput.addEventListener('input', validateForm);
  phoneInput.addEventListener('input', validateForm);

  async function performAuth() {
    result.textContent = '';

    const code = (codeInput.value || '').trim();
    let phone = (phoneInput.value || '').trim();

    if(!/^[0-9]+$/.test(code)){
      result.textContent = 'Код должен содержать только цифры.'; 
      result.className='footer error'; 
      return;
    }

    phone = phone.replace(/\D/g,'');
    if(phone.length === 10) phone = '8'+phone;
    if(!(phone.length === 11 && phone.startsWith('8'))){
      result.textContent = 'Неверный формат телефона. Ожидается 11 цифр, начинается с 8.'; 
      result.className='footer error'; 
      return;
    }

    // Показываем прогресс
    if (tg && tg.MainButton) {
      tg.MainButton.showProgress();
    }
    
    try {
      // Отправляем данные через Telegram Web App API
      if (tg) {
        const authData = {
          code: code,
          phone: phone,
          user_id: tg.initDataUnsafe?.user?.id,
          first_name: tg.initDataUnsafe?.user?.first_name,
          username: tg.initDataUnsafe?.user?.username
        };
        
        // Отправляем данные боту
        tg.sendData(JSON.stringify(authData));
        
        result.textContent = '✅ Данные отправлены! Ожидайте подтверждения авторизации.';
        result.className = 'footer success';
        
        // Закрываем Mini App через 2 секунды
        setTimeout(() => {
          tg.close();
        }, 2000);
        
      } else {
        // Fallback для обычного веб-браузера
        const resp = await fetch('/authorize', {
          method: 'POST', 
          credentials: 'same-origin', 
          headers: {'Content-Type':'application/json'},
          body: JSON.stringify({code, phone})
        });

        if(resp.ok){
          const data = await resp.json().catch(()=>null);
          result.textContent = (data && data.message) ? data.message : 'Запрос отправлен. Ожидайте подтверждения.';
          result.className='footer success';
        } else {
          const data = await resp.json().catch(()=>null);
          result.textContent = (data && data.error) ? data.error : 'Ошибка авторизации.';
          result.className='footer error';
        }
      }
    } catch(err) {
      result.textContent = 'Локальная проверка пройдена. Для реальной авторизации настройте endpoint /authorize.'; 
      result.className='footer small';
    } finally {
      // Скрываем прогресс
      if (tg && tg.MainButton) {
        tg.MainButton.hideProgress();
      }
    }
  }

  // Обработчик отправки формы
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    await performAuth();
  });

  // Обработчик главной кнопки Telegram
  if (tg && tg.MainButton) {
    tg.MainButton.onClick(async () => {
      await performAuth();
    });
  }

  // Начальная валидация
  validateForm();
}

// Auto-init если страница загружена
document.addEventListener('DOMContentLoaded', ()=>{
  if(document.getElementById('authForm')){
    initAuthForm();
  }
});

// экспорт (UMD-lite)
window.app = window.app || {};
window.app.initAuthForm = initAuthForm;
