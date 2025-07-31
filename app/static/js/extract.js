const handleLoadingSpinner = (state) => {
  const container = document.getElementById("result-loading-container");
  if (!container) return;

  const existingSpinner = container.querySelector(".spinner");

  if (state) {
    container.classList.remove("hidden");

    if (!existingSpinner) {
      const spinner = document.createElement("div");
      spinner.className = "spinner";
      container.appendChild(spinner);
    }
  } else {
    if (existingSpinner) {
      existingSpinner.remove();
    }

    container.classList.add("hidden"); // ✅ 전체 숨김
  }
};

const handleUpdateData = (data) => {
  try {
    const resultContainer = document.getElementById("result-container");

    resultContainer.classList.remove("hidden");

    const content = data.content;
    const summary = data.summary;
    const eval = data.evaluation;

    const contentElement = document.getElementById("result-content");
    const summaryElement = document.getElementById("result-summary");
    const evalElementContainer = document.getElementById("result-evaluation");

    if (contentElement) {
      contentElement.innerHTML = content;
    }

    if (summaryElement) {
      summaryElement.innerHTML = summary;
    }

    if (evalElementContainer) {
      const elementList = Object.entries(eval).map(([key, value]) => {
        return `<li>${key}: ${value}</li>`;
      }).join("");

      evalElementContainer.innerHTML = elementList;
    }
  } catch (e) {
    console.error(e);
  }
}

const handleForm = () => {
  const form = document.getElementById("extract-form");

  if (!form) return;

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    event.stopPropagation();

    const urlInput = form.querySelector("input[name='url']");
    const url = urlInput.value;

    if (!url) throw new Error("URL 값이 없습니다.");

    handleLoadingSpinner(true);

    try {
      const response = await fetch("/api/extract", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          url: url,
        }),
      });
      const result = await response.json();

      if (!result.success) throw new Error(result?.message || "요청 실패");

      handleUpdateData(result.data);
      handleLoadingSpinner(false);
    } catch (err) {
      console.error("요청 실패", err);

      alert("요청 중 오류가 발생했습니다.");
    } finally {
      handleLoadingSpinner(false);
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  handleForm();
});
