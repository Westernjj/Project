from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone

from .forms import (
    UserRegisterForm,
    UserUpdateForm,
    ProfileUpdateForm,
    ActivationCodeForm,
)
from .models import VerificationCode

# Отримуємо поточну модель користувача (може бути кастомна)
User = get_user_model()

# Максимальна кількість спроб введення одного коду активації
MAX_ATTEMPTS = 5

# Мінімальний інтервал (у секундах) між повторними відправками коду
RESEND_COOLDOWN_SEC = 60

# Допоміжна функція відправки коду активації на e-mail
def _send_activation_code(user, ttl=15):
    # Створюємо (issue) новий код з терміном дії ttl хвилин
    vc = VerificationCode.issue(user, ttl_minutes=ttl)

    # Рендеримо текст листа з шаблону, передаючи користувача, код і час життя
    body = render_to_string(
        "accounts/activation_code_email.txt",
        {"user": user, "code": vc.code, "ttl": ttl},
    )

    # Відправляємо email користувачу
    send_mail(
        subject="Код активації",
        message=body,
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
        recipient_list=[user.email],
    )
    return vc

# Реєстрація нового користувача
def register(request):
    """
    Відображає форму реєстрації та обробляє створення нового користувача.
    Користувач створюється неактивним, йому надсилається код активації.
    """
    if request.method == "POST":
        # Створюємо форму з даними, які надійшли від користувача
        form = UserRegisterForm(request.POST)

        # Перевіряємо, чи форма валідна
        if form.is_valid():
            # Створюємо об'єкт User, але тимчасово не зберігаємо в БД
            user = form.save(commit=False)
            # Робимо користувача неактивним до підтвердження коду
            user.is_active = False
            # Тепер зберігаємо в БД
            user.save()

            # Створюємо та надсилаємо код активації на e-mail
            _send_activation_code(user)

            # Зберігаємо id користувача в сесії, щоб знати, кого підтверджуємо
            request.session["pending_uid"] = user.pk

            # Повідомлення користувачу
            messages.success(
                request, "Ми надіслали код активації на вашу електронну пошту."
            )
            # Перенаправлення на сторінку введення коду
            return redirect("accounts:verify")

        # Якщо форма невалідна, знову відображаємо шаблон з помилками
        return render(request, "accounts/register.html", {"form": form})

    # Якщо GET-запит, показуємо порожню форму реєстрації
    form = UserRegisterForm()
    return render(request, "accounts/register.html", {"form": form})

# Перевірка коду активації
def verify(request):
    """
    Сторінка введення коду активації.
    Перевіряє:
      - чи є користувач у сесії (pending_uid),
      - чи існує код,
      - чи не перевищено кількість спроб,
      - чи не прострочений код,
      - чи відповідає введене значення збереженому коду.
    У разі успіху активує акаунт та автоматично логінить користувача.
    """
    # Отримуємо id користувача з сесії
    uid = request.session.get("pending_uid")
    if not uid:
        # Якщо ніхто не реєструється/не верифікується, просимо спочатку зареєструватися
        messages.info(request, "Спочатку зареєструйтеся.")
        return redirect("accounts:register")

    # Отримуємо користувача або повертаємо 404, якщо його не існує
    user = get_object_or_404(User, pk=uid)

    # Створюємо форму для коду (або з POST-даними, або порожню)
    form = ActivationCodeForm(request.POST or None)

    # Обробка POST-запиту з формою
    if request.method == "POST" and form.is_valid():
        # Очищене значення коду з форми
        code = form.cleaned_data["code"].strip()

        # Отримуємо найсвіжіший невикористаний код активації для цього користувача
        vc = (
            VerificationCode.objects.filter(
                user=user, purpose="activation", is_used=False
            )
            .order_by("-created_at")
            .first()
        )
        # Якщо коду не знайдено, пропонуємо запитати новий
        if not vc:
            messages.error(request, "Код не знайдено. Запитайте новий.")
            return redirect("accounts:resend")

        # Якщо кількість спроб для цього коду вже вичерпано
        if vc.attempts >= MAX_ATTEMPTS:
            messages.error(
                request, "Перевищено кількість спроб. Новий код надіслано."
            )
            # Надсилаємо новий код і повертаємо на сторінку verify
            _send_activation_code(user)
            return redirect("accounts:verify")

        # ВИПАДОК ВАЛІДНОГО КОДУ 
        if vc.is_valid(code):
            # Позначаємо код як використаний
            vc.is_used = True
            vc.save(update_fields=["is_used"])

            # Активуємо користувача
            user.is_active = True
            user.save(update_fields=["is_active"])

            # Видаляємо з сесії запис про "очікуючого" користувача
            request.session.pop("pending_uid", None)
            user.backend = "django.contrib.auth.backends.ModelBackend"
            # Логінимо користувача в сесію
            login(request, user)

            messages.success(request, f"Акаунт активовано! Вітаємо, {user.username}.")
            # Перенаправляємо на головну сторінку з товарами
            return redirect("products")

        # ВИПАДОК НЕВІРНОГО/ПРОСТРОЧЕНОГО КОДУ
        # Збільшуємо кількість спроб
        vc.attempts += 1
        vc.save(update_fields=["attempts"])

        # Перевіряємо, чи вже вийшов строк дії коду
        if timezone.now() > vc.expires_at:
            messages.error(request, "Код прострочений. Запитайте новий.")
        else:
            messages.error(request, "Невірний код. Спробуйте знову.")

        # Повертаємо на сторінку вводу коду
        return redirect("accounts:verify")

    # Якщо GET-запит або форма невалідна, показуємо шаблон з формою та email'ом
    return render(request, "accounts/verify.html", {"form": form, "email": user.email})

