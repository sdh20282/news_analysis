const handleLoading = (state) => {
  try {
    const loadingSpinner = document.getElementById("loading-spinner");
    const resultContainer = document.getElementById("result-container");

    if (!loadingSpinner || !resultContainer) return;

    if (state) {
      loadingSpinner.classList.remove("hidden");
      resultContainer.classList.add("hidden");
    } else {
      loadingSpinner.classList.add("hidden");
      resultContainer.classList.remove("hidden");
    }
  } catch (e) {
    console.error("Loading spinner error:", e);
  }
};

const handleUpdateData = (data) => {
  try {
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

    handleLoading(true);

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
      handleLoading(false);
    } catch (err) {
      console.error("요청 실패", err);

      alert("요청 중 오류가 발생했습니다.");
    } finally {
      handleLoading(false);
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  handleForm();
});
