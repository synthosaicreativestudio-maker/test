// Внешний скрипт для страницы авторизации
// Экспортируем функцию инициализации, чтобы можно было переиспользовать в других страницах

function initAuthForm({formId = 'authForm', resultId = 'result', codeId = 'code', phoneId = 'phone'} = {}){
  const form = document.getElementById(formId);
  const codeInput = document.getElementById(codeId);
  const phoneInput = document.getElementById(phoneId);
  const result = document.getElementById(resultId);

  phoneInput.addEventListener('focus', ()=>{
    if(!phoneInput.value) phoneInput.value = '8';
  });

  form.addEventListener('submit', async (e)=>{
    e.preventDefault();
    result.textContent = '';

    const code = (codeInput.value || '').trim();
    let phone = (phoneInput.value || '').trim();

    if(!/^[0-9]+$/.test(code)){
      result.textContent = 'Код должен содержать только цифры.'; result.className='footer error'; return;
    }

    phone = phone.replace(/\D/g,'');
    if(phone.length === 10) phone = '8'+phone;
    if(!(phone.length === 11 && phone.startsWith('8'))){
      result.textContent = 'Неверный формат телефона. Ожидается 11 цифр, начинается с 8.'; result.className='footer error'; return;
    }

    try{
      const resp = await fetch('/authorize', {
        method: 'POST', credentials: 'same-origin', headers: {'Content-Type':'application/json'},
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
    }catch(err){
      result.textContent = 'Локальная проверка пройдена. Для реальной авторизации настройте endpoint /authorize.'; result.className='footer small';
    }
  });
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