# Повторна відправка коду активації (resend) з rate-limit-ом

def resend(request):
    # Знову перевіряємо, чи є користувач в процесі підтвердження
    uid = request.session.get("pending_uid")
    if not uid:
        messages.info(request, "Спочатку зареєструйтеся.")
        return redirect("accounts:register")

    now = timezone.now()
    last_ts = request.session.get("last_resend_at")

    # Якщо вже є час останньої відправки в сесії
    if last_ts:
        # Перетворюємо рядок ISO назад у datetime
        last = timezone.datetime.fromisoformat(last_ts)
        # Перевіряємо, чи пройшла достатня кількість секунд
        if now - last < timedelta(seconds=RESEND_COOLDOWN_SEC):
            # Обчислюємо, скільки ще чекати
            wait = RESEND_COOLDOWN_SEC - int((now - last).total_seconds())
            messages.warning(
                request, f"Зачекайте ще {wait} с перед повторною відправкою."
            )
            return redirect("accounts:verify")

    # Якщо ліміт нас не зупинив, отримаємо користувача та надішлемо новий код
    user = get_object_or_404(User, pk=uid)
    _send_activation_code(user)

    # Оновлюємо час останньої відправки в сесії
    request.session["last_resend_at"] = now.isoformat()

    messages.success(request, "Новий код надіслано.")
    return redirect("accounts:verify")

# Профіль: перегляд
@login_required
def profile(request):
    """
    Проста сторінка перегляду профілю користувача.
    У шаблоні можна використовувати request.user та request.user.profile.
    """
    return render(request, "accounts/profile.html")

# Профіль: редагування
@login_required
def profile_edit(request):
    """
    Сторінка редагування профілю користувача.
    Оновлює одночасно:
      - стандартну модель User (username, email),
      - пов'язаний Profile (avatar, phone, bio).
    """
    if request.method == "POST":
        # Форма оновлення даних користувача
        u_form = UserUpdateForm(request.POST, instance=request.user)

        # Форма оновлення профілю (ВАЖЛИВО: request.FILES для аватару)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        # Перевіряємо обидві форми
        if u_form.is_valid() and p_form.is_valid():
            # Зберігаємо дані користувача
            u_form.save()
            # Зберігаємо дані профілю (включно з файлом аватару)
            p_form.save()

            messages.success(request, "Профіль оновлено.")
            # Після успішного збереження переходимо на сторінку перегляду профілю
            return redirect("accounts:profile")

        # Якщо форми не пройшли валідацію, повторно відображаємо сторінку з помилками
        return render(
            request, "accounts/profile_edit.html", {"u_form": u_form, "p_form": p_form}
        )

    # Якщо GET-запит: заповнюємо форми поточними даними користувача та його профілю
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)

    # Відображаємо шаблон редагування профілю
    return render(
        request, "accounts/profile_edit.html", {"u_form": u_form, "p_form": p_form}
    )
