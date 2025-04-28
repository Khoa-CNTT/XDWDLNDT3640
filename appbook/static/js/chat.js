document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("imageModal");
    const fullImage = document.getElementById("fullImage");
    const closeBtn = document.querySelector(".close");

    // Mở ảnh lớn khi click vào ảnh nhỏ
    document.querySelectorAll(".chat-image").forEach(img => {
        img.addEventListener("click", function () {
            fullImage.src = this.src;
            modal.style.display = "block";
        });
    });

    // Đóng modal khi click vào nút đóng
    closeBtn.addEventListener("click", function () {
        modal.style.display = "none";
    });

    // Đóng modal khi click ra ngoài nền tối
    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
});
