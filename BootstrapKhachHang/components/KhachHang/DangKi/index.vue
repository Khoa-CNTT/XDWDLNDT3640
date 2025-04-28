<template>
    <div class="background-image"></div>
    <div class="container mt-5">
        <div class="row w-100">
            <div class="col-lg-3"></div>
            <div class="col-lg-6">
                <div class="card shadow p-4">
                    <h1 class="text-center mb-3">📝 Đăng Ký Tài Khoản</h1>
                    <p class="text-center text-muted">Tham gia ngay để nhân được những ưu đãi tuyệt vời!</p>

                    <form>
                        <div class="mb-3">
                            <label>👤 Tên Tài Khoản:</label>
                            <input type="text" class="form-control"
                                placeholder="Nhập tên tài khoản của bạn">
                        </div>
                        <div class="mb-3">
                            <label>📧 Email:</label>
                            <input type="email" class="form-control"
                                placeholder="Nhập email của bạn">
                        </div>
                        <div class="mb-3">
                            <label>Họ:</label>
                            <input type="number" class="form-control"
                                placeholder="Nhập họ của bạn">
                        </div>
                        <div class="mb-3">
                            <label>Tên:</label>
                            <input type="text" class="form-control"
                                placeholder="Nhập tên của bạn">
                        </div>
                        <div class="mb-3">
                            <label>🔒 Mật Khẩu:</label>
                            <input type="password" class="form-control"
                                placeholder="Nhập mật khẩu">
                        </div>

                        <div class="mb-3">
                            <label>🔄 Xác Nhận Mật Khẩu:</label>
                            <input type="password" class="form-control"
                                placeholder="Xác nhận mật khẩu">
                        </div>

                        <div class="d-grid">
                            <button type="button" class="btn btn-success">
                                Đăng Ký
                            </button>
                        </div>
                    </form>

                    <div class="text-center mt-3">
                        <p>Đã có tài khoản?
                            <router-link to="/khach-hang/dang-nhap">
                                <a href="#" class="text-decoration-none">🚀 Đăng Nhập</a>
                            </router-link>
                        </p>
                    </div>
                </div>
            </div>
            <div class="col-lg-3"></div>
        </div>
    </div>
</template>

<style scoped>
.background-image {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: url('https://static.wixstatic.com/media/c9a15a_87964ab282744f05add609c9b770613f~mv2.jpg/v1/fill/w_715,h_403,al_c,q_80,usm_0.66_1.00_0.01,enc_auto/resort.jpg');
    background-size: cover;
    background-position: center;
    filter: blur(2px);
    opacity: 0.6;
    z-index: 0;
}
</style>

<script>
export default {
    data() {
        return {
        }
    },
}
</script>
<style></style>