def orm_list(request):
    sections = []

    def show(title, sql, orm, queryset):
        # Получаем реальные результаты запроса
        data = list(queryset)

        sections.append({
            "title": title,
            "sql": sql,
            "orm": orm,
            "count": len(data),
            "data": pformat(data, width=100),
        })

    # 1. SELECT *
    show(
        "Все сотрудники",
        "SELECT * FROM employees;",
        "Employees.objects.all()",
        Employees.objects.all()
    )

    # 2. SELECT нужных столбцов
    show(
        "Имя и фамилия",
        "SELECT first_name, last_name FROM employees;",
        'Employees.objects.values("first_name", "last_name")',
        Employees.objects.values("first_name", "last_name")
    )

    # 3. DISTINCT
    show(
        "Уникальные имена и фамилии",
        "SELECT DISTINCT first_name, last_name FROM employees;",
        'Employees.objects.values("first_name", "last_name").distinct()',
        Employees.objects.values(
            "first_name", "last_name"
        ).distinct()
    )

    # 4. LIMIT и OFFSET
    show(
        "Первые 10 сотрудников",
        "SELECT * FROM employees LIMIT 10;",
        "Employees.objects.all()[:10]",
        Employees.objects.all()[:10].values()
    )

    show(
        "Следующие 5 сотрудников после первых пяти",
        "SELECT * FROM employees LIMIT 5 OFFSET 5;",
        "Employees.objects.all()[5:10]",
        Employees.objects.all()[5:10].values()
    )

    # 5. WHERE и IN
    show(
        "Страны региона 1",
        "SELECT * FROM countries WHERE region_id = 1;",
        "Countries.objects.filter(region_id=1)",
        Countries.objects.filter(region_id=1).values()
    )

    show(
        "Страны регионов 1 и 2",
        "SELECT * FROM countries WHERE region_id IN (1, 2);",
        "Countries.objects.filter(region_id__in=[1, 2])",
        Countries.objects.filter(
            region_id__in=[1, 2]
        ).values()
    )

    # 6. Поиск по тексту
    show(
        "Страны, начинающиеся на A",
        "SELECT * FROM countries WHERE country_name LIKE 'A%';",
        'Countries.objects.filter(country_name__startswith="A")',
        Countries.objects.filter(
            country_name__startswith="A"
        ).values()
    )

    show(
        "Страны, содержащие sa",
        "SELECT * FROM countries WHERE LOWER(country_name) LIKE '%sa%';",
        'Countries.objects.filter(country_name__icontains="sa")',
        Countries.objects.filter(
            country_name__icontains="sa"
        ).values()
    )

    show(
        "Страны, заканчивающиеся на a",
        "SELECT * FROM countries WHERE country_name LIKE '%a';",
        'Countries.objects.filter(country_name__iendswith="a")',
        Countries.objects.filter(
            country_name__iendswith="a"
        ).values()
    )

    # 7. Q: OR, AND и NOT
    show(
        "Страны на A или B",
        "SELECT * FROM countries WHERE country_name LIKE 'A%' OR country_name LIKE 'B%';",
        'Countries.objects.filter(Q(country_name__startswith="A") | Q(country_name__startswith="B"))',
        Countries.objects.filter(
            Q(country_name__startswith="A")
            | Q(country_name__startswith="B")
        ).values()
    )

    show(
        "Страны на A в регионе 2",
        "SELECT * FROM countries WHERE country_name LIKE 'A%' AND region_id = 2;",
        'Countries.objects.filter(country_name__startswith="A", region_id=2)',
        Countries.objects.filter(
            country_name__startswith="A",
            region_id=2
        ).values()
    )

    show(
        "Страны не на A и не из региона 1",
        "SELECT * FROM countries WHERE country_name NOT LIKE 'A%' AND region_id != 1;",
        'Countries.objects.filter(~Q(country_name__startswith="A"), ~Q(region_id=1))',
        Countries.objects.filter(
            ~Q(country_name__startswith="A"),
            ~Q(region_id=1)
        ).values()
    )

    # 8. Сравнение чисел
    show(
        "Зарплата больше 10000",
        "SELECT * FROM employees WHERE salary > 10000;",
        "Employees.objects.filter(salary__gt=10000)",
        Employees.objects.filter(
            salary__gt=10000
        ).values()
    )

    show(
        "Зарплата от 5000 до 10000",
        "SELECT * FROM employees WHERE salary BETWEEN 5000 AND 10000;",
        "Employees.objects.filter(salary__range=(5000, 10000))",
        Employees.objects.filter(
            salary__range=(5000, 10000)
        ).values()
    )

    # 9. exclude и NULL
    show(
        "Сотрудники не из должности 1",
        "SELECT * FROM employees WHERE job_id != 1;",
        "Employees.objects.exclude(job_id=1)",
        Employees.objects.exclude(job_id=1).values()
    )

    show(
        "Сотрудники без руководителя",
        "SELECT * FROM employees WHERE manager_id IS NULL;",
        "Employees.objects.filter(manager_id__isnull=True)",
        Employees.objects.filter(
            manager_id__isnull=True
        ).values()
    )

    show(
        "Сотрудники с руководителем",
        "SELECT * FROM employees WHERE manager_id IS NOT NULL;",
        "Employees.objects.filter(manager_id__isnull=False)",
        Employees.objects.filter(
            manager_id__isnull=False
        ).values()
    )

    # 10. Сортировка
    show(
        "Сотрудники по имени",
        "SELECT * FROM employees ORDER BY first_name ASC;",
        'Employees.objects.order_by("first_name")',
        Employees.objects.order_by("first_name").values()
    )

    show(
        "Сотрудники по зарплате от большей к меньшей",
        "SELECT * FROM employees ORDER BY salary DESC;",
        'Employees.objects.order_by("-salary")',
        Employees.objects.order_by("-salary").values()
    )

    # 11. Агрегаты
    show(
        "Количество сотрудников",
        "SELECT COUNT(*) FROM employees;",
        "Employees.objects.count()",
        [{"count": Employees.objects.count()}]
    )

    show(
        "Минимальная зарплата",
        "SELECT MIN(salary) FROM employees;",
        'Employees.objects.aggregate(Min("salary"))',
        [Employees.objects.aggregate(value=Min("salary"))]
    )

    show(
        "Максимальная зарплата",
        "SELECT MAX(salary) FROM employees;",
        'Employees.objects.aggregate(Max("salary"))',
        [Employees.objects.aggregate(value=Max("salary"))]
    )

    show(
        "Сумма зарплат",
        "SELECT SUM(salary) FROM employees;",
        'Employees.objects.aggregate(Sum("salary"))',
        [Employees.objects.aggregate(value=Sum("salary"))]
    )

    show(
        "Средняя зарплата",
        "SELECT AVG(salary) FROM employees;",
        'Employees.objects.aggregate(Avg("salary"))',
        [Employees.objects.aggregate(value=Avg("salary"))]
    )

    # 12. GROUP BY
    show(
        "Количество сотрудников по должностям",
        "SELECT job_id, COUNT(*) FROM employees GROUP BY job_id;",
        'Employees.objects.values("job_id").annotate(count=Count("*"))',
        Employees.objects.values("job_id").annotate(
            count=Count("*")
        ).order_by("job_id")
    )

    # 13. Остальные таблицы базы
    show(
        "Все должности",
        "SELECT * FROM jobs;",
        "Jobs.objects.all()",
        Jobs.objects.all().values()
    )

    show(
        "Все отделы",
        "SELECT * FROM departments;",
        "Departments.objects.all()",
        Departments.objects.all().values()
    )

    show(
        "Все местоположения",
        "SELECT * FROM locations;",
        "Locations.objects.all()",
        Locations.objects.all().values()
    )

    show(
        "Все зависимые члены семьи",
        "SELECT * FROM dependents;",
        "Dependents.objects.all()",
        Dependents.objects.all().values()
    )

    show(
        "Все регионы",
        "SELECT * FROM regions;",
        "Regions.objects.all()",
        Regions.objects.all().values()
    )

    # Формируем HTML через HttpResponse



# The public view delegates to the template-based explorer implementation.
from .studio import orm_list as _render_orm_studio


def orm_list(request):
    return _render_orm_studio(request)