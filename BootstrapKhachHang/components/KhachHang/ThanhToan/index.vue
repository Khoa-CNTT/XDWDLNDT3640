<template>
    <div class="card border-0 shadow-sm mb-4">
        <div class="card-body">
            <div class="d-flex justify-content-between align-items-center">
                <div class="d-flex align-items-center">
                    <h2 class="card-title mb-0 fw-bold">Thanh Toán</h2>
                </div>
            </div>
        </div>
    </div>
    <div class="row">
        <div class="card">
            <div class="row g-0">
                <div class="col-lg-4">
                    <div class="card-body">
                        <h2 class="card-title mb-3">Thông Tin Thanh Toán</h2>
                        <dl class="row">
                            <dt class="col-sm-4">Quản Lý Resort:</dt>
                            <dd class="col-sm-8">Amango</dd>

                            <dt class="col-sm-4">Resort:</dt>
                            <dd class="col-sm-8">Amango</dd>

                            <dt class="col-sm-4">Khách Hàng:</dt>
                            <dd class="col-sm-8">vung0</dd>

                            <dt class="col-sm-4">Email:</dt>
                            <dd class="col-sm-8">vungne@gmail.com</dd>

                            <dt class="col-sm-4">Ngày Đến:</dt>
                            <dd class="col-sm-8">April 26,2025</dd>

                            <dt class="col-sm-4">Ngày Đi:</dt>
                            <dd class="col-sm-8">May 1,2025</dd>

                            <dt class="col-sm-4">Số phòng:</dt>
                            <dd class="col-sm-8">3</dd>

                            <dt class="col-sm-4">Tổng Tiền:</dt>
                            <dd class="col-sm-8">750K VNĐ</dd>

                            <dt class="col-sm-4">ID Thanh Toán:</dt>
                            <dd class="col-sm-8">PAY49421849948</dd>
                        </dl>
                    </div>
                </div>
                <div class="col-lg-6">
                    <div class="card-body">
                        <h2 class="card-title">Quét Mã QR</h2>
                        <p>*Lưu ý nội dung thanh toán là ID thanh toán</p>
                        <dl class="row">
                            <img src="https://th.bing.com/th/id/R.dcf4b6e228aef80dd1a58f4c76f07128?rik=Qj2LybacmBALtA&riu=http%3a%2f%2fpngimg.com%2fuploads%2fqr_code%2fqr_code_PNG25.png&ehk=eKH2pdoegouCUxO1rt6BJXt4avVYywmyOS8biIPp5zc%3d&risl=&pid=ImgRaw&r=0"
                                alt="" style="width: 25%;">
                        </dl>
                        <button class="btn btn-primary">Xác Nhận Thanh Toán</button>
                        <button class="btn btn-danger ms-2">Huỷ Đặt Phòng</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    data() {
        return {

        }
    },
}
</script>

<style></style>