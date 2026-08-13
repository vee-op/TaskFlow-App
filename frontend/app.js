const API_URL = "/api";


async function loadTasks(filter = "all") {

    const response = await fetch(`${API_URL}/tasks`);

    const tasks = await response.json();

    const container = document.getElementById("tasks");

    container.innerHTML = "";

    let filteredTasks = tasks;

    if (filter === "active") {
        filteredTasks = tasks.filter(task => !task.completed);
    }

    if (filter === "completed") {
        filteredTasks = tasks.filter(task => task.completed);
    }

    filteredTasks.forEach(task => {

        const taskElement = document.createElement("div");

        taskElement.className = "task";

        taskElement.innerHTML = `
            <div>
                <h3 class="${task.completed ? "completed" : ""}">
                    ${task.title}
                </h3>

                <p>
                    ${task.description || ""}
                </p>
            </div>

            <div class="actions">

                <button onclick="toggleTask(
                    ${task.id},
                    ${!task.completed}
                )">
                    ${task.completed ? "Undo" : "Complete"}
                </button>

                <button
                    class="delete"
                    onclick="deleteTask(${task.id})"
                >
                    Delete
                </button>

            </div>
        `;

        container.appendChild(taskElement);
    });
}


document
    .getElementById("taskForm")
    .addEventListener("submit", async function(event) {

        event.preventDefault();

        const title =
            document.getElementById("title").value;

        const description =
            document.getElementById("description").value;

        await fetch(`${API_URL}/tasks`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                title,
                description
            })
        });

        document.getElementById("taskForm").reset();

        loadTasks();
    });


async function toggleTask(id, completed) {

    await fetch(`${API_URL}/tasks/${id}`, {

        method: "PUT",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            completed
        })
    });

    loadTasks();
}


async function deleteTask(id) {

    await fetch(`${API_URL}/tasks/${id}`, {
        method: "DELETE"
    });

    loadTasks();
}


loadTasks();