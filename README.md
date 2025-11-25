# 🏎️ Formula 1 — Server-Side Programming Project  
### ✔ Django + DRF + Repository Pattern + Templates + External API Integration

---

## 📘 Опис проєкту
Цей навчальний проєкт виконано в межах дисципліни **«Програмування на стороні сервера»**.  
Проєкт реалізує:

- роботу з базою даних Formula 1 (Teams, Drivers, Circuits, Cars тощо)
- патерн **Repository**
- повноцінний **REST API** через Django REST Framework
- **HTML-шаблони Django** (list/detail/form/delete)
- інтеграцію зі **стороннім REST API колеги** через бібліотеку `requests` та BasicAuth
- фронтенд-сторінки для роботи з даними (власними та чужими)

---

# 🧩 Частина 1 — Repository Pattern

Проєкт використовує власні репозиторії (`F1Repository` + вкладені класи), які інкапсулюють логіку доступу до бази даних.

### Реалізовано методи:
- `list_all()` — отримання всіх записів  
- `get_by_id()` — отримання одного об’єкта  
- `add()` — створення нового запису  
- `update()` — редагування  
- `delete_by_id()` — видалення  

Repository використовується у всіх **ViewSet-ах DRF**.

---

# 🌐 Частина 2 — REST API (Django REST Framework)

Для кожної сутності бази даних реалізовано CRUD через DRF:

| Endpoint | Опис |
|---------|------|
| `/api/teams/` | CRUD команд |
| `/api/drivers/` | CRUD гонщиків |
| `/api/circuits/` | CRUD трас |
| `/api/principals/` | CRUD керівників |
| `/api/cars/` | CRUD машин |
| `/api/results/` | CRUD результатів |
| `/api/report/` | агрегований звіт |

### Звіт:
`GET /api/report/`  
Повертає кількість пілотів у кожній команді (GROUP BY + COUNT).

### API використовує:
- ViewSet-и  
- Routers  
- Serializers  
- DjangoFilterBackend  

---

# 🎨 Частина 3 — Робота з шаблонами (Frontend)

За вимогою лабораторної створено повний CRUD у шаблонах для сутності **Principals**.

### ✔ Реалізовані сторінки:
- `/frontend/principals/` — список керівників  
- `/frontend/principals/<id>/` — детальна сторінка  
- `/frontend/principals/add/` — створення  
- `/frontend/principals/<id>/edit/` — редагування  
- `/frontend/principals/<id>/delete/` — підтвердження видалення  

### ✔ Використано:
- Django ModelForm (`PrincipalForm`)
- HTML forms + CSRF захист
- Template loops
- Передача ForeignKey (principal → team)
- Окрема сторінка підтвердження видалення

---

# 🔗 Частина 4 — Інтеграція зі стороннім REST API

Було розгорнуто проєкт колеги (на порту **8001**), створено користувача, додано дані через Django Admin.

### 📌 Розроблено `NetworkHelper.py`
```python
get_list()
get_item()
create_item()
update_item()
delete_item()
