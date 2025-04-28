<template>
    <div class="container position-relative">
        <!-- Background Image -->
        <div class="background-image"></div>

        <div class="row justify-content-center align-items-center min-vh-100 position-relative" style="z-index: 1;">
            <div class="col-md-6 col-lg-4">
                <div class="card border-0 shadow">
                    <div class="card-body p-4">
                        <div class="text-center mb-4">
                            <h3 class="fw-bold">Đăng Nhập</h3>
                            <p class="text-muted small">Chào mừng đến với Web Đặt Resort</p>
                        </div>

                        <form>
                            <div class="mb-3">
                                <label for="email" class="form-label">Email</label>
                                <input type="email" class="form-control" id="email"
                                    placeholder="Nhập email">
                            </div>

                            <div class="mb-4">
                                <label for="password" class="form-label">Mật khẩu</label>
                                <input type="password" class="form-control" id="password"
                                    placeholder="Nhập mật khẩu">
                            </div>
                            <button type="submit" class="btn btn-primary w-100 mb-3">
                                Đăng Nhập
                            </button>

                            <div class="text-center">
                                <div class="row">
                                    <div class="col-lg-7 text-end">
                                        <h6 class="text-decoration-none">Tôi chưa có tài khoản</h6>
                                    </div>
                                    <div class="col-lg-3 text-start">
                                        <router-link to="" class="text-decoration-none">
                                            <h6 class="text-primary">Đăng ký</h6>
                                        </router-link>
                                    </div>
                                </div>               
                            </div>
                        </form>
                    </div>
                </div>
            </div>
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
