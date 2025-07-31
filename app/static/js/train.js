let isUploading = false;
let logInterval = null;

const uploadExcel = async (file) => {
  if (isUploading || !file) return;

  isUploading = true;

  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('api/upload/excel', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorText = await response.text();

      throw new Error(errorText || '서버 오류 발생');
    }

    const result = await response.json();

    if (!result.success) {
      throw new Error(result.message);
    }

    alert(result.message);

    const input = document.getElementById("file-input");

    input.value = '';
  } catch (error) {
    console.error("Error occurred while uploading excel file", error)

    alert('업로드 중 오류가 발생했습니다.');
  } finally {
    isUploading = false;
  }
}

const handleExcelChange = () => {
  const fileInput = document.getElementById("file-input");
  const fileNameSpan = document.getElementById("file-name");

  if (!fileInput || !fileNameSpan) return;

  fileInput.addEventListener("change", async (event) => {
    const file = fileInput.files[0];

    if (!file) return;

    const ext = file.name.split('.').pop()?.toLowerCase();
    const allowedExts = ['xls', 'xlsx'];
    const allowedTypes = [
      'application/haansoftxlsx',
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      'application/vnd.ms-excel'
    ];

    if (!allowedTypes.includes(file.type) || !allowedExts.includes(ext)) {
      alert('엑셀 파일만 업로드 가능합니다.');

      fileInput.value = '';
      fileNameSpan.textContent = '선택된 파일 없음';

      return;
    }

    fileNameSpan.textContent = file.name;

    await uploadExcel(file);
  });
}

const stopPollingLogs = () => {
  if (logInterval) {
    clearInterval(logInterval);

    logInterval = null;
  }
}

const pollFinetuneLogs = () => {
  const logElement = document.getElementById("log-output");

  if (!logElement) return;

  if (logInterval) {
    clearInterval(logInterval);
  }

  logInterval = setInterval(async () => {
    try {
      const res = await fetch("/api/finetune/logs");
      const data = await res.json();

      logElement.textContent = data.message;
      logElement.scrollTop = logElement.scrollHeight;

      if (!data.success) {
        stopPollingLogs();
      }
    } catch (e) {
      logElement.textContent = "[로그 로딩 실패]";
    }
  }, 1000);
};

const startFinetune = async () => {
  try {
    const response = await fetch("/api/finetune/start", { method: "POST" });
    const result = await response.json();

    if (!response.ok) {
      alert(result.message || '서버 오류 발생');

      throw new Error(result.message || '서버 오류 발생');
    }

    pollFinetuneLogs();
  } catch (e) {
    console.error("Error occurred while uploading excel file", error)
  }
}

const stopFinetune = async () => {
  try {
    const response = await fetch("/api/finetune/stop", { method: "POST" });
    const result = await response.json();

    if (!response.ok) {
      alert(result.message || '서버 오류 발생');

      throw new Error(result.message || '서버 오류 발생');
    }

    stopPollingLogs();
  } catch (e) {
    console.error("Error occurred while uploading excel file", error)
  }
}

const handleFinetuneButtons = () => {
  const startButton = document.getElementById("start-finetune-button");
  const stopButton = document.getElementById("stop-finetune-button");

  if (!startButton || !stopButton) return;

  startButton.addEventListener("click", startFinetune);
  stopButton.addEventListener("click", stopFinetune);
}

document.addEventListener("DOMContentLoaded", () => {
  handleExcelChange();
  handleFinetuneButtons();
});
