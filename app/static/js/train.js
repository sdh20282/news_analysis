let isUploading = false;

async function uploadExcel(file) {
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
    const fileNameSpan = document.getElementById("file-name");

    input.value = '';
    fileNameSpan.textContent = '선택된 파일 없음';
  } catch (error) {
    console.error("Error occurred while uploading excel file", error)

    alert('업로드 중 오류가 발생했습니다.');
  } finally {
    isUploading = false;
  }
}

function handleExcelChange() {
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
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', // .xlsx
      'application/vnd.ms-excel' // .xls
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

document.addEventListener("DOMContentLoaded", () => {
  handleExcelChange();
});
