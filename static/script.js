document.addEventListener("DOMContentLoaded", () => {
    const dropZone = document.getElementById("drop-zone");
    const fileInput = document.getElementById("file-input");
    const previewContainer = document.getElementById("preview-container");
    const previewImg = document.getElementById("preview-img");
    const btnPredict = document.getElementById("btn-predict");
    const btnCancel = document.getElementById("btn-cancel");

    const resultPlaceholder = document.getElementById("result-placeholder");
    const loading = document.getElementById("loading");
    const resultImg = document.getElementById("result-img");
    const statsPanel = document.getElementById("stats-panel");
    const detectionsList = document.getElementById("detections-list");

    let currentFile = null;

    // 1. Mở hộp thoại chọn file khi click vào drop zone
    dropZone.addEventListener("click", () => {
        fileInput.click();
    });

    // 2. Xử lý Drag & Drop trên toàn bộ trang web (tránh lỡ tay thả ra ngoài bị mất trang)
    document.addEventListener("dragover", (e) => {
        e.preventDefault();
        // Làm nổi bật khu vực drop zone khi đang kéo file trên màn hình
        if (dropZone.style.display !== "none") {
            dropZone.classList.add("dragover");
        }
    });

    document.addEventListener("dragleave", (e) => {
        e.preventDefault();
        if(e.relatedTarget === null || e.relatedTarget.nodeName === "HTML") {
             dropZone.classList.remove("dragover");
        }
    });

    document.addEventListener("drop", (e) => {
        e.preventDefault();
        dropZone.classList.remove("dragover");
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    // 3. Xử lý khi chọn file qua input
    fileInput.addEventListener("change", (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    // Hàm đọc file và hiển thị Preview
    function handleFile(file) {
        if (!file.type.startsWith("image/")) {
            alert("Vui lòng chọn một file hình ảnh hợp lệ!");
            return;
        }

        currentFile = file;
        const reader = new FileReader();
        reader.onload = (e) => {
            previewImg.src = e.target.result;
            dropZone.style.display = "none";
            previewContainer.style.display = "flex";
            
            // Reset khu vực kết quả
            resetResultArea();
        };
        reader.readAsDataURL(file);
    }

    // Nút Hủy
    btnCancel.addEventListener("click", () => {
        currentFile = null;
        fileInput.value = "";
        previewContainer.style.display = "none";
        dropZone.style.display = "flex";
        resetResultArea();
    });

    // Nút Chạy Mô Hình
    btnPredict.addEventListener("click", async () => {
        if (!currentFile) return;

        // Đổi UI sang trạng thái Loading
        resultPlaceholder.style.display = "none";
        resultImg.style.display = "none";
        statsPanel.style.display = "none";
        loading.style.display = "flex";
        btnPredict.disabled = true;
        btnPredict.textContent = "Đang xử lý...";

        // Chuẩn bị form data gửi lên Backend
        const formData = new FormData();
        formData.append("file", currentFile);

        try {
            const response = await fetch("/predict", {
                method: "POST",
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                // Hiển thị ảnh trả về (dạng base64)
                resultImg.src = "data:image/jpeg;base64," + data.image_base64;
                loading.style.display = "none";
                resultImg.style.display = "block";

                // Hiển thị danh sách nhận diện
                detectionsList.innerHTML = "";
                if (data.detections.length > 0) {
                    data.detections.forEach(det => {
                        const li = document.createElement("li");
                        li.className = "detection-item";
                        li.innerHTML = `<span class="det-name">${det.class}</span> <span class="det-conf">${(det.confidence * 100).toFixed(0)}%</span>`;
                        detectionsList.appendChild(li);
                    });
                } else {
                    detectionsList.innerHTML = `<li class="detection-item"><span class="det-name">Không tìm thấy biển báo nào</span></li>`;
                }
                statsPanel.style.display = "block";

            } else {
                alert("Lỗi từ server: " + data.error);
                resetResultArea();
            }

        } catch (error) {
            alert("Lỗi kết nối tới Server. Đảm bảo bạn đã chạy file app.py!");
            console.error(error);
            resetResultArea();
        } finally {
            btnPredict.disabled = false;
            btnPredict.textContent = "Chạy Mô Hình Phân Tích";
        }
    });

    function resetResultArea() {
        resultPlaceholder.style.display = "flex";
        loading.style.display = "none";
        resultImg.style.display = "none";
        statsPanel.style.display = "none";
    }

    // Modal phóng to ảnh Logic
    const modal = document.getElementById("image-modal");
    const modalImg = document.getElementById("modal-img");
    const spanClose = document.getElementsByClassName("close")[0];

    // Phóng to ảnh kết quả khi click
    resultImg.addEventListener("click", function(){
        modal.style.display = "block";
        modalImg.src = this.src;
    });

    // Phóng to ảnh preview khi click (tuỳ chọn)
    previewImg.addEventListener("click", function(){
        if(this.src) {
            modal.style.display = "block";
            modalImg.src = this.src;
        }
    });
    previewImg.style.cursor = "zoom-in";

    // Đóng modal khi click nút x
    spanClose.addEventListener("click", function() { 
        modal.style.display = "none";
    });

    // Đóng modal khi click ra ngoài ảnh
    modal.addEventListener("click", function(e) {
        if (e.target !== modalImg) {
            modal.style.display = "none";
        }
    });
});
