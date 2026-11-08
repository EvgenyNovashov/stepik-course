const API = "/api/tasks";

const form = document.getElementById("task-form");
const titleInput = document.getElementById("task-title");
const listEl = document.getElementById("task-list");
const errorEl = document.getElementById("error");

function showError(message) {
  errorEl.textContent = message;
  errorEl.hidden = !message;
}

function formatDate(iso) {
  try {
    return new Date(iso).toLocaleString("ru-RU");
  } catch {
    return iso;
  }
}

function renderTasks(tasks) {
  listEl.innerHTML = "";
  if (!tasks.length) {
    const li = document.createElement("li");
    li.className = "empty";
    li.textContent = "Задач пока нет — добавьте первую.";
    listEl.appendChild(li);
    return;
  }

  for (const task of tasks) {
    const li = document.createElement("li");
    li.className = "task-item" + (task.completed ? " completed" : "");

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = task.completed;
    checkbox.setAttribute("aria-label", "Отметить выполненной");
    checkbox.addEventListener("change", () => toggleTask(task.id, checkbox.checked));

    const body = document.createElement("div");
    body.className = "task-body";

    const title = document.createElement("p");
    title.className = "task-title";
    title.textContent = task.title;

    const meta = document.createElement("p");
    meta.className = "task-meta";
    meta.textContent = `Создано: ${formatDate(task.created_at)}`;

    body.append(title, meta);
    li.append(checkbox, body);
    listEl.appendChild(li);
  }
}

async function loadTasks() {
  showError("");
  try {
    const res = await fetch(API);
    if (!res.ok) throw new Error(`Ошибка загрузки (${res.status})`);
    const tasks = await res.json();
    renderTasks(tasks);
  } catch (err) {
    showError(err.message || "Не удалось загрузить задачи");
  }
}

async function createTask(title) {
  const res = await fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });
  if (res.status === 422) {
    throw new Error("Название не может быть пустым");
  }
  if (!res.ok) throw new Error(`Не удалось создать задачу (${res.status})`);
  return res.json();
}

async function toggleTask(id, completed) {
  showError("");
  try {
    const res = await fetch(`${API}/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ completed }),
    });
    if (!res.ok) throw new Error(`Ошибка обновления (${res.status})`);
    await loadTasks();
  } catch (err) {
    showError(err.message || "Не удалось обновить задачу");
    await loadTasks();
  }
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const title = titleInput.value.trim();
  if (!title) {
    showError("Введите название задачи");
    return;
  }
  showError("");
  try {
    await createTask(title);
    titleInput.value = "";
    await loadTasks();
  } catch (err) {
    showError(err.message || "Не удалось создать задачу");
  }
});

loadTasks();
