# 🚀 Настройка GitHub Actions для Docker

Инструкция по активации автоматической сборки и публикации Docker образов.

---

## ✅ Что уже сделано

1. ✅ Создан workflow файл `.github/workflows/docker-publish.yml`
2. ✅ Настроена автоматическая сборка при push в `main` или `develop`
3. ✅ Настроена публикация в GitHub Container Registry (ghcr.io)

---

## 🔧 Активация GitHub Actions

### Шаг 1: Проверьте настройки репозитория

1. Перейдите на GitHub: https://github.com/bocharov62-bit/AI_Agent_Target
2. Откройте **Settings** → **Actions** → **General**
3. Убедитесь, что **Actions** включены
4. В разделе **Workflow permissions** выберите:
   - ✅ **Read and write permissions**
   - ✅ **Allow GitHub Actions to create and approve pull requests**

### Шаг 2: Merge feature-ветки в main

**Вариант A: Через Pull Request (рекомендуется)**

1. Перейдите по ссылке:
   ```
   https://github.com/bocharov62-bit/AI_Agent_Target/pull/new/feature/web-interface
   ```

2. Создайте Pull Request из `feature/web-interface` в `main`

3. Нажмите **Create Pull Request**

4. После проверки нажмите **Merge pull request**

**Вариант B: Через командную строку**

```bash
git checkout main
git merge feature/web-interface
git push origin main
```

### Шаг 3: Проверьте запуск workflow

1. Перейдите в **Actions** на GitHub
2. Вы увидите запущенный workflow "Build and Publish Docker Image"
3. Дождитесь завершения (обычно 3-5 минут)

---

## 📦 Использование образов

После успешной сборки образы будут доступны по адресам:

### CLI образ:
```
ghcr.io/bocharov62-bit/ai_agent_target:latest
ghcr.io/bocharov62-bit/ai_agent_target:main
```

### Веб-интерфейс (после добавления в workflow):
```
ghcr.io/bocharov62-bit/ai_agent_target:web-latest
```

---

## 🔐 Авторизация для pull образов

### Публичные образы (рекомендуется)

1. Перейдите в **Settings** → **Actions** → **General**
2. В разделе **Workflow permissions** включите:
   - ✅ **Read and write permissions**
3. В разделе **Packages** включите:
   - ✅ **Public packages** (если хотите публичные образы)

### Приватные образы

Для использования приватных образов нужна авторизация:

```bash
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
```

Где `GITHUB_TOKEN` - Personal Access Token с правами `read:packages`.

---

## 📊 Просмотр образов

После успешной сборки:

1. Перейдите на: https://github.com/bocharov62-bit/AI_Agent_Target/pkgs/container/ai_agent_target
2. Вы увидите все опубликованные версии

---

## 🐳 Использование образов

### CLI режим:
```bash
docker run --rm --env-file .env \
  ghcr.io/bocharov62-bit/ai_agent_target:latest \
  https://example.com --role all
```

### Веб-интерфейс:
```bash
docker run -d -p 8000:8000 --env-file .env \
  ghcr.io/bocharov62-bit/ai_agent_target:web-latest
```

---

## 🔄 Обновление workflow для веб-образа

Текущий workflow собирает только CLI образ. Для добавления веб-образа:

1. Откройте `.github/workflows/docker-publish.yml`
2. Добавьте второй job для сборки веб-образа (используя `Dockerfile.web`)

Или используйте matrix strategy для сборки обоих образов одновременно.

---

## ❓ Решение проблем

### Workflow не запускается

**Решение:**
- Проверьте, что Actions включены в настройках репозитория
- Убедитесь, что файл `.github/workflows/docker-publish.yml` существует

### Ошибка: "Permission denied"

**Решение:**
- Проверьте настройки Workflow permissions
- Убедитесь, что выбрано "Read and write permissions"

### Образ не публикуется

**Решение:**
- Проверьте логи workflow в разделе Actions
- Убедитесь, что используется правильный `GITHUB_TOKEN`

---

## 📚 Дополнительные ресурсы

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Docker Guide](DOCKER_GUIDE.md)

---

*Последнее обновление: 02.01.2026*

